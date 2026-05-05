import re
from datetime import date
from pathlib import Path

from agents.config import settings
from agents.llm import invoke, load_prompt
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
        "research", "outputs/reports", "outputs/evals",
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
        lines.append("Restore them from AGENTS.md or version control to avoid weakening generation quality.")

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
            ".obsidian/workspace-mobile.json\n.trash/\n\n# OS files\n.DS_Store\nThumbs.db\n\n"
            "# Large binary files\nraw/papers/*.pdf\nraw/web/*.pdf\n\nresearch/\n"
        ),
        settings.vault_root / "research" / "chapter-1-current-state.md": _chapter_template("Chapter 1: Current State of the Field"),
        settings.vault_root / "research" / "chapter-2-methodology.md": _chapter_template("Chapter 2: Methodology"),
        settings.vault_root / "research" / "chapter-3-findings.md": _chapter_template("Chapter 3: Findings"),
        settings.vault_root / "research" / "_research-index.md": (
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
    return [
        path.read_text()
        for path in all_files
        if topic.lower() in path.read_text().lower() or topic.lower() in path.stem.lower()
    ]
