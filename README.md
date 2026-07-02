# Lila

Operations intelligence for a pizza restaurant. An Obsidian vault with a multi-agent system that ingests supplier invoices, recipes, and operational data — then builds a wiki, runs fidelity checks, and generates analytics reports.

## Setup

Requires Python 3.11+.

```bash
# Clone and enter the repo
git clone <repo-url> && cd lila

# Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install with your LLM provider
pip install -e ".[anthropic]"
```

Other providers: `pip install -e ".[openai]"`, `".[google]"`, or `".[mistral]"`.

### Environment variables

Create a `.env` file or export directly:

```bash
# Required — pick your provider and set its API key
export KB_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Optional — override default models
export KB_MODEL=claude-sonnet-4-20250514
export KB_MODEL_STRONG=claude-opus-4-20250514
```

For OpenAI use `OPENAI_API_KEY`, for Google use `GOOGLE_API_KEY`, for Mistral use `MISTRAL_API_KEY`.

### Initialize the vault

```bash
lila init
```

Creates the full directory structure, prompt templates, and planning files. Run once.

## Commands

```bash
lila <command> [args]
```

### Core workflow

| Command | Description |
|---------|-------------|
| `init` | Scaffold vault structure and prompt templates |
| `catalog` | Scan `raw/suppliers/` for new files and extract metadata |
| `catalog-update` | Sync extracted/ingested flags in the catalog |
| `find <query>` | Search catalog by title, supplier, or keyword |
| `ingest <file>` | Summarize a source into the wiki (with fidelity check) |
| `ingest-all` | Ingest all unprocessed sources |
| `compile-ingredients` | Generate ingredient/concept articles from cross-referenced analyses |
| `synthesize <topic>` | Cross-source synthesis on a topic |
| `status` | Dashboard of sources, articles, and wiki health |

### Analysis & reports

| Command | Description |
|---------|-------------|
| `discounts` | Analyze "on the house" discount patterns from xlsx files and generate an interactive HTML report |
| `eval <file>` | Deep fidelity check of a wiki article against its sources |
| `eval-all` | Eval every wiki article, produce roll-up report |
| `lint` | Health check: broken links, orphans, stale articles, gaps |
| `query <question>` | Answer a question grounded in wiki content |
| `slides <topic>` | Generate a Marp slide deck from wiki content |

### Planning & references

| Command | Description |
|---------|-------------|
| `update-plan <name>` | Suggest updates to a planning doc based on wiki content |
| `references` | Build a citation network across vault sources |
| `suggest` | Rank external references not yet in the vault by frequency |
| `backfill-references` | Extract references from existing summaries |

### Utilities

| Command | Description |
|---------|-------------|
| `watch` | Watch `raw/suppliers/` and auto-ingest new files |
| `graph [agent]` | Print the Mermaid graph for any sub-agent |

## Discount analysis

Drop `.xlsx` files (exported from your POS) into `raw/discounts/` and run:

```bash
lila discounts
```

Generates an interactive HTML report at `outputs/reports/discount-report.html` with:

- **Metadata panel** — file count, date range, totals
- **Hourly breakdown** — discount count and amount by hour
- **Daily breakdown** — by day of week
- **By waiter** — top 15 waiters by discount amount
- **Top items** — most frequently discounted menu items
- **Discount types** — pie chart by definition/reason
- **Trend** — daily discount amounts over time
- **Heatmap** — day × hour matrix

Every chart has a collapsible data table underneath — click to expand the raw numbers.

## Workflow

1. Drop a supplier invoice or recipe into `raw/suppliers/`
2. `lila catalog` — registers it with title, supplier, keywords
3. `lila ingest <filename>` — extracts text, generates an analysis, runs fidelity check, saves to `wiki/analyses/`
4. `lila compile-ingredients` — creates standalone ingredient/concept articles from cross-referenced analyses
5. `lila synthesize <topic>` — produces a cross-source synthesis
6. `lila lint` — catches broken links, orphans, and contradictions

## Structure

```
raw/
  suppliers/    Source documents (invoices, specs). Human-curated, never auto-edited.
  recipes/      Recipe files and formulations.
  discounts/    POS discount export xlsx files for analysis.
  notes/        Your own rough notes and ideas.
  web/          Web-clipped articles.
wiki/
  analyses/     LLM-generated analyses of source documents.
  ingredients/  Standalone concept/ingredient articles.
  insights/     Cross-cutting themes and comparisons.
planning/       Operations planning docs (menu strategy, cost optimization).
prompts/        Prompt templates that drive generation quality.
outputs/
  reports/      Generated reports (including discount-report.html).
  evals/        Fidelity check reports.
  slides/       Marp slide decks.
  figures/      Generated charts and diagrams.
agents/         The multi-agent system (LangGraph + LangChain + Pydantic).
```

## Architecture

A supervisor routes each command to a specialized sub-agent. Each agent is a LangGraph `StateGraph` with typed Pydantic state.

The ingest agent has a fidelity retry loop: after generating an analysis, it evaluates every claim against the source and fixes distortions (up to 3 attempts) before saving.

The discount analysis pipeline uses pandas + plotly to generate interactive HTML reports from POS export data.

Provider-agnostic — swap between Anthropic, OpenAI, Google, or Mistral by changing one env var.
