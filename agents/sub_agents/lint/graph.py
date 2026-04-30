from langgraph.graph import StateGraph, END

from agents.models import BrokenLink, LintResult, LintState
from agents.sub_agents.base import BaseAgent


class LintAgent(BaseAgent[LintState]):
    state_schema = LintState

    def build_graph(self) -> StateGraph:
        g = StateGraph(LintState)
        g.add_node("check", self.check)
        g.set_entry_point("check")
        g.add_edge("check", END)
        return g

    def check(self, state: LintState) -> dict:
        stats = self.vault.stats()

        broken = [BrokenLink(link=l, suggestion="create concept article") for l in stats.broken_links]

        lines = ["## Wiki Health Report", ""]

        if broken:
            lines.append(f"**Broken links**: {len(broken)}")
            for b in broken:
                lines.append(f"  - [[{b.link}]] — {b.suggestion}")
            lines.append("")

        if stats.orphaned:
            lines.append(f"**Orphaned articles**: {len(stats.orphaned)}")
            for o in stats.orphaned:
                lines.append(f"  - {o}")
            lines.append("")

        if stats.missing_concepts:
            lines.append(f"**Suggested new concept articles**: {len(stats.missing_concepts)}")
            for c in stats.missing_concepts:
                lines.append(f"  - [[{c}]]")
            lines.append("")

        if not broken and not stats.orphaned and not stats.missing_concepts:
            lines.append("All clear — no issues found.")

        result = LintResult(broken_links=broken, orphaned=stats.orphaned)
        return {"result": result, "report": "\n".join(lines)}
