import pytest
from agents.llm import load_prompt, LLMError


class TestLoadPrompt:
    def test_loads_existing(self, vault):
        content = load_prompt("compile-source.md")
        assert "Prompt template stub" in content

    def test_missing_raises(self, vault):
        with pytest.raises(LLMError, match="not found"):
            load_prompt("nonexistent-prompt.md")
