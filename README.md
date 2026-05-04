# phd-kb

LLM-maintained research knowledge base built as an Obsidian vault. Drop PDFs into `raw/papers/`, and Claude Code turns them into a structured, interlinked wiki.

## Getting Started

1. Clone this repo
2. Open the folder in Obsidian
3. Install [Claude Code](https://claude.ai/code) and run it in the repo root
4. Drop a PDF into `raw/papers/`
5. Tell Claude Code: `ingest <filename>`

Claude Code reads `CLAUDE.md` automatically and knows all the commands.

## Structure

- `raw/` — Your source materials (papers, notes, web clips). Human-curated, never auto-edited.
- `wiki/` — LLM-generated summaries, concept articles, syntheses, glossary. Never hand-edited.
- `research/` — Your dissertation chapters (local-only until you choose to track them).
- `prompts/` — Prompt templates that drive wiki generation.
- `outputs/` — Generated reports, eval results, slides.

## Commands

Run these in Claude Code:

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

## Conventions

- **Filenames**: `authorYEAR-keyword` for papers (e.g., `vaswani2017-attention.pdf`), lowercase-hyphenated for concepts
- **Wikilinks**: `[[concept-name]]` — always lowercase-hyphenated, consistent across the wiki
- **Frontmatter**: every wiki article has YAML frontmatter with `title`, `type`, `sources`, `created`, `updated`

See `CLAUDE.md` for the full specification.
