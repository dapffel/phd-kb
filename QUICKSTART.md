# Quickstart

This is the shortest path from an empty template repo to your first wiki article.

## 1. Open the Vault

Open this folder in Obsidian with **Open folder as vault**.

## 2. Start Your Local LLM Agent

Use a tool that can read and write local files:

- Claude Code: run `claude` in the repo root.
- OpenAI Codex: run `codex` in the repo root.
- Cursor or Copilot: open this repo in your IDE and point the assistant to `CLAUDE.md`.

The commands below are prompts for the LLM agent. Do not type them into your terminal.

## 3. Add a Paper

Rename a PDF with the pattern `authorYEAR-keyword.pdf`, then put it in `raw/papers/`.

Example:

```text
raw/papers/smith2024-habitat-loss.pdf
```

PDFs are ignored by Git, so keep them backed up somewhere else such as Zotero, Google Drive, Dropbox, or OneDrive.

## 4. Register the Paper

Prompt the LLM:

```text
catalog
```

This updates `raw/_catalog.json` and `raw/_catalog.md`.

## 5. Ingest the Paper

Prompt the LLM:

```text
ingest smith2024-habitat-loss.pdf
```

The LLM should extract the PDF text, create a summary in `wiki/summaries/`, run a fidelity check, and update the wiki index.

## 6. Browse the Wiki

Open these files in Obsidian:

- `wiki/_index.md`
- `wiki/_sources.md`
- the new file in `wiki/summaries/`

## 7. Grow the Wiki

Useful next prompts:

```text
status
compile-concepts
query <your question>
synthesize <topic>
lint
```

Use a stronger model for `ingest`, `eval`, and `synthesize` when possible.

## Optional: Install the CLI

If you prefer command-line automation over prompting the LLM directly:

```bash
pip install -e ".[anthropic]"
kb status
```

The `kb` CLI runs the same workflows as the prompts above, but as a local pipeline. See [README.md](README.md) for the full command list.
