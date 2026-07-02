import json
from pathlib import Path
from unittest import mock

import pytest


@pytest.fixture
def tmp_vault(tmp_path):
    """Create a minimal vault structure for testing."""
    dirs = [
        "raw/suppliers", "raw/recipes", "raw/notes", "raw/web", "raw/images",
        "wiki/analyses", "wiki/ingredients", "wiki/insights",
        "planning", "outputs/reports", "outputs/evals",
        "outputs/slides", "outputs/figures", "prompts",
    ]
    for d in dirs:
        (tmp_path / d).mkdir(parents=True)

    (tmp_path / "raw" / "_catalog.json").write_text("[]")
    (tmp_path / "wiki" / "_index.md").write_text("---\ntitle: Wiki Index\n---\n")
    (tmp_path / "wiki" / "_sources.md").write_text("---\ntitle: Sources\n---\n")
    (tmp_path / "wiki" / "_glossary.md").write_text("---\ntitle: Glossary\n---\n")

    for name in ["compile-source.md", "write-concept.md", "lint-wiki.md",
                  "query.md", "update-chapter.md", "synthesize.md", "eval-source.md"]:
        (tmp_path / "prompts" / name).write_text(f"# {name}\nPrompt template stub.")

    return tmp_path


@pytest.fixture
def vault(tmp_vault):
    from agents.config import Settings
    from agents.vault import Vault

    s = Settings(vault_root=tmp_vault)
    v = Vault(root=tmp_vault)

    with mock.patch("agents.config.settings", s), \
         mock.patch("agents.vault.settings", s), \
         mock.patch("agents.llm.settings", s), \
         mock.patch("agents.commands.settings", s):
        yield v


@pytest.fixture
def sample_catalog_entries():
    from agents.models import CatalogEntry
    return [
        CatalogEntry(
            filename="smith2020-attention.pdf",
            title="Attention in Ecology",
            authors=["Smith", "Jones"],
            year=2020,
            keywords=["attention", "ecology", "niche"],
            extracted=True,
            ingested=True,
        ),
        CatalogEntry(
            filename="doe2021-climate.pdf",
            title="Climate Impacts",
            authors=["Doe"],
            year=2021,
            keywords=["climate", "change"],
            extracted=True,
            ingested=False,
        ),
        CatalogEntry(
            filename="new2022-unprocessed.pdf",
            title="New Paper",
            authors=["New"],
            year=2022,
            keywords=["novel"],
            extracted=False,
            ingested=False,
        ),
    ]
