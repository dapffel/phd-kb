from langgraph.graph import StateGraph, END

from agents.config import settings
from agents.llm import invoke, load_prompt
from agents.models import EvalState
from agents.sub_agents.base import BaseAgent


class EvalAgent(BaseAgent[EvalState]):
    state_schema = EvalState

    def build_graph(self) -> StateGraph:
        g = StateGraph(EvalState)
        g.add_node("evaluate", self.evaluate)
        g.add_node("save", self.save)
        g.set_entry_point("evaluate")
        g.add_edge("evaluate", "save")
        g.add_edge("save", END)
        return g

    def evaluate(self, state: EvalState) -> dict:
        filename = state["filename"]
        stem = filename.rsplit(".", 1)[0]

        summary_path = settings.wiki_dir / "summaries" / f"{stem}.md"
        if not summary_path.exists():
            return {"eval_report": "", "report": f"No summary found for {filename}"}

        source_text = self.vault.read_extract(filename)
        if not source_text:
            return {"eval_report": "", "report": f"No extract found for {filename}"}

        system = load_prompt("eval-source.md")
        human = (
            f"## Source Text\n{source_text[:10000]}\n\n"
            f"## Wiki Article to Evaluate\n{summary_path.read_text()}"
        )
        return {"eval_report": invoke(system, human, strong=True)}

    def save(self, state: EvalState) -> dict:
        if not state.get("eval_report"):
            return state if isinstance(state, dict) else {}

        filename = state["filename"]
        stem = filename.rsplit(".", 1)[0]
        output_path = settings.outputs_dir / "evals" / f"eval-{stem}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(state["eval_report"])

        return {"report": f"Eval saved to outputs/evals/eval-{stem}.md"}
