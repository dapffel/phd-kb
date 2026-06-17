# Changelog

This file tracks notable changes to the template. If you created your repo from an earlier version and want to pull in new features, follow the upgrade instructions for each release.

---

## v0.3.0 — 2026-06-17

### What's new

- **Citation tracking** — `kb ingest` now extracts the reference list from each paper and stores it in the summary's YAML frontmatter.
- **`kb references`** — builds a citation network across all vault papers and saves it to `wiki/connections/citation-network.md`. Shows which papers cite each other and ranks the most-cited.
- **`kb suggest`** — ranks papers frequently cited by your sources but not yet in your vault. A data-driven reading list.
- **`kb backfill-references`** — one-time command to extract references from summaries that were ingested before citation tracking existed.
- **Vault explorer notebook** (`explore.ipynb`) — interactive data exploration with networkx and matplotlib: wikilink graph, citation network, concept co-occurrence, publication timeline, keyword distribution, coverage gaps. No LLM calls needed.
- **`kb graph <agent>`** — prints a Mermaid diagram of any agent's pipeline (e.g., `kb graph ingest`).
- **`--dry-run` flag** — preview what bulk commands would do without running them (e.g., `kb ingest-all --dry-run`).
- **LangSmith tracing** — optional integration via `KB_LANGSMITH_TRACING=true`.
- **Vault file caching** — repeated reads are cached in memory, improving performance for commands that scan the whole wiki.
- **Improved `kb eval-all`** — generates a roll-up report with overall fidelity %, error type breakdown, and per-article table sorted by issue count.
- **Query save prompt** — after `kb query`, the CLI suggests saving the answer to wiki or outputs.

### How to upgrade

If your repo was created from an earlier version of this template:

**1. Add the template as a remote**

```bash
git remote add template https://github.com/dapffel/phd-kb.git
git fetch template
```

**2. Copy the updated agent system**

```bash
# overwrite agents/, tests/, and supporting files with the latest versions
git checkout template/template -- agents/ tests/ pyproject.toml prompts/extract-references.md explore.ipynb
```

**3. Reinstall**

```bash
pip install -e ".[anthropic]"   # or your provider
```

**4. Backfill references for existing summaries**

```bash
kb backfill-references
kb references
```

**5. Review and commit**

```bash
git diff --staged   # review what changed
git commit -m "chore: upgrade agents to template v0.3.0"
```

### Files changed

| Path | Action |
|------|--------|
| `agents/models.py` | Added `Reference` model, extended `IngestState` and `IngestResult` |
| `agents/sub_agents/ingest/graph.py` | Added `extract_references` node, frontmatter injection in save |
| `agents/commands.py` | Added `build_citation_network`, `suggest_reading`, `backfill_references`, `match_reference_to_catalog` |
| `agents/supervisor/graph.py` | Added `references`, `suggest`, `backfill-references` routes; improved `eval-all` roll-up |
| `agents/main.py` | Added `graph` command, `--dry-run` parsing, LangSmith tracing, updated help text |
| `agents/config.py` | Added LangSmith settings |
| `agents/vault.py` | Added file read cache |
| `prompts/extract-references.md` | **New** — prompt for extracting bibliography as JSON |
| `explore.ipynb` | **New** — vault explorer notebook |
| `tests/` | Extended to 62 tests covering references, citation matching, fidelity parsing |
| `pyproject.toml` | Added `tracing` optional dependency |

---

## v0.2.0 — 2026-06-08

### What's new

- **LangGraph agent system** — full CLI (`kb`) with supervisor routing to specialized sub-agents for ingest, catalog, compile-concepts, synthesize, eval, lint, query, and status.
- **Multi-provider support** — configure via `KB_PROVIDER` env var: anthropic, openai, google, or mistral.
- **Fidelity checking** — `kb ingest` automatically verifies every claim in the generated summary against the source, with retry loop (up to 3 attempts).
- **`kb eval` / `kb eval-all`** — deep factual accuracy checks against original sources.
- **`kb lint`** — wiki health checks: broken links, orphans, contradictions, stale content.
- **`kb slides <topic>`** — generate Marp slide decks from wiki content.
- **Test suite** — pytest-based tests for models, vault operations, ingest pipeline, and commands.

### How to upgrade

If your repo was created from v0.1.0 (prompt-only, no agents):

```bash
git remote add template https://github.com/dapffel/phd-kb.git
git fetch template
git checkout template/template -- agents/ tests/ pyproject.toml
pip install -e ".[anthropic]"
kb status   # verify it works
git add agents/ tests/ pyproject.toml
git commit -m "chore: add agent system from template v0.2.0"
```

Your existing wiki, raw files, and prompts are untouched.

---

## v0.1.0 — 2026-04-25

### Initial release

- Obsidian vault structure with `raw/`, `wiki/`, `research/`, `prompts/`, `outputs/`.
- `CLAUDE.md` with full workflow definitions for LLM-driven ingestion, compilation, synthesis, and evaluation.
- Prompt templates for all workflows.
- Research chapter templates in `research/templates/`.
- Git workflow with commit conventions and `.gitignore` for PDFs and research drafts.
