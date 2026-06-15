import re
from datetime import date

from langgraph.graph import StateGraph, END

from agents.config import settings
from agents.models import (
    CompileState, IngestState, SynthesizeState, EvalState, QueryState,
    SupervisorState,
)
from agents.vault import Vault
from agents.commands import (
    backfill_references,
    build_citation_network,
    catalog_update,
    create_slides,
    find_catalog,
    init_vault,
    suggest_reading,
    update_chapter,
)
from agents.git_ops import has_changes
from agents.sub_agents.status.graph import StatusAgent
from agents.sub_agents.catalog.graph import CatalogAgent
from agents.sub_agents.ingest.graph import IngestAgent
from agents.sub_agents.compile_concepts.graph import CompileConceptsAgent
from agents.sub_agents.synthesize.graph import SynthesizeAgent
from agents.sub_agents.eval_agent.graph import EvalAgent
from agents.sub_agents.lint.graph import LintAgent
from agents.sub_agents.query.graph import QueryAgent


class Supervisor:
    def __init__(self):
        self.vault = Vault()
        self.dry_run = False

    def build_graph(self) -> StateGraph:
        g = StateGraph(SupervisorState)
        g.add_node("route", self.route)
        g.set_entry_point("route")
        g.add_edge("route", END)
        return g

    def run(self, command: str, args: str = "", dry_run: bool = False) -> str:
        self.dry_run = dry_run
        graph = self.build_graph().compile()
        result = graph.invoke({"command": command, "args": args})
        if isinstance(result, dict):
            return result.get("output", "")
        return result.output

    def route(self, state: SupervisorState) -> dict:
        command = state.command
        args = state.args

        handler = {
            "init": self._init,
            "status": self._status,
            "catalog": self._catalog,
            "catalog-update": self._catalog_update,
            "find": self._find,
            "ingest": self._ingest,
            "ingest-all": self._ingest_all,
            "compile-concepts": self._compile_concepts,
            "synthesize": self._synthesize,
            "slides": self._slides,
            "eval": self._eval,
            "eval-all": self._eval_all,
            "lint": self._lint,
            "query": self._query,
            "update-chapter": self._update_chapter,
            "references": self._references,
            "suggest": self._suggest,
            "backfill-references": self._backfill_references,
        }.get(command)

        if not handler:
            return {"output": f"Unknown command: {command}"}

        return {"output": handler(args)}

    def _with_commit_suggestion(self, output: str, message: str) -> str:
        if has_changes(["wiki/", "raw/_catalog.json", "raw/_catalog.md", "outputs/"]):
            return f"{output}\n\nSuggested commit: `{message}`"
        return output

    def _init(self, args: str) -> str:
        report, changed = init_vault()
        if not changed:
            return report
        return self._with_commit_suggestion(report, "init: scaffold vault structure and prompt templates")

    def _status(self, args: str) -> str:
        return StatusAgent(self.vault).run().report

    def _catalog(self, args: str) -> str:
        result = CatalogAgent(self.vault).run()
        return self._with_commit_suggestion(result.report, f"catalog: {result.report}")

    def _catalog_update(self, args: str) -> str:
        report, changed = catalog_update(self.vault)
        if not changed:
            return report
        return self._with_commit_suggestion(report, "catalog: update extracted and ingested flags")

    def _find(self, args: str) -> str:
        return find_catalog(self.vault, args)

    def _ingest(self, args: str) -> str:
        if not args:
            unprocessed = self.vault.unprocessed_pdfs()
            uningested = self.vault.uningested_papers()
            targets = unprocessed or uningested
            if not targets:
                return "Nothing to ingest."
            args = targets[0]

        result = IngestAgent(self.vault).run(IngestState(filename=args))

        lines = [f"Ingested: {args}"]
        if result.result:
            f = result.result.fidelity
            lines.append(
                f"Fidelity: {f.claims_checked} claims, {f.verified} verified, "
                f"{f.distorted} distorted, {f.unsupported} unsupported "
                f"(attempts: {result.result.attempts})"
            )
            if result.detected_concepts:
                lines.append(f"New concepts detected: {', '.join(result.detected_concepts)}")

        output = "\n".join(lines)
        return self._with_commit_suggestion(output, f"ingest: add {args.rsplit('.', 1)[0]}")

    def _ingest_all(self, args: str) -> str:
        uncataloged = self.vault.unprocessed_pdfs()
        if uncataloged and not self.dry_run:
            self._catalog("")

        uningested = self.vault.uningested_papers()
        web = self.vault.unprocessed_web()
        targets = list(dict.fromkeys(uningested + web))

        if not targets:
            return "All sources already ingested."

        if self.dry_run:
            lines = [f"[dry-run] Would ingest {len(targets)} sources:"]
            lines += [f"  - {t}" for t in targets]
            return "\n".join(lines)

        results = [self._ingest(filename) for filename in targets]
        return "\n\n".join(results)

    def _compile_concepts(self, args: str) -> str:
        if self.dry_run:
            agent = CompileConceptsAgent(self.vault)
            detect_result = agent.detect(CompileState())
            candidates = detect_result.get("concept_names", [])
            if not candidates:
                return "[dry-run] No new concepts to compile."
            lines = [f"[dry-run] Would compile {len(candidates)} concepts:"]
            lines += [f"  - {c}" for c in candidates]
            return "\n".join(lines)

        result = CompileConceptsAgent(self.vault).run()
        return self._with_commit_suggestion(
            result.report,
            f"compile: generate {len(result.created)} concept articles",
        )

    def _synthesize(self, args: str) -> str:
        if not args:
            return "Usage: synthesize <topic>"
        result = SynthesizeAgent(self.vault).run(SynthesizeState(topic=args))
        return self._with_commit_suggestion(result.report, f"synthesize: {args}")

    def _slides(self, args: str) -> str:
        output = create_slides(self.vault, args)
        if output.startswith("Usage:") or output.startswith("No relevant"):
            return output
        slug = args.strip().lower().replace(" ", "-")
        return self._with_commit_suggestion(
            output,
            f"synthesize: create slides for {slug}",
        )

    def _eval(self, args: str) -> str:
        if not args:
            return "Usage: eval <filename>"
        result = EvalAgent(self.vault).run(EvalState(filename=args))
        return self._with_commit_suggestion(result.report or "Eval complete.", f"eval: check {args}")

    def _eval_all(self, args: str) -> str:
        articles = self.vault.list_summaries() + self.vault.list_concepts()

        if self.dry_run:
            lines = [f"[dry-run] Would evaluate {len(articles)} articles:"]
            lines += [f"  - {p.name}" for p in articles]
            return "\n".join(lines)

        per_article: list[dict] = []

        for path in articles:
            result = EvalAgent(self.vault).run(EvalState(filename=path.name))
            counts = self._parse_eval_counts(result.eval_report)
            counts["filename"] = path.name
            per_article.append(counts)

        total_claims = sum(a["claims"] for a in per_article)
        total_verified = sum(a["verified"] for a in per_article)
        total_distorted = sum(a["distorted"] for a in per_article)
        total_unsupported = sum(a["unsupported"] for a in per_article)
        total_missing = sum(a["missing"] for a in per_article)
        fidelity_pct = (total_verified / total_claims * 100) if total_claims else 0

        by_issues = sorted(per_article, key=lambda a: a["issues"], reverse=True)

        lines = [
            "# Eval Summary\n",
            f"**Date**: {date.today().isoformat()}",
            f"**Articles evaluated**: {len(per_article)}",
            f"**Overall fidelity**: {fidelity_pct:.0f}% ({total_verified}/{total_claims} claims verified)\n",
            "## Error Type Breakdown\n",
            f"| Type | Count |",
            f"|------|-------|",
            f"| Distorted | {total_distorted} |",
            f"| Unsupported | {total_unsupported} |",
            f"| Missing attribution | {total_missing} |",
            "",
            "## Articles by Issue Count\n",
            "| Article | Claims | Verified | Issues |",
            "|---------|--------|----------|--------|",
        ]
        for a in by_issues:
            lines.append(f"| {a['filename']} | {a['claims']} | {a['verified']} | {a['issues']} |")

        needs_attention = [a["filename"] for a in by_issues if a["issues"] > 0]
        if needs_attention:
            lines += ["", "## Needs Attention\n"]
            for name in needs_attention:
                lines.append(f"- {name}")

        summary_path = settings.outputs_dir / "evals" / "_eval-summary.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text("\n".join(lines) + "\n")

        return self._with_commit_suggestion(
            f"Eval-all: {len(per_article)} articles, {fidelity_pct:.0f}% fidelity. "
            f"Roll-up saved to outputs/evals/_eval-summary.md",
            f"eval: eval-all run, {fidelity_pct:.0f}% fidelity",
        )

    @staticmethod
    def _parse_eval_counts(raw: str) -> dict:
        def _find(label: str) -> int:
            m = re.search(rf"\*?\*?{label}\*?\*?\s*[:\|]\s*(\d+)", raw or "", re.IGNORECASE)
            return int(m.group(1)) if m else 0

        claims = _find("Claims.checked")
        verified = _find("Verified")
        distorted = _find("Distorted")
        unsupported = _find("Unsupported")
        missing = _find("Missing.attribution")
        return {
            "claims": claims,
            "verified": verified,
            "distorted": distorted,
            "unsupported": unsupported,
            "missing": missing,
            "issues": distorted + unsupported + missing,
        }

    def _lint(self, args: str) -> str:
        result = LintAgent(self.vault).run()
        return self._with_commit_suggestion(result.report, "lint: update wiki health report artifacts")

    def _query(self, args: str) -> str:
        if not args:
            return "Usage: query <question>"
        result = QueryAgent(self.vault).run(QueryState(question=args))
        slug = args.strip()[:60].lower().replace(" ", "-")
        return (
            f"{result.answer}\n\n"
            f"Save this answer? Run:\n"
            f"  `synthesize {slug}` → wiki/connections/{slug}.md\n"
            f"Or save manually to outputs/reports/{slug}.md"
        )

    def _update_chapter(self, args: str) -> str:
        return update_chapter(self.vault, args)

    def _references(self, args: str) -> str:
        output = build_citation_network(self.vault)
        return self._with_commit_suggestion(output, "references: build citation network")

    def _suggest(self, args: str) -> str:
        return suggest_reading(self.vault)

    def _backfill_references(self, args: str) -> str:
        output = backfill_references(self.vault)
        return self._with_commit_suggestion(output, "references: backfill existing summaries")
