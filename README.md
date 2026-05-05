# phd-kb

LLM-maintained research knowledge base built as an Obsidian vault. Drop PDFs, tell your LLM to ingest them, and it builds a structured, interlinked wiki of your literature.

Works with any LLM: Claude Code, ChatGPT, Gemini, Cursor, Copilot, or any tool that can read files and follow instructions.

## Setup

### 1. Clone the repo

```bash
git clone -b template https://github.com/dapffel/phd-kb.git
cd phd-kb
```

### 2. Install Obsidian

Download from [obsidian.md](https://obsidian.md/) (free, Mac/Windows/Linux).

Open Obsidian, click **Open folder as vault**, and select the `phd-kb` folder.

### 3. Connect your LLM

**Option A — Claude Code (recommended)**

Install Claude Code and run it in the repo root. It reads `CLAUDE.md` automatically.

```bash
claude
```

**Option B — Any other LLM**

Paste the contents of `CLAUDE.md` as system context in your tool (ChatGPT, Gemini, Cursor, etc.). The file contains the full specification — commands, formats, and rules.

### 4. Add your first paper

Rename your PDF to the format `authorYEAR-keyword.pdf` and drop it into `raw/papers/`:

```
raw/papers/smith2024-habitat-loss.pdf
```

### 5. Ingest it

Tell your LLM:

```
ingest smith2024-habitat-loss.pdf
```

It will extract the text, generate a structured summary in `wiki/summaries/`, run a fidelity check against the source, and update the catalog and index.

### 6. Build up the wiki

As you add more papers, use these commands to grow the knowledge base:

```
catalog              — register new PDFs and extract metadata
ingest-all           — ingest everything that hasn't been processed yet
compile-concepts     — generate concept articles from cross-source themes
synthesize <topic>   — create a cross-source synthesis on a topic
lint                 — check wiki health (broken links, orphans, gaps)
status               — see where things stand
```

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

## Full specification

See `CLAUDE.md` for the complete command reference, output formats, and rules.
