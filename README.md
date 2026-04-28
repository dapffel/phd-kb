# phd-kb

Personal PhD knowledge base for species distribution modelling literature. LLM-maintained wiki built as an Obsidian vault.

## Structure

- `raw/` — Source materials (paper extracts, notes, catalog). Human-curated, never auto-edited.
- `wiki/` — LLM-generated summaries, concept articles, cross-source syntheses, glossary. Never hand-edited.
- `research/` — Dissertation chapters (local-only, not tracked in git until graduated).
- `prompts/` — Prompt templates driving wiki generation and maintenance.
- `outputs/` — Generated reports, eval results, slides, figures.

## Commands

Managed via Claude Code using the workflows defined in `CLAUDE.md`:

- `ingest <file>` — Extract and summarise a paper into the wiki
- `compile-concepts` — Generate concept articles from cross-referenced summaries
- `synthesize <topic>` — Produce cross-source synthesis documents
- `eval <file>` — Fidelity-check a wiki article against its sources
- `lint` — Health check for broken links, orphans, contradictions
- `query <question>` — Answer questions grounded in wiki content
- `status` — Dashboard of wiki stats

## Current state

- 10 sources ingested
- 5 concept articles
- 1 cross-source synthesis
- 30 glossary terms
