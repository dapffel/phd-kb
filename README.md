# phd-kb

A structured Obsidian vault for managing PhD research literature. You add papers, tell your LLM to process them, and it builds an interlinked wiki of summaries, concepts, and cross-source syntheses.

The LLM follows instructions defined in `CLAUDE.md` — no custom code or plugins required.

## What you need

- **Obsidian** (free) — for browsing and navigating the wiki
- **An LLM with filesystem access** — it needs to read your PDFs and write markdown files

Tested with: **Claude Code**, **Cursor**, **GitHub Copilot** (IDE). These can read/write local files directly.

> **Note:** Web-based tools (ChatGPT, Gemini web UI) cannot read local files or write to your vault. They won't work for this workflow.

## Setup

### 1. Clone the repo

```bash
git clone -b template https://github.com/dapffel/phd-kb.git
cd phd-kb
```

### 2. Install Obsidian

Download from [obsidian.md](https://obsidian.md/) (free, Mac/Windows/Linux).

Open Obsidian → **Open folder as vault** → select the `phd-kb` folder.

### 3. Connect your LLM

**Claude Code (recommended)** — run `claude` in the repo root. It reads `CLAUDE.md` automatically.

**Cursor / Copilot** — open the repo in your IDE. Point the AI assistant to `CLAUDE.md` as its instructions file.

### 4. Add your first paper

Rename your PDF to `authorYEAR-keyword.pdf` and drop it into `raw/papers/`:

```
raw/papers/smith2024-habitat-loss.pdf
```

### 5. Ingest it

Tell your LLM:

```
ingest smith2024-habitat-loss.pdf
```

The LLM will read the PDF, generate a structured summary in `wiki/summaries/`, and update the catalog and index. The quality depends on the LLM and how well it follows the instructions in `CLAUDE.md`.

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

These are not CLI commands — they are instructions the LLM understands from `CLAUDE.md`. Type them as prompts to your LLM.

## Structure

```
phd-kb/
├── raw/papers/        — your PDFs and their extracted text
├── raw/notes/         — your own rough notes
├── wiki/summaries/    — one summary per source (LLM-generated)
├── wiki/concepts/     — standalone concept articles (LLM-generated)
├── wiki/connections/  — cross-source syntheses (LLM-generated)
├── research/          — your dissertation chapters (yours to write)
├── prompts/           — prompt templates (the logic driving generation)
└── outputs/           — reports, evals, slides
```

## Conventions

- **Filenames**: `authorYEAR-keyword` for papers, lowercase-hyphenated for concepts
- **Wikilinks**: `[[concept-name]]` — always lowercase-hyphenated
- **Frontmatter**: every wiki article has YAML with `title`, `type`, `sources`, `created`, `updated`
- **raw/** is yours — the LLM reads from it but never edits it
- **wiki/** is the LLM's — never hand-edit, regenerate instead

## Limitations

- Results depend on the LLM you use. Stronger models produce better summaries and more reliable fidelity checks.
- `CLAUDE.md` is long. LLMs with small context windows may not follow all instructions consistently.
- PDF extraction quality varies — scanned PDFs or complex layouts may need manual cleanup.

## Full specification

See `CLAUDE.md` for the complete workflow definitions, output formats, and rules.
