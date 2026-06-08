import json
import re
from datetime import date
from pathlib import Path

import frontmatter
import fitz

from agents.config import settings
from agents.models import CatalogEntry, WikiArticle, WikiStats


class Vault:
    def __init__(self, root: Path = settings.vault_root):
        self.root = root

    # --- Catalog ---

    def load_catalog(self) -> list[CatalogEntry]:
        if not settings.catalog_json.exists():
            return []
        data = json.loads(settings.catalog_json.read_text())
        return [CatalogEntry(**entry) for entry in data]

    def save_catalog(self, entries: list[CatalogEntry]):
        data = [entry.model_dump() for entry in entries]
        settings.catalog_json.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        self._regenerate_catalog_md(entries)

    def mark_ingested(self, filename: str):
        catalog = self.load_catalog()
        for entry in catalog:
            if entry.filename == filename:
                entry.extracted = True
                entry.ingested = True
                break
        self.save_catalog(catalog)

    def _regenerate_catalog_md(self, entries: list[CatalogEntry]):
        extracted_count = sum(1 for e in entries if e.extracted)
        ingested_count = sum(1 for e in entries if e.ingested)

        lines = [
            "---",
            f'title: "Source Catalog"',
            f"updated: {_today()}",
            f"total: {len(entries)}",
            f"extracted: {extracted_count}",
            f"ingested: {ingested_count}",
            "---",
            "",
            "## All Sources",
            "",
            "| # | Title | Authors | Year | Keywords | Extracted | Ingested |",
            "|---|-------|---------|------|----------|-----------|----------|",
        ]

        for i, e in enumerate(entries, 1):
            authors = ", ".join(e.authors[:3])
            if len(e.authors) > 3:
                authors += " et al."
            kw = ", ".join(e.keywords[:5])
            ext = "✅" if e.extracted else "❌"
            ing = "✅" if e.ingested else "❌"
            lines.append(f"| {i} | {e.title} | {authors} | {e.year} | {kw} | {ext} | {ing} |")

        not_extracted = [e.filename for e in entries if not e.extracted]
        not_ingested = [e for e in entries if e.extracted and not e.ingested]

        lines += ["", "## Not Yet Extracted", ""]
        lines += [f"- {f}" for f in not_extracted] if not_extracted else ["(none)"]

        lines += ["", "## Extracted But Not Ingested", ""]
        lines += [f"- {e.filename}" for e in not_ingested] if not_ingested else ["(none)"]

        settings.catalog_md.write_text("\n".join(lines) + "\n")

    # --- PDF extraction ---

    def extract_pdf(self, filename: str) -> str:
        pdf_path = settings.papers_dir / filename
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            raise ValueError(f"Cannot open PDF '{filename}': {e}") from e

        pages = []
        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                pages.append(f"--- Page {i + 1} ---\n{text}")
        doc.close()

        if not pages:
            raise ValueError(f"PDF '{filename}' produced no extractable text (scanned image?)")

        return "\n\n".join(pages)

    def save_extract(self, filename: str, content: str) -> Path:
        md_name = Path(filename).stem + ".md"
        path = settings.papers_dir / md_name
        path.write_text(content)
        return path

    def read_extract(self, filename: str) -> str:
        md_name = Path(filename).stem + ".md"
        path = settings.papers_dir / md_name
        return path.read_text() if path.exists() else ""

    def has_extract(self, filename: str) -> bool:
        md_name = Path(filename).stem + ".md"
        return (settings.papers_dir / md_name).exists()

    def has_summary(self, filename: str) -> bool:
        md_name = Path(filename).stem + ".md"
        return (settings.wiki_dir / "summaries" / md_name).exists()

    # --- Wiki articles ---

    def read_article(self, path: Path) -> WikiArticle:
        post = frontmatter.load(str(path))
        return WikiArticle(
            path=str(path.relative_to(self.root)),
            title=post.get("title", ""),
            type=post.get("type", ""),
            sources=post.get("sources", []),
            created=post.get("created"),
            updated=post.get("updated"),
            content=post.content,
        )

    def save_article(self, subdir: str, filename: str, content: str):
        path = settings.wiki_dir / subdir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def list_summaries(self) -> list[Path]:
        d = settings.wiki_dir / "summaries"
        return sorted(d.glob("*.md")) if d.exists() else []

    def list_concepts(self) -> list[Path]:
        d = settings.wiki_dir / "concepts"
        return sorted(d.glob("*.md")) if d.exists() else []

    def list_connections(self) -> list[Path]:
        d = settings.wiki_dir / "connections"
        return sorted(d.glob("*.md")) if d.exists() else []

    # --- Wiki index files ---

    def regenerate_wiki_index(self):
        summaries = self.list_summaries()
        concepts = self.list_concepts()
        connections = self.list_connections()

        lines = [
            "---",
            'title: "Wiki Index"',
            f"updated: {_today()}",
            "---",
            "",
            "## Summaries",
            "",
        ]
        for f in summaries:
            lines.append(f"- [[{f.stem}]]")

        lines += ["", "## Concepts", ""]
        for f in concepts:
            lines.append(f"- [[{f.stem}]]")

        lines += ["", "## Connections", ""]
        for f in connections:
            lines.append(f"- [[{f.stem}]]")

        settings.wiki_index.write_text("\n".join(lines) + "\n")

    def update_sources_file(self, filename: str, title: str):
        sources_path = settings.wiki_sources
        content = sources_path.read_text() if sources_path.exists() else "---\ntitle: Sources\n---\n"
        if filename not in content:
            content += f"\n- **{title}** — `{filename}`"
            sources_path.write_text(content)

    def regenerate_glossary(self):
        concepts = self.list_concepts()
        lines = [
            "---",
            'title: "Glossary"',
            f"updated: {_today()}",
            "---",
            "",
        ]
        for path in concepts:
            definition = self._extract_definition(path.read_text())
            lines.append(f"**[[{path.stem}]]** — {definition}")
            lines.append("")

        settings.wiki_glossary.write_text("\n".join(lines) + "\n")

    def _extract_definition(self, content: str) -> str:
        in_def = False
        for line in content.split("\n"):
            if line.strip() == "## Definition":
                in_def = True
                continue
            if in_def and line.startswith("##"):
                break
            if in_def and line.strip():
                return line.strip()
        return ""

    # --- Wiki stats ---

    def stats(self) -> WikiStats:
        summaries = self.list_summaries()
        concepts = self.list_concepts()
        connections = self.list_connections()

        all_files = summaries + concepts + connections
        existing_stems = {f.stem for f in all_files}

        total_words = 0
        broken = []
        linked_to = set()

        for f in all_files:
            content = f.read_text()
            total_words += len(content.split())
            links = re.findall(r"\[\[([^\]]+)\]\]", content)
            linked_to.update(links)
            for link in links:
                if link not in existing_stems:
                    broken.append(link)

        orphaned = [f.stem for f in all_files if f.stem not in linked_to]

        return WikiStats(
            summaries=len(summaries),
            concepts=len(concepts),
            connections=len(connections),
            total_words=total_words,
            broken_links=sorted(set(broken)),
            orphaned=orphaned,
            missing_concepts=sorted(set(broken) - {f.stem for f in summaries}),
        )

    # --- Utility ---

    def read_index(self) -> str:
        return settings.wiki_index.read_text() if settings.wiki_index.exists() else ""

    def read_file(self, path: Path) -> str:
        return path.read_text() if path.exists() else ""

    def unprocessed_pdfs(self) -> list[str]:
        catalog = self.load_catalog()
        cataloged = {e.filename for e in catalog}
        pdfs = settings.papers_dir.glob("*.pdf")
        return [p.name for p in pdfs if p.name not in cataloged]

    def uningested_papers(self) -> list[str]:
        catalog = self.load_catalog()
        return [e.filename for e in catalog if e.extracted and not e.ingested]


def _today() -> str:
    return date.today().isoformat()
