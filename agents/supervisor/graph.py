from langgraph.graph import StateGraph, END

from agents.models import (
    IngestState, SynthesizeState, EvalState, QueryState,
    SupervisorState, Command,
)
from agents.vault import Vault
from agents.git_ops import commit, has_changes
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

    def build_graph(self) -> StateGraph:
        g = StateGraph(SupervisorState)
        g.add_node("route", self.route)
        g.set_entry_point("route")
        g.add_edge("route", END)
        return g

    def run(self, command: str, args: str = "") -> str:
        graph = self.build_graph().compile()
        result = graph.invoke({"command": command, "args": args})
        return result.get("output", "")

    def route(self, state: SupervisorState) -> dict:
        command = state["command"]
        args = state.get("args", "")

        handler = {
            "status": self._status,
            "catalog": self._catalog,
            "ingest": self._ingest,
            "ingest-all": self._ingest_all,
            "compile-concepts": self._compile_concepts,
            "synthesize": self._synthesize,
            "eval": self._eval,
            "lint": self._lint,
            "query": self._query,
        }.get(command)

        if not handler:
            return {"output": f"Unknown command: {command}"}

        return {"output": handler(args)}

    def _status(self, args: str) -> str:
        return StatusAgent(self.vault).run().report

    def _catalog(self, args: str) -> str:
        result = CatalogAgent(self.vault).run()
        if has_changes():
            commit(f"catalog: {result.report}")
        return result.report

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
        if has_changes():
            commit(f"ingest: add {args.rsplit('.', 1)[0]}")
        return output

    def _ingest_all(self, args: str) -> str:
        unprocessed = self.vault.unprocessed_pdfs()
        uningested = self.vault.uningested_papers()
        targets = list(set(unprocessed + uningested))

        if not targets:
            return "All papers already ingested."

        results = [self._ingest(filename) for filename in targets]
        return "\n\n".join(results)

    def _compile_concepts(self, args: str) -> str:
        result = CompileConceptsAgent(self.vault).run()
        if has_changes():
            commit(f"compile: generate {len(result.created)} concept articles")
        return result.report

    def _synthesize(self, args: str) -> str:
        if not args:
            return "Usage: synthesize <topic>"
        result = SynthesizeAgent(self.vault).run(SynthesizeState(topic=args))
        if has_changes():
            commit(f"synthesize: {args}")
        return result.report

    def _eval(self, args: str) -> str:
        if not args:
            return "Usage: eval <filename>"
        result = EvalAgent(self.vault).run(EvalState(filename=args))
        return result.report or "Eval complete."

    def _lint(self, args: str) -> str:
        return LintAgent(self.vault).run().report

    def _query(self, args: str) -> str:
        if not args:
            return "Usage: query <question>"
        result = QueryAgent(self.vault).run(QueryState(question=args))
        return result.answer
