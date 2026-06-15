import json
import re
from datetime import date
from pathlib import Path

import frontmatter

from agents.config import settings
from agents.llm import invoke, load_prompt
from agents.models import CatalogEntry, Reference
from agents.vault import Vault


PROMPT_FILES = [
    "compile-source.md",
    "write-concept.md",
    "lint-wiki.md",
    "query.md",
    "update-chapter.md",
    "synthesize.md",
    "eval-source.md",
]


def init_vault() -> tuple[str, bool]:
    dirs = [
        "raw/papers", "raw/notes", "raw/web", "raw/images",
        "wiki/summaries", "wiki/concepts", "wiki/connections",
        "research/templates", "outputs/reports", "outputs/evals",
        "outputs/slides", "outputs/figures", "prompts",
    ]
    for dirname in dirs:
        (settings.vault_root / dirname).mkdir(parents=True, exist_ok=True)

    created = []
    files = _starter_files()
    for path, content in files.items():
        if not path.exists():
            path.write_text(content)
            created.append(str(path.relative_to(settings.vault_root)))

    missing_prompts = [
        name for name in PROMPT_FILES
        if not (settings.prompts_dir / name).exists()
    ]

    lines = [
        f"Initialized vault structure. Created {len(created)} files; existing files were left untouched."
    ]
    if missing_prompts:
        lines.append(
            "Missing prompt templates were not recreated from stubs: "
            + ", ".join(missing_prompts)
        )
        lines.append("Restore them from CLAUDE.md or version control to avoid weakening generation quality.")

    return "\n".join(lines), bool(created)


def catalog_update(vault: Vault) -> tuple[str, bool]:
    catalog = vault.load_catalog()
    changed = False
    for entry in catalog:
        extracted = vault.has_extract(entry.filename)
        ingested = vault.has_summary(entry.filename)
        changed = changed or entry.extracted != extracted or entry.ingested != ingested
        entry.extracted = extracted
        entry.ingested = ingested
    if changed:
        vault.save_catalog(catalog)
    return f"Catalog updated. Total: {len(catalog)}.", changed


def find_catalog(vault: Vault, args: str) -> str:
    query = args.strip().strip('"').lower()
    if not query:
        return "Usage: find <query>"

    matches = []
    for entry in vault.load_catalog():
        haystack = " ".join([
            entry.title,
            " ".join(entry.authors),
            " ".join(entry.keywords),
        ]).lower()
        if query in haystack:
            matches.append(entry)

    if not matches:
        return f"No catalog matches for: {args}"

    lines = [f"Found {len(matches)} matches:", ""]
    not_ingested = []
    for i, entry in enumerate(matches, 1):
        authors = ", ".join(entry.authors[:3])
        if len(entry.authors) > 3:
            authors += " et al."
        ext = "extracted" if entry.extracted else "not extracted"
        ing = "ingested" if entry.ingested else "not ingested"
        if not entry.ingested:
            not_ingested.append(entry.filename)
        lines += [
            f"{i}. \"{entry.title}\" — {authors}, {entry.year}",
            f"   Keywords: {', '.join(entry.keywords)}",
            f"   Status: {ext}, {ing}",
            "",
        ]
    if not_ingested:
        lines.append("Some matches have not been ingested yet. Run `ingest <filename>` for any you want to add.")
    return "\n".join(lines).rstrip()


def create_slides(vault: Vault, args: str) -> str:
    if not args:
        return "Usage: slides <topic>"
    topic = args.strip()
    relevant = _relevant_wiki_text(vault, topic)[:10]
    if not relevant:
        return f"No relevant wiki articles found for slides topic: {topic}"

    system = (
        "You are creating a Marp slide deck from a PhD research wiki. "
        "Return only markdown. Include Marp frontmatter and cite wiki sources with [[wikilinks]]."
    )
    human = f"Topic: {topic}\n\nWiki context:\n\n" + "\n---\n".join(relevant)
    deck = invoke(system, human, strong=True)
    slug = topic.lower().replace(" ", "-")
    path = settings.outputs_dir / "slides" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(deck)
    return f"Slide deck saved to outputs/slides/{slug}.md"


