import importlib
import time
import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from agents.config import settings

logger = logging.getLogger(__name__)

PROVIDERS = {
    "anthropic": ("langchain_anthropic", "ChatAnthropic"),
    "openai": ("langchain_openai", "ChatOpenAI"),
    "google": ("langchain_google_genai", "ChatGoogleGenerativeAI"),
    "mistral": ("langchain_mistralai", "ChatMistralAI"),
}


class LLMError(Exception):
    pass


def get_llm(strong: bool = False) -> BaseChatModel:
    model = settings.model_strong if strong else settings.model
    provider = settings.provider
    if provider not in PROVIDERS:
        raise LLMError(f"Unknown provider: {provider}. Choose from: {', '.join(PROVIDERS)}")
    module_name, class_name = PROVIDERS[provider]
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise LLMError(
            f"Provider package '{module_name}' not installed. "
            f"Run: pip install phd-kb-agents[{provider}]"
        )
    cls = getattr(module, class_name)
    return cls(model=model, temperature=settings.temperature, max_tokens=settings.max_tokens)


def load_prompt(name: str) -> str:
    path = settings.prompts_dir / name
    if not path.exists():
        raise LLMError(f"Prompt template not found: {path}. Run `kb init` to regenerate.")
    return path.read_text()


def invoke(system: str, human: str, strong: bool = False, max_retries: int = 3) -> str:
    llm = get_llm(strong=strong)
    messages = [SystemMessage(content=system), HumanMessage(content=human)]

    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            response = llm.invoke(messages)
            content = response.content
            if not content or not content.strip():
                raise LLMError("LLM returned empty response")
            return content
        except LLMError:
            raise
        except Exception as e:
            last_error = e
            error_str = str(e).lower()
            is_retryable = any(k in error_str for k in ("rate", "limit", "timeout", "overloaded", "529", "503"))
            if not is_retryable or attempt == max_retries:
                break
            wait = 2 ** attempt
            logger.warning("LLM call failed (attempt %d/%d), retrying in %ds: %s", attempt, max_retries, wait, e)
            time.sleep(wait)

    raise LLMError(f"LLM call failed after {max_retries} attempts: {last_error}")
