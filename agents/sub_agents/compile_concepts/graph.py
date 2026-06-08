import re

from langgraph.graph import StateGraph, END

from agents.llm import invoke, load_prompt
from agents.models import CompileState
from agents.sub_agents.base import BaseAgent


class CompileConceptsAgent(BaseAgent[CompileState]):
    state_schema = CompileState

    def build_graph(self) -> StateGraph:
        g = StateGraph(CompileState)
        g.add_node("detect", self.detect)
        g.add_node("generate", self.generate)
        g.add_node("update_index", self.update_index)
        g.set_entry_point("detect")
        g.add_edge("detect", "generate")
        g.add_edge("generate", "update_index")
        g.add_edge("update_index", END)
        return g

    def detect(self, state: CompileState) -> dict:
        summaries = self.vault.list_summaries()
        concept_counts: dict[str, int] = {}

        for path in summaries:
            links = re.findall(r"\[\[([^\]]+)\]\]", path.read_text())
            for link in links:
                concept_counts[link] = concept_counts.get(link, 0) + 1

        existing = {f.stem for f in self.vault.list_concepts()}
        existing_summaries = {f.stem for f in summaries}

        candidates = [
            name for name, count in concept_counts.items()
            if count >= 2 and name not in existing and name not in existing_summaries
        ]
        return {"concept_names": sorted(candidates)}

    def generate(self, state: CompileState) -> dict:
        system = load_prompt("write-concept.md")
        summaries = self.vault.list_summaries()
        created = []

        summary_contents = [(path, path.read_text()) for path in summaries]
        for concept in state.concept_names:
            relevant = [
                content for path, content in summary_contents
                if f"[[{concept}]]" in content
            ]
            if not relevant:
                continue

            human = (
                f"Concept: {concept}\n\n"
                f"Source summaries that discuss this concept:\n\n"
                + "\n---\n".join(relevant)
            )
            article = invoke(system, human, strong=True)
            self.vault.save_article("concepts", f"{concept}.md", article)
            created.append(concept)

        return {"created": created, "updated": []}

    def update_index(self, state: CompileState) -> dict:
        self.vault.regenerate_wiki_index()
        self.vault.regenerate_glossary()

        created = state.created
        updated = state.updated
        stats = self.vault.stats()
        report = (
            f"Created {len(created)} concepts, updated {len(updated)}. "
            f"Wiki: {stats.summaries} summaries, {stats.concepts} concepts, "
            f"{stats.connections} connections, {stats.total_words:,} words."
        )
        return {"report": report}
