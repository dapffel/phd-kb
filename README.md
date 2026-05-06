# phd-kb

Personal PhD knowledge base for species distribution modelling literature. An Obsidian vault with an automated multi-agent system that ingests papers, builds a wiki, and checks factual accuracy.

## Setup

Requires Python 3.11+.

```bash
# Clone and enter the repo
git clone <repo-url> && cd phd-kb

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
kb init
```

This creates the full directory structure, prompt templates, and starter files. Run once.

## Commands

```bash
kb <command> [args]
```

| Command | Description |
|---------|-------------|
| `init` | Scaffold vault structure and prompt templates |
| `catalog` | Scan `raw/papers/` for new PDFs and extract metadata |
| `catalog-update` | Sync extracted/ingested flags in the catalog |
| `find <query>` | Search catalog by title, author, or keyword |
| `ingest <file>` | Summarize a paper into the wiki (with fidelity check) |
| `ingest-all` | Ingest all unprocessed papers |
| `compile-concepts` | Generate concept articles from cross-referenced summaries |
| `synthesize <topic>` | Cross-source synthesis on a topic |
| `eval <file>` | Deep fidelity check of a wiki article against its sources |
| `eval-all` | Eval every wiki article, produce roll-up report |
| `lint` | Health check: broken links, orphans, stale articles, gaps |
| `query <question>` | Answer a question grounded in wiki content |
| `update-chapter <name>` | Suggest updates to a research chapter based on wiki |
| `slides <topic>` | Generate a Marp slide deck from wiki content |
| `status` | Dashboard of sources, articles, and wiki health |
| `watch` | Watch `raw/papers/` and auto-ingest new PDFs |

## Workflow

1. Drop a PDF into `raw/papers/`
2. `kb catalog` — registers it with title, authors, keywords
3. `kb ingest <filename>` — extracts text, generates a summary, runs fidelity check, saves to `wiki/summaries/`
4. `kb compile-concepts` — creates standalone concept articles from cross-referenced summaries
5. `kb synthesize <topic>` — produces a cross-source synthesis
6. `kb lint` — catches broken links, orphans, and contradictions

## Structure

```
raw/          Source materials (PDFs, notes, web clips). Human-curated, never auto-edited.
wiki/         LLM-generated summaries, concepts, connections, glossary. Never hand-edited.
research/     Your dissertation chapters. Collaborative — you write, agents suggest updates.
prompts/      Prompt templates that drive generation quality.
outputs/      Generated reports, evals, slides, figures.
agents/       The multi-agent system (LangGraph + LangChain + Pydantic).
```

## Architecture

A supervisor routes each command to a specialized sub-agent. Each agent is a LangGraph `StateGraph` with typed Pydantic state.

The ingest agent has a fidelity retry loop: after generating a summary, it evaluates every claim against the source and fixes distortions (up to 3 attempts) before saving.

Provider-agnostic — swap between Anthropic, OpenAI, Google, or Mistral by changing one env var.
