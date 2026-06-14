# phd-kb

> **This is a template repository.** Click **"Use this template"** above to create your own copy — you'll get a clean, independent repo with no shared history.

A structured Obsidian vault for managing PhD research literature. You add papers, tell your LLM to process them, and it builds an interlinked wiki of summaries, concepts, and cross-source syntheses.

The LLM follows instructions defined in `CLAUDE.md` and `AGENTS.md` — no custom code or plugins required. Power users can optionally install a Python CLI (`kb`) for batch processing and automation.

New here? Start with [QUICKSTART.md](QUICKSTART.md) for the shortest first-paper workflow.

## What you need

- **Obsidian** (free) — for browsing and navigating the wiki
- **An LLM with filesystem access** — it needs to read your PDFs and write markdown files
- **Optional: Python 3.11+** — only needed if you want the `kb` CLI for automated pipelines

Tested with: **Claude Code**, **OpenAI Codex**, **Cursor**, **GitHub Copilot** (IDE). These can read/write local files directly.

> **Note:** Web-based tools (ChatGPT, Gemini web UI) cannot read local files or write to your vault. They won't work for this workflow.

## Setup

### 1. Create your repo

Click the green **"Use this template"** button at the top of this page → **"Create a new repository"**. Name it whatever you like (e.g., `my-phd-kb`), then clone it:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Install Obsidian

Download from [obsidian.md](https://obsidian.md/) (free, Mac/Windows/Linux).

Open Obsidian → **Open folder as vault** → select the `phd-kb` folder.

### 3. Connect your LLM

**Claude Code (recommended)** — run `claude` in the repo root. It reads `CLAUDE.md` automatically.

**OpenAI Codex** — run `codex` in the repo root. It reads `AGENTS.md` automatically; `AGENTS.md` points it to the same canonical instructions.

**Cursor / Copilot** — open the repo in your IDE. Point the AI assistant to `CLAUDE.md` as its instructions file.

### 4. Add your first paper

Rename your PDF to `authorYEAR-keyword.pdf` and drop it into `raw/papers/`:

```
raw/papers/smith2024-habitat-loss.pdf
```

PDFs are ignored by Git. Keep your source PDFs backed up in Zotero, Google Drive, Dropbox, OneDrive, or another storage system. This repo tracks the lightweight extracted `.md` text and generated wiki, not the large source PDFs.

### 5. Ingest it

Tell your LLM by typing this into the LLM chat or agent prompt, not into your terminal:

```
ingest smith2024-habitat-loss.pdf
```

The LLM will read the PDF, generate a structured summary in `wiki/summaries/`, and update the catalog and index. The quality depends on the LLM and how well it follows the instructions in `CLAUDE.md`.

### 6. Build up the wiki

As you add more papers, ask the LLM to run these workflows. These are prompts for the LLM, not shell commands:

```
catalog              — register new PDFs and extract metadata
ingest-all           — ingest everything that hasn't been processed yet
compile-concepts     — generate concept articles from cross-source themes
synthesize <topic>   — create a cross-source synthesis on a topic
lint                 — check wiki health (broken links, orphans, gaps)
status               — see where things stand
```

Stronger models are recommended for `ingest`, `eval`, and `synthesize`, because those workflows require careful source reading and fidelity checks.

### Alternative: CLI-based workflow (power users)

If you prefer shell commands over LLM prompts, install the agent system:

```bash
pip install -e ".[anthropic]"   # or .[openai], .[google], .[mistral]
```

Then use the `kb` CLI directly in your terminal:

```bash
kb catalog
kb ingest smith2024-habitat-loss.pdf
kb ingest-all
kb compile-concepts
kb synthesize "habitat loss"
kb status
kb lint
kb graph ingest              # print agent DAG as Mermaid diagram
```

The CLI runs the same pipelines as the prompt-based workflow. Configure the LLM provider via environment variables:

```bash
export KB_PROVIDER=anthropic     # or openai, google, mistral
export KB_MODEL=claude-sonnet-4-20250514
```

See `CLAUDE.md` for the full command reference.

## Structure

```
phd-kb/
├── raw/papers/        — your PDFs and their extracted text
├── raw/notes/         — your own rough notes
├── wiki/summaries/    — one summary per source (LLM-generated)
├── wiki/concepts/     — standalone concept articles (LLM-generated)
├── wiki/connections/  — cross-source syntheses (LLM-generated)
├── research/          — your dissertation chapters and tracked templates
├── prompts/           — prompt templates (the logic driving generation)
├── outputs/           — reports, evals, slides
├── agents/            — optional: LangGraph agent system (kb CLI)
└── tests/             — optional: test suite for agents/
```

Each major folder includes a short `README.md` explaining what belongs there.

## Conventions

- **Filenames**: `authorYEAR-keyword` for papers, lowercase-hyphenated for concepts
- **Wikilinks**: `[[concept-name]]` — always lowercase-hyphenated
- **Frontmatter**: every wiki article has YAML with `title`, `type`, `sources`, `created`, `updated`
- **raw/** is yours — the LLM reads from it but never edits it
- **wiki/** is the LLM's — never hand-edit, regenerate instead
- **research/** is yours — chapter drafts are ignored by Git until you choose to track them; starter templates live in `research/templates/`

## Limitations

- Results depend on the LLM you use. Stronger models produce better summaries and more reliable fidelity checks.
- `CLAUDE.md` is long. LLMs with small context windows may not follow all instructions consistently.
- PDF extraction quality varies — scanned PDFs or complex layouts may need manual cleanup.
- Web chat tools that require uploading documents may create privacy or copyright concerns. Prefer local filesystem agents when working with copyrighted papers.

## Full specification

See `CLAUDE.md` for the complete workflow definitions, output formats, and rules. `AGENTS.md` is included for tools that look for that filename.
