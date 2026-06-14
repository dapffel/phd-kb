from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from langgraph.graph import StateGraph

from agents.vault import Vault

StateT = TypeVar("StateT", bound=BaseModel)


class BaseAgent(ABC, Generic[StateT]):
    state_schema: type[StateT]

    def __init__(self, vault: Vault | None = None):
        self.vault = vault or Vault()

    @abstractmethod
    def build_graph(self) -> StateGraph:
        ...

    def run(self, input_state: StateT | None = None) -> StateT:
        graph = self.build_graph().compile()
        data = input_state.model_dump() if input_state else {}
        result = graph.invoke(data)
        return self.state_schema.model_validate(result)
