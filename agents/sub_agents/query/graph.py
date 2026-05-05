from langgraph.graph import StateGraph, END

from agents.llm import invoke, load_prompt
from agents.models import QueryState
from agents.state import state_get
from agents.sub_agents.base import BaseAgent


class QueryAgent(BaseAgent[QueryState]):
    state_schema = QueryState

    def build_graph(self) -> StateGraph:
        g = StateGraph(QueryState)
        g.add_node("gather", self.gather)
        g.add_node("answer", self.answer)
        g.set_entry_point("gather")
        g.add_edge("gather", "answer")
        g.add_edge("answer", END)
        return g

    def gather(self, state: QueryState) -> dict:
        question = state_get(state, "question", "").lower()
        all_files = (
            self.vault.list_summaries()
            + self.vault.list_concepts()
            + self.vault.list_connections()
        )

        relevant = []
        for path in all_files:
            content = path.read_text()
            words = question.split()
            if any(w in content.lower() for w in words if len(w) > 3):
                relevant.append(content)

        return {"context": relevant[:10]}

    def answer(self, state: QueryState) -> dict:
        system = load_prompt("query.md")
        context_items = state_get(state, "context", [])
        context = "\n---\n".join(context_items) if context_items else "(No relevant articles found)"
        human = (
            f"Question: {state_get(state, 'question', '')}\n\n"
            f"Wiki articles:\n\n{context}"
        )
        return {"answer": invoke(system, human, strong=True)}
