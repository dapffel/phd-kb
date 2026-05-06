from langgraph.graph import StateGraph, END

from agents.config import settings
from agents.llm import invoke, load_prompt
from agents.models import EvalState
from agents.state import state_get
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
        filename = state_get(state, "filename", "")
        stem = filename.rsplit(".", 1)[0]

        summary_path = settings.wiki_dir / "summaries" / f"{stem}.md"
        concept_path = settings.wiki_dir / "concepts" / f"{stem}.md"
        article_path = summary_path if summary_path.exists() else concept_path
        if not article_path.exists():
            return {"eval_report": "", "report": f"No wiki article found for {filename}"}

        source_text = self._source_text(filename, article_path)
        if not source_text:
            return {"eval_report": "", "report": f"No source extracts found for {filename}"}

        system = load_prompt("eval-source.md")
        human = (
            f"## Source Text\n{source_text[:10000]}\n\n"
            f"## Wiki Article to Evaluate\n{article_path.read_text()}"
        )
        return {"eval_report": invoke(system, human, strong=True)}

    def save(self, state: EvalState) -> dict:
        eval_report = state_get(state, "eval_report", "")
        if not eval_report:
            return {}

        filename = state_get(state, "filename", "")
        stem = filename.rsplit(".", 1)[0]
        output_path = settings.outputs_dir / "evals" / f"eval-{stem}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(eval_report)

        return {"report": f"Eval saved to outputs/evals/eval-{stem}.md"}

    def _source_text(self, filename: str, article_path) -> str:
        if "summaries" in article_path.parts:
            return self.vault.read_extract(filename)

        article = self.vault.read_article(article_path)
        extracts = []
        for source in article.sources:
            text = self.vault.read_extract(source)
            if text:
                extracts.append(f"## {source}\n{text}")
        return "\n\n".join(extracts)
