import frontmatter
from langgraph.graph import StateGraph, END

from agents.config import settings
from agents.models import StatusState
from agents.sub_agents.base import BaseAgent


class StatusAgent(BaseAgent[StatusState]):
    state_schema = StatusState

    def build_graph(self) -> StateGraph:
        g = StateGraph(StatusState)
        g.add_node("gather", self.gather)
        g.set_entry_point("gather")
        g.add_edge("gather", END)
        return g

    def gather(self, state: StatusState) -> dict:
        catalog = self.vault.load_catalog()
        stats = self.vault.stats()

        lines = [
            "## Knowledge Base Status",
            "",
            f"**Sources**: {len(catalog)} cataloged, "
            f"{sum(1 for e in catalog if e.extracted)} extracted, "
            f"{sum(1 for e in catalog if e.ingested)} ingested",
            "",
            f"**Wiki**: {stats.summaries} summaries, {stats.concepts} concepts, "
            f"{stats.connections} connections",
            f"**Total words**: {stats.total_words:,}",
            "",
        ]

        chapters = self._research_chapters()
        if chapters:
            lines.append("**Research chapters**:")
            for name, status, updated in chapters:
                lines.append(f"  - {name} | status: {status} | updated: {updated}")
            lines.append("")

        if stats.broken_links:
            lines.append(f"**Broken links**: {len(stats.broken_links)}")
            for link in stats.broken_links[:10]:
                lines.append(f"  - [[{link}]]")

        if stats.orphaned:
            lines.append(f"**Orphaned articles**: {len(stats.orphaned)}")
            for name in stats.orphaned[:10]:
                lines.append(f"  - {name}")

        if stats.missing_concepts:
            lines.append(f"**Missing concept articles**: {len(stats.missing_concepts)}")
            for name in stats.missing_concepts[:10]:
                lines.append(f"  - [[{name}]]")

        unprocessed = self.vault.unprocessed_pdfs()
        if unprocessed:
            lines.append(f"\n**Unprocessed PDFs**: {len(unprocessed)}")
            for f in unprocessed:
                lines.append(f"  - {f}")

        return {"report": "\n".join(lines)}

    def _research_chapters(self) -> list[tuple[str, str, str]]:
        research_dir = settings.vault_root / "research"
        if not research_dir.exists():
            return []
        chapters = []
        for path in sorted(research_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue
            try:
                post = frontmatter.load(str(path))
                status = post.get("status", "unknown")
                updated = str(post.get("updated", "—"))
            except Exception:
                status = "unknown"
                updated = "—"
            chapters.append((path.stem, status, updated))
        return chapters