def update_chapter(vault: Vault, args: str) -> str:
    if not args:
        return "Usage: update-chapter <chapter-name>"
    chapter = args if args.endswith(".md") else f"{args}.md"
    path = settings.vault_root / "research" / chapter
    if not path.exists():
        matches = list((settings.vault_root / "research").glob(f"*{args}*.md"))
        if len(matches) == 1:
            path = matches[0]
        else:
            return f"No chapter found for: {args}"

    content = path.read_text()
    links = sorted(set(re.findall(r"\[\[([^\]]+)\]\]", content)))
    wiki_files = {
        p.stem: p
        for p in vault.list_summaries() + vault.list_concepts() + vault.list_connections()
    }
    referenced = [wiki_files[link].read_text() for link in links if link in wiki_files]

    system = load_prompt("update-chapter.md")
    human = (
        f"Chapter file: {path.name}\n\n## Chapter\n{content}\n\n"
        f"## Referenced wiki articles\n\n" + "\n---\n".join(referenced)
    )
    return invoke(system, human, strong=True)


def _starter_files() -> dict[Path, str]:
    return {
        settings.raw_dir / "_catalog.json": "[]\n",
        settings.raw_dir / "_catalog.md": (
            "---\n"
            'title: "Source Catalog"\n'
            f"updated: {date.today().isoformat()}\n"
            "total: 0\n"
            "extracted: 0\n"
            "ingested: 0\n"
            "---\n\n"
            "## All Sources\n\n"
        ),
        settings.wiki_index: "---\ntitle: \"Wiki Index\"\nupdated: \n---\n\n## Summaries\n\n## Concepts\n\n## Connections\n",
        settings.wiki_sources: "---\ntitle: \"Source Catalog\"\nupdated: \n---\n\n## Ingested Sources\n",
        settings.wiki_glossary: "---\ntitle: \"Glossary\"\nupdated: \n---\n\n## Terms\n",
        settings.vault_root / ".gitignore": (
            "# Obsidian temporary files\n.obsidian/workspace.json\n"
            ".obsidian/workspace-mobile.json\n.trash/\n\n"
            "# OS files\n.DS_Store\nThumbs.db\n\n"
            "# Python\n__pycache__/\n*.pyc\n.claude/\n*.egg-info/\n.venv/\n\n"
            "# Large binary files\nraw/papers/*.pdf\nraw/web/*.pdf\n\n"
            "# Obsidian plugin cache\n.obsidian/plugins/*/data.json\n\n"
            "# Research chapters — excluded until you're ready to commit them.\n"
            "research/*\n!research/.gitkeep\n!research/README.md\n"
            "!research/templates/\n!research/templates/*.md\n"
        ),
        settings.vault_root / "research" / "templates" / "chapter-1-current-state.md": _chapter_template("Chapter 1: Current State of the Field"),
        settings.vault_root / "research" / "templates" / "chapter-2-methodology.md": _chapter_template("Chapter 2: Methodology"),
        settings.vault_root / "research" / "templates" / "chapter-3-findings.md": _chapter_template("Chapter 3: Findings"),
        settings.vault_root / "research" / "templates" / "_research-index.md": (
            "---\ntitle: \"Research Overview\"\nupdated: \n---\n\n"
            "## Dissertation Structure\n\n"
            "| Chapter | Title | Status | Last Updated |\n"
            "|---------|-------|--------|-------------|\n"
            "| 1 | Current State of the Field | not started | — |\n"
            "| 2 | Methodology | not started | — |\n"
            "| 3 | Findings | not started | — |\n"
        ),
    }


