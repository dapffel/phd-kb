from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

from agents.config import settings


def get_llm(strong: bool = False) -> ChatAnthropic:
    model = settings.model_strong if strong else settings.model
    return ChatAnthropic(
        model=model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )


def load_prompt(name: str) -> str:
    path = settings.prompts_dir / name
    return path.read_text()


def invoke(system: str, human: str, strong: bool = False) -> str:
    llm = get_llm(strong=strong)
    response = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=human),
    ])
    return response.content
