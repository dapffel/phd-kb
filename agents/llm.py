import importlib

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from agents.config import settings

PROVIDERS = {
    "anthropic": ("langchain_anthropic", "ChatAnthropic"),
    "openai": ("langchain_openai", "ChatOpenAI"),
    "google": ("langchain_google_genai", "ChatGoogleGenerativeAI"),
    "mistral": ("langchain_mistralai", "ChatMistralAI"),
}


def get_llm(strong: bool = False) -> BaseChatModel:
    model = settings.model_strong if strong else settings.model
    module_name, class_name = PROVIDERS[settings.provider]
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls(model=model, temperature=settings.temperature, max_tokens=settings.max_tokens)


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