def _chapter_template(title: str) -> str:
    return (
        "---\n"
        f'title: "{title}"\n'
        "status: draft\n"
        "updated: \n"
        "---\n\n"
        "## Research Question\n\n"
        "## Current State\n\n"
        "## Key Debates and Disagreements\n\n"
        "## Identified Gaps\n\n"
        "## My Position\n\n"
        "## TODO\n"
        "- [ ] Draft this chapter\n"
    )


def _relevant_wiki_text(vault: Vault, topic: str) -> list[str]:
    all_files = vault.list_summaries() + vault.list_concepts() + vault.list_connections()
    topic_lower = topic.lower()
    relevant = []
    for path in all_files:
        content = path.read_text()
        if topic_lower in content.lower() or topic_lower in path.stem.lower():
            relevant.append(content)
    return relevant


def match_reference_to_catalog(
    ref: dict, catalog: list[CatalogEntry]
) -> CatalogEntry | None:
    ref_author = ref.get("author", "").lower().strip()
    ref_year = ref.get("year", 0)
    if not ref_author or not ref_year:
        return None

    for entry in catalog:
        if entry.year == ref_year and entry.authors and entry.authors[0].lower() == ref_author:
            return entry

    for entry in catalog:
        if entry.year == ref_year and any(a.lower() == ref_author for a in entry.authors):
            return entry

    return None


def build_citation_network(vault: Vault) -> str:
    catalog = vault.load_catalog()
    summaries = vault.list_summaries()

    cited_by: dict[str, list[str]] = {}
    external_counts: dict[tuple[str, int, str], list[str]] = {}

    for path in summaries:
        post = frontmatter.load(str(path))
        refs = post.get("references", [])
        source_stem = path.stem

        for ref in refs:
            if not isinstance(ref, dict):
                continue
            match = match_reference_to_catalog(ref, catalog)
            if match:
                matched_stem = match.filename.rsplit(".", 1)[0]
                if matched_stem != source_stem:
                    cited_by.setdefault(matched_stem, []).append(source_stem)
            else:
                key = (
                    ref.get("author", "").strip(),
                    ref.get("year", 0),
                    ref.get("title", "").strip()[:80],
                )
                if key[0] and key[1]:
                    external_counts.setdefault(key, []).append(source_stem)

    total_refs = sum(
        len(frontmatter.load(str(p)).get("references", []))
        for p in summaries
    )
    cross_refs = sum(len(citers) for citers in cited_by.values())

    most_cited = sorted(cited_by.items(), key=lambda x: len(x[1]), reverse=True)

    lines = [
        "---",
        'title: "Citation Network"',
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        "type: connection",
        "sources: []",
        "---",
        "",
        "## Overview",
        "",
        f"{len(summaries)} papers in vault. {total_refs} total references extracted. "
        f"{cross_refs} cross-citations between vault papers.",
        "",
        "## Most Cited Within Vault",
        "",
        "| Paper | Cited by | Count |",
        "|-------|----------|-------|",
    ]
    for stem, citers in most_cited:
        citer_links = ", ".join(f"[[{c}]]" for c in citers[:5])
        if len(citers) > 5:
            citer_links += f" +{len(citers) - 5} more"
        lines.append(f"| [[{stem}]] | {citer_links} | {len(citers)} |")

    lines += [
        "",
        "## Citation Edges",
        "",
    ]
    for path in summaries:
        post = frontmatter.load(str(path))
        refs = post.get("references", [])
        matched = []
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            m = match_reference_to_catalog(ref, catalog)
            if m:
                matched_stem = m.filename.rsplit(".", 1)[0]
                if matched_stem != path.stem:
                    matched.append(f"[[{matched_stem}]]")
        if matched:
            lines.append(f"- [[{path.stem}]] cites {', '.join(matched)}")

    top_external = sorted(external_counts.items(), key=lambda x: len(x[1]), reverse=True)[:20]
    if top_external:
        lines += [
            "",
            "## Frequently Cited External Papers",
            "",
            "| # | Author | Year | Title | Cited by |",
            "|---|--------|------|-------|----------|",
        ]
        for i, ((author, year, title), citers) in enumerate(top_external, 1):
            lines.append(f"| {i} | {author} | {year} | {title} | {len(citers)} sources |")

    vault.save_article("connections", "citation-network.md", "\n".join(lines) + "\n")
    vault.regenerate_wiki_index()

    summary_lines = [
        f"{len(summaries)} papers, {total_refs} references, {cross_refs} cross-citations.",
    ]
    if most_cited:
        top = most_cited[0]
        summary_lines.append(f"Most cited: {top[0]} ({len(top[1])} citations).")
    summary_lines.append("Saved to wiki/connections/citation-network.md")
    return "\n".join(summary_lines)


