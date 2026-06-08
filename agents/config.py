from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    vault_root: Path = Path(__file__).parent.parent
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-20250514"
    model_strong: str = "claude-opus-4-20250514"
    temperature: float = 0.0
    max_tokens: int = 8192
    max_fidelity_attempts: int = 3

    @property
    def raw_dir(self) -> Path:
        return self.vault_root / "raw"

    @property
    def papers_dir(self) -> Path:
        return self.raw_dir / "papers"

    @property
    def web_dir(self) -> Path:
        return self.raw_dir / "web"

    @property
    def wiki_dir(self) -> Path:
        return self.vault_root / "wiki"

    @property
    def prompts_dir(self) -> Path:
        return self.vault_root / "prompts"

    @property
    def outputs_dir(self) -> Path:
        return self.vault_root / "outputs"

    @property
    def catalog_json(self) -> Path:
        return self.raw_dir / "_catalog.json"

    @property
    def catalog_md(self) -> Path:
        return self.raw_dir / "_catalog.md"

    @property
    def wiki_index(self) -> Path:
        return self.wiki_dir / "_index.md"

    @property
    def wiki_sources(self) -> Path:
        return self.wiki_dir / "_sources.md"

    @property
    def wiki_glossary(self) -> Path:
        return self.wiki_dir / "_glossary.md"

    model_config = {"env_prefix": "KB_", "protected_namespaces": ()}


settings = Settings()
