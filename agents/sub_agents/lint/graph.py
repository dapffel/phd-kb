import re
from datetime import date

import frontmatter
from langgraph.graph import StateGraph, END

from agents.config import settings
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
        all_files = self.vault.list_summaries() + self.vault.list_concepts() + self.vault.list_connections()
        missing_frontmatter = self._missing_frontmatter(all_files)
        stale = self._stale_concepts()
        gaps = self._gaps(all_files)
        contradictions = self._contradiction_candidates(all_files)

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

        if missing_frontmatter:
            lines.append(f"**Missing or incomplete frontmatter**: {len(missing_frontmatter)}")
            for item in missing_frontmatter:
                lines.append(f"  - {item}")
            lines.append("")

        if stale:
            lines.append(f"**Stale concept articles**: {len(stale)}")
            for item in stale:
                lines.append(f"  - {item}")
            lines.append("")

        if gaps:
            lines.append(f"**Gaps / high-frequency missing concepts**: {len(gaps)}")
            for item in gaps:
                lines.append(f"  - [[{item}]]")
            lines.append("")

        if contradictions:
            self._write_contradictions(contradictions)
            lines.append(f"**Contradiction candidates**: {len(contradictions)}")
            for item in contradictions[:10]:
                lines.append(f"  - {item}")
            lines.append("")

        if not any([broken, stats.orphaned, stats.missing_concepts, missing_frontmatter, stale, gaps, contradictions]):
            lines.append("All clear — no issues found.")

        result = LintResult(
            broken_links=broken,
            orphaned=stats.orphaned,
            contradictions=contradictions,
            stale=stale,
            gaps=gaps,
            missing_frontmatter=missing_frontmatter,
        )
        return {"result": result, "report": "\n".join(lines)}

    def _missing_frontmatter(self, paths) -> list[str]:
        required = {"title", "created", "updated", "type", "sources"}
        missing = []
        for path in paths:
            try:
                post = frontmatter.load(str(path))
            except Exception:
                missing.append(str(path.relative_to(settings.vault_root)))
                continue
            absent = []
            for key in sorted(required):
                if key not in post.metadata:
                    absent.append(key)
                elif key != "sources" and not post.get(key):
                    absent.append(key)
            if absent:
                rel = path.relative_to(settings.vault_root)
                missing.append(f"{rel} missing {', '.join(absent)}")
        return missing

    def _stale_concepts(self) -> list[str]:
        summaries = {path.name: path for path in self.vault.list_summaries()}
        stale = []
        for concept_path in self.vault.list_concepts():
            try:
                post = frontmatter.load(str(concept_path))
            except Exception:
                continue
            concept_mtime = concept_path.stat().st_mtime
            newer_sources = []
            for source in post.get("sources", []):
                summary = summaries.get(source) or summaries.get(f"{source.rsplit('.', 1)[0]}.md")
                if summary and summary.stat().st_mtime > concept_mtime:
                    newer_sources.append(summary.stem)
            if newer_sources:
                stale.append(f"[[{concept_path.stem}]] references newer summaries: {', '.join(newer_sources)}")
        return stale

    def _gaps(self, paths) -> list[str]:
        existing = {p.stem for p in paths}
        counts: dict[str, int] = {}
        for path in paths:
            for link in re.findall(r"\[\[([^\]]+)\]\]", path.read_text()):
                counts[link] = counts.get(link, 0) + 1
        return sorted(link for link, count in counts.items() if count >= 3 and link not in existing)

    def _contradiction_candidates(self, paths) -> list[str]:
        patterns = re.compile(
            r"\b("
            r"contradict(?:s|ion|ory)?|"
            r"conflict(?:s|ing)?|"
            r"disagree(?:s|ment)?|"
            r"diverge(?:s|d|nce)?|"
            r"in tension|"
            r"trade-?off"
            r")\b",
            re.IGNORECASE,
        )
        candidates = []
        for path in paths:
            if path.stem == "contradictions":
                continue
            try:
                content = frontmatter.load(str(path)).content
            except Exception:
                content = path.read_text()
            for line in content.splitlines():
                clean = line.strip()
                if clean and patterns.search(clean):
                    candidates.append(f"[[{path.stem}]]: {clean[:180]}")
                    break
        return candidates

    def _write_contradictions(self, contradictions: list[str]):
        path = settings.wiki_dir / "connections" / "contradictions.md"
        created = date.today().isoformat()
        if path.exists():
            try:
                created = str(frontmatter.load(str(path)).get("created", created))
            except Exception:
                pass
        lines = [
            "---",
            'title: "Contradictions and Tensions"',
            f"created: {created}",
            f"updated: {date.today().isoformat()}",
            "type: connection",
            "sources: []",
            "---",
            "",
            "## Candidates",
            "",
            "These are heuristic candidates flagged by `lint`; verify them against sources before treating them as actual contradictions.",
            "",
        ]
        lines += [f"- {item}" for item in contradictions]
        content = "\n".join(lines) + "\n"
        if not path.exists() or path.read_text() != content:
            path.write_text(content)
            self.vault.regenerate_wiki_index()
