# phd-kb

Personal PhD knowledge base for species distribution modelling literature. LLM-maintained wiki built as an Obsidian vault, with an automated multi-agent system for ingestion and maintenance.

## Structure

- `raw/` — Source materials (paper extracts, notes, catalog). Human-curated, never auto-edited.
- `wiki/` — LLM-generated summaries, concept articles, cross-source syntheses, glossary. Never hand-edited.
- `research/` — Dissertation chapters (local-only, not tracked in git until graduated).
- `prompts/` — Prompt templates driving wiki generation and maintenance.
- `outputs/` — Generated reports, eval results, slides, figures.
- `agents/` — LangGraph multi-agent system that automates the workflows below.

## Usage

Run via CLI:

```
kb <command> [args]
```

| Command | What it does |
|---------|-------------|
| `ingest <file>` | Extract a paper and summarise it into the wiki, with fidelity checking |
| `ingest-all` | Ingest all unprocessed papers |
| `catalog` | Scan `raw/papers/` for new PDFs and extract metadata |
| `compile-concepts` | Generate concept articles from cross-referenced summaries |
| `synthesize <topic>` | Produce a cross-source synthesis document |
| `eval <file>` | Fidelity-check a wiki article against its original sources |
| `lint` | Health check for broken links, orphans, missing concepts |
| `query <question>` | Answer a question grounded in wiki content |
| `status` | Dashboard of sources, articles, and wiki health |
| `watch` | Watch `raw/papers/` and auto-ingest new PDFs |

## Agents

Built with LangGraph, LangChain, and Pydantic. A supervisor routes commands to specialized sub-agents, each defined as a `StateGraph` with typed Pydantic state.

The ingest agent includes a fidelity retry loop: after generating a summary, it evaluates every claim against the source and fixes distortions before saving.

## Setup

```
pip install -e .
```

Requires `ANTHROPIC_API_KEY` in environment.