def suggest_reading(vault: Vault) -> str:
    catalog = vault.load_catalog()
    summaries = vault.list_summaries()

    external_counts: dict[tuple[str, int], list[str]] = {}
    best_title: dict[tuple[str, int], str] = {}

    for path in summaries:
        post = frontmatter.load(str(path))
        refs = post.get("references", [])

        for ref in refs:
            if not isinstance(ref, dict):
                continue
            if match_reference_to_catalog(ref, catalog):
                continue
            author = ref.get("author", "").strip()
            year = ref.get("year", 0)
            title = ref.get("title", "").strip()
            if not author or not year:
                continue
            key = (author.lower(), year)
            external_counts.setdefault(key, []).append(path.stem)
            if title and len(title) > len(best_title.get(key, "")):
                best_title[key] = title

    ranked = sorted(external_counts.items(), key=lambda x: len(x[1]), reverse=True)
    ranked = [(k, citers) for k, citers in ranked if len(citers) >= 2]

    if not ranked:
        return "No frequently-cited external papers found (need >= 2 citations)."

    lines = ["Papers frequently cited by your sources but not yet in the vault:", ""]
    for i, ((author, year), citers) in enumerate(ranked[:20], 1):
        title = best_title.get((author, year), "")
        title_str = f' "{title}"' if title else ""
        lines.append(f"  {i}. {author.title()} ({year}){title_str} — cited by {len(citers)} sources")

    return "\n".join(lines)


def backfill_references(vault: Vault) -> str:
    summaries = vault.list_summaries()
    updated = []

    for path in summaries:
        post = frontmatter.load(str(path))
        if post.get("references"):
            continue

        sources = post.get("sources", [])
        if not sources:
            continue

        source_filename = sources[0]
        source_text = vault.read_extract(source_filename)
        if not source_text:
            web_path = settings.web_dir / source_filename
            papers_path = settings.papers_dir / source_filename
            if web_path.exists():
                source_text = web_path.read_text()
            elif papers_path.exists():
                source_text = papers_path.read_text()
        if not source_text:
            continue

        system = load_prompt("extract-references.md")
        text = source_text
        if len(text) > 8000:
            human = text[:2000] + "\n...\n" + text[-6000:]
        else:
            human = text

        try:
            raw = invoke(system, human)
            raw = raw.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```\w*\n?", "", raw)
                raw = re.sub(r"\n?```$", "", raw)
            refs = json.loads(raw)
            references = [
                Reference(author=r["author"], year=int(r["year"]), title=r.get("title", ""))
                for r in refs if isinstance(r, dict) and "author" in r and "year" in r
            ]
        except (json.JSONDecodeError, KeyError, ValueError):
            references = []

        if not references:
            continue

        post.metadata["references"] = [r.model_dump() for r in references]
        path.write_text(frontmatter.dumps(post))
        updated.append(f"{path.stem} ({len(references)} refs)")

    if not updated:
        return "No summaries needed reference backfill."
    return f"Backfilled references for {len(updated)} summaries:\n" + "\n".join(f"  - {u}" for u in updated)
