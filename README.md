# phd-kb

> **This is a template repository.** Click **"Use this template"** above to create your own copy — you'll get a clean, independent repo with no shared history.

A structured Obsidian vault for managing PhD research literature. You add papers, tell your LLM to process them, and it builds an interlinked wiki of summaries, concepts, and cross-source syntheses — complete with citation tracking and reading suggestions.

The LLM follows instructions defined in `CLAUDE.md` and `AGENTS.md` — no custom code or plugins required. You can also optionally install a Python CLI (`kb`) for batch processing and automation.

New here? Start with [QUICKSTART.md](QUICKSTART.md) for the shortest first-paper workflow.

## What you need

- **Obsidian** (free) — for browsing and navigating the wiki
- **An LLM with filesystem access** — it needs to read your PDFs and write markdown files
- **Optional: Python 3.11+** — only needed if you want the `kb` CLI for automated pipelines

Tested with: **Claude Code**, **OpenAI Codex**, **Cursor**, **GitHub Copilot** (IDE). These can read/write local files directly.

> **Note:** Web-based tools (ChatGPT, Gemini web UI) cannot read local files or write to your vault. They won't work for this workflow.

## Setup

### 1. Create your repo

Click the green **"Use this template"** button at the top of this page, then clone it:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Install Obsidian

Download from [obsidian.md](https://obsidian.md/) (free, Mac/Windows/Linux).

Open Obsidian → **Open folder as vault** → select the repo folder.

### 3. Connect your LLM

**Claude Code (recommended)** — run `claude` in the repo root. It reads `CLAUDE.md` automatically.

**OpenAI Codex** — run `codex` in the repo root. It reads `AGENTS.md` automatically.

**Cursor / Copilot** — open the repo in your IDE. Point the AI assistant to `CLAUDE.md` as its instructions file.

### 4. Add your first paper

Rename your PDF to `authorYEAR-keyword.pdf` and drop it into `raw/papers/`:

```
raw/papers/smith2024-habitat-loss.pdf
```

PDFs are ignored by Git. Keep your source PDFs backed up in Zotero, Google Drive, Dropbox, or another storage system.

### 5. Ingest it

Tell your LLM (type this into the LLM chat, not your terminal):

```
ingest smith2024-habitat-loss.pdf
```

The LLM reads the PDF, generates a structured summary in `wiki/summaries/`, extracts the paper's reference list, runs a fidelity check against the source, and updates the catalog and index.

### 6. Build up the wiki

As you add more papers, ask the LLM to run these workflows:

```
catalog              — register new PDFs and extract metadata
ingest-all           — ingest everything that hasn't been processed yet
compile-concepts     — generate concept articles from cross-source themes
synthesize <topic>   — create a cross-source synthesis on a topic
lint                 — check wiki health (broken links, orphans, gaps)
status               — see where things stand
```

Stronger models are recommended for `ingest`, `eval`, and `synthesize`, because those workflows require careful source reading and fidelity checks.

## Commands

### Paper management

| Command | What it does |
|---------|-------------|
| `init` | Create the vault directory structure and starter files |
| `catalog` | Scan `raw/papers/` for new PDFs, extract metadata |
| `catalog-update` | Refresh extracted/ingested flags from disk |
| `find <query>` | Search the catalog by title, author, or keyword |
| `ingest <file>` | Process a paper: extract text, summarize, extract references, fidelity check |
| `ingest-all` | Ingest all unprocessed papers and web clips |

### Wiki building

| Command | What it does |
|---------|-------------|
| `compile-concepts` | Generate concept articles from cross-source themes |
| `synthesize <topic>` | Create a cross-source synthesis document |
| `query <question>` | Answer a question using wiki content, with source citations |
| `slides <topic>` | Generate a Marp slide deck from wiki content |

### Citation network

| Command | What it does |
|---------|-------------|
| `references` | Build a citation network across all vault papers, saved to `wiki/connections/citation-network.md` |
| `suggest` | Rank frequently-cited papers not yet in your vault — a reading list based on what your sources reference |
| `backfill-references` | Extract reference lists for existing summaries that were ingested before reference tracking was added |

### Quality and maintenance

| Command | What it does |
|---------|-------------|
| `eval <file>` | Deep fidelity check: verify every claim against the original source |
| `eval-all` | Evaluate all wiki articles, produce a roll-up report with fidelity % and error breakdown |
| `lint` | Health check: broken links, orphans, contradictions, gaps, stale content |
| `status` | Dashboard: source counts, article counts, word count, broken links |
| `update-chapter <name>` | Suggest updates to a research chapter based on new wiki content |

### CLI-only

| Command | What it does |
|---------|-------------|
| `graph <agent>` | Print a Mermaid diagram of an agent's pipeline (e.g., `kb graph ingest`) |
| `--dry-run` | Preview what a bulk command would do without running it (e.g., `kb ingest-all --dry-run`) |

## CLI installation

If you prefer shell commands over LLM prompts, install the agent system:

```bash
pip install -e ".[anthropic]"   # or .[openai], .[google], .[mistral]
```

Then use the `kb` CLI directly:

```bash
kb catalog
kb ingest smith2024-habitat-loss.pdf
kb ingest-all
kb compile-concepts
kb references
kb suggest
kb status
kb graph ingest
```

### Configuration

The CLI uses environment variables prefixed with `KB_`:

```bash
export KB_PROVIDER=anthropic     # or openai, google, mistral
export KB_MODEL=claude-sonnet-4-20250514
```

For LangSmith tracing (optional):

```bash
export KB_LANGSMITH_TRACING=true
export KB_LANGSMITH_API_KEY=your-key-here
export KB_LANGSMITH_PROJECT=phd-kb
```

## Structure

```
phd-kb/
├── raw/papers/        — your PDFs and their extracted text
├── raw/notes/         — your own rough notes
├── raw/web/           — web-clipped articles
├── wiki/summaries/    — one summary per source (LLM-generated)
├── wiki/concepts/     — standalone concept articles (LLM-generated)
├── wiki/connections/  — cross-source syntheses and citation network
├── research/          — your dissertation chapters (Git-ignored until ready)
├── research/templates — starter chapter templates
├── prompts/           — prompt templates driving generation
├── outputs/           — reports, evals, slides
├── agents/            — LangGraph agent system (kb CLI)
└── tests/             — test suite (62 tests)
```

## Conventions

- **Filenames**: `authorYEAR-keyword` for papers, lowercase-hyphenated for concepts
- **Wikilinks**: `[[concept-name]]` — always lowercase-hyphenated, filename without extension
- **Frontmatter**: every wiki article has YAML with `title`, `type`, `sources`, `created`, `updated`
- **References**: summaries include a `references:` list in frontmatter (author, year, title) for citation tracking
- **raw/** is yours — the LLM reads from it but never edits it
- **wiki/** is the LLM's — never hand-edit, regenerate instead
- **research/** is yours — chapter drafts are Git-ignored until you choose to track them; starter templates live in `research/templates/`

## Limitations

- Results depend on the LLM you use. Stronger models produce better summaries and more reliable fidelity checks.
- `CLAUDE.md` is long. LLMs with small context windows may not follow all instructions consistently.
- PDF extraction quality varies — scanned PDFs or complex layouts may need manual cleanup.
- Citation matching uses first-author surname + year, which works well for small-to-medium vaults but may produce false matches in very large collections.
- Web chat tools that require uploading documents may create privacy or copyright concerns. Prefer local filesystem agents when working with copyrighted papers.

## Full specification

See `CLAUDE.md` for the complete workflow definitions, output formats, and rules. `AGENTS.md` is included for tools that look for that filename.
