from langgraph.graph import StateGraph, END

from agents.llm import invoke, load_prompt
from agents.models import SynthesizeState
from agents.sub_agents.base import BaseAgent


class SynthesizeAgent(BaseAgent[SynthesizeState]):
    state_schema = SynthesizeState

    def build_graph(self) -> StateGraph:
        g = StateGraph(SynthesizeState)
        g.add_node("gather", self.gather)
        g.add_node("synthesize", self.synthesize)
        g.add_node("save", self.save)
        g.set_entry_point("gather")
        g.add_edge("gather", "synthesize")
        g.add_edge("synthesize", "save")
        g.add_edge("save", END)
        return g

    def gather(self, state: SynthesizeState) -> dict:
        topic = state.topic
        all_files = (
            self.vault.list_summaries()
            + self.vault.list_concepts()
            + self.vault.list_connections()
        )

        relevant = [
            path.read_text() for path in all_files
            if topic.lower() in path.read_text().lower() or topic.lower() in path.stem.lower()
        ]
        return {"relevant_articles": relevant}

    def synthesize(self, state: SynthesizeState) -> dict:
        system = load_prompt("synthesize.md")
        human = (
            f"Topic: {state.topic}\n\n"
            f"Relevant wiki articles:\n\n"
            + "\n---\n".join(state.relevant_articles)
        )
        return {"synthesis": invoke(system, human, strong=True)}

    def save(self, state: SynthesizeState) -> dict:
        topic_slug = state.topic.lower().replace(" ", "-")
        self.vault.save_article("connections", f"{topic_slug}.md", state.synthesis)
        self.vault.regenerate_wiki_index()

        count = len(state.relevant_articles)
        return {"report": f"Synthesized {count} articles on '{state.topic}'. Saved to wiki/connections/{topic_slug}.md"}
