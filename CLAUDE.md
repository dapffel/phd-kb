# PhD Knowledge Base — LLM Instructions

## What This Is

These instructions tell the LLM how to scaffold and maintain a personal knowledge base for your PhD research. The system has two layers: an **articles wiki** (LLM-written summaries of papers you've read) and **research chapters** (your synthesis and arguments). Both live in one Obsidian vault.

This file defines how the LLM should manage this vault. Claude Code reads it automatically as `CLAUDE.md`. Tools that read `AGENTS.md` should use that file as a pointer back to this canonical instruction set. For other tools, paste the contents of this file as system context.

---

## Project Structure

When asked to initialize the vault, create exactly this structure:

```
phd-kb/
├── raw/                          # Source materials — human curated, never auto-edited
│   ├── papers/                   # PDFs and their markdown extracts
│   ├── notes/                    # Your own rough notes, ideas, scratchpad
│   ├── web/                      # Web-clipped articles (from Obsidian Web Clipper)
│   ├── images/                   # Figures, diagrams, screenshots from sources
│   ├── _catalog.json             # Source of truth — structured index of all PDFs
│   └── _catalog.md               # Human-readable view, auto-generated from JSON
│
├── wiki/                         # LLM-generated and LLM-maintained — never hand-edit
│   ├── summaries/                # One summary per source document
│   ├── concepts/                 # Standalone concept/topic articles
│   ├── connections/              # Cross-cutting themes, contradictions, comparisons
│   ├── _index.md                 # Master index of all wiki articles, grouped by theme
│   ├── _sources.md               # Catalog of every ingested source with one-line descriptions
│   └── _glossary.md              # Alphabetical term definitions
│
├── research/                     # YOUR dissertation chapters and synthesis
│   └── templates/                # Starter chapter templates tracked in Git
│
├── outputs/                      # Generated deliverables
│   ├── reports/                  # Research reports, literature reviews
│   ├── evals/                    # Eval reports from fidelity checks
│   ├── slides/                   # Marp-format slide decks
│   └── figures/                  # Generated charts, diagrams, visualizations
│
├── prompts/                      # Reusable prompt templates (used by the LLM)
│   ├── compile-source.md
│   ├── write-concept.md
│   ├── lint-wiki.md
│   ├── query.md
│   ├── update-chapter.md
│   ├── synthesize.md
│   └── eval-source.md
│
├── CLAUDE.md                     # This file — canonical LLM instructions
├── AGENTS.md                     # Pointer for tools that auto-read AGENTS.md
└── .gitignore
```

---

## Core Rules

1. **Never edit files in `raw/` automatically.** That directory is human-curated. Only read from it.
2. **Never hand-edit files in `wiki/`.** All wiki content is generated and maintained by the LLM. If something is wrong, fix the source or the prompt and regenerate.
3. **Research chapter files in `research/` are collaborative.** The human writes their arguments; you help draft, expand, and update sections when asked. Always preserve the human's voice and intent.
4. **Always use Obsidian-style `[[wikilinks]]`** when referencing other articles. Use the filename without extension as the link target (e.g., `[[attention-mechanisms]]` links to `wiki/concepts/attention-mechanisms.md`).
5. **Every wiki article must have YAML frontmatter** with at least: `title`, `created`, `updated`, `type` (summary | concept | connection), and `sources` (list of source filenames).
6. **After any wiki changes, update `_index.md` and `_sources.md`** to reflect the current state.

---

## Commands

When the user gives one of these commands, follow the corresponding workflow:

### `init`
Create the full directory structure above. Generate starter `_index.md`, `_sources.md`, `_glossary.md` files with placeholder content. Generate empty `raw/_catalog.json` (as `[]`) and `raw/_catalog.md` with placeholder header. Generate all prompt templates in `prompts/`. Generate research chapter templates. Generate `.gitignore` (ignore `.obsidian/workspace.json`, `.trash/`). Print a summary of what was created.

### `ingest <filename>`
The user has added a new PDF or markdown file to `raw/papers/` or `raw/web/`. Do the following:
1. Read the source file.
2. If it's a PDF, extract the content to a companion `.md` file in the same directory.
3. Using the compilation prompt (`prompts/compile-source.md`), generate a structured summary and save it to `wiki/summaries/<filename>.md`.
4. **Fidelity check (automatic):** Re-read the original source and compare it against the generated summary. For each claim in the summary, verify it is supported by the source. Flag any claim that is unsupported, distorted, or overly simplified. If issues are found, fix them in the summary before proceeding. Print a brief fidelity report (e.g., "Fidelity check: 12 claims verified, 0 issues found" or "Fidelity check: 11/12 claims verified, 1 fixed — Finding #3 overstated significance").
5. Scan the summary for `[[wikilinks]]` to concepts that don't have articles yet. List them for the user.
6. Update `_sources.md` with the new source entry.
7. Update `_index.md` if new categories emerged.
8. Update `raw/_catalog.json` — mark this source as `extracted: true, ingested: true`. Regenerate `raw/_catalog.md`.
9. Print: what was created, what new concepts were detected, fidelity check result, and suggested next steps.

### `ingest-all`
Run the `ingest` workflow for every file in `raw/papers/` and `raw/web/` that doesn't already have a corresponding summary in `wiki/summaries/`.

### `compile-concepts`
1. Read all files in `wiki/summaries/`.
2. Identify the most important concepts that appear across multiple sources.
3. For each concept, check if `wiki/concepts/<concept-name>.md` exists.
4. For new concepts: generate a standalone article that synthesizes what the sources say. Include backlinks to relevant summaries and cross-links to related concepts.
5. For existing concepts: update the article with any new information from recently added sources.
6. Regenerate `_index.md` and `_glossary.md`.
7. Print: how many concepts were created/updated, and the current wiki stats (total articles, total sources, total words).

### `lint`
Run a health check over the entire wiki:
1. **Broken links**: Find all `[[wikilinks]]` that point to files that don't exist. List them and suggest which ones to create.
2. **Orphaned files**: Find wiki articles that no other article links to.
3. **Contradictions**: Scan for claims in different articles that may conflict. Create or update `wiki/connections/contradictions.md`.
4. **Gaps**: Based on the existing wiki content, suggest topics or papers that seem missing.
5. **Stale content**: Flag articles whose source summaries have been updated more recently than the concept articles that reference them.
6. Print a health report with counts and recommendations.

### `query <question>`
1. Read `_index.md` to understand the wiki structure.
2. Identify which articles are relevant to the question.
3. Read those articles.
4. Synthesize an answer grounded in the wiki content, citing specific sources.
5. If the answer would be useful to keep, ask the user if they want to file it into `wiki/connections/` or `outputs/reports/`.

### `update-chapter <chapter-name>`
1. Read the specified research chapter file.
2. Read all wiki articles it references via `[[wikilinks]]`.
3. Check if any referenced sources have been updated since the chapter was last modified.
4. Suggest updates: new findings to incorporate, outdated claims to revise, new connections to add.
5. If the user approves, make the updates while preserving the human's voice and argumentation style.

### `status`
Print a dashboard:
- Total sources ingested
- Total wiki articles (summaries + concepts + connections)
- Total word count across wiki
- Research chapters and their last-updated dates
- Number of broken links
- Number of concepts without articles

### `slides <topic>`
Generate a Marp-format slide deck on the given topic using wiki content. Save to `outputs/slides/<topic>.md`.

### `synthesize <topic>`
1. Read `_index.md` to find all articles related to the topic.
2. Read each relevant summary and concept article.
3. Produce a synthesis document that:
   - Summarizes the state of knowledge across all sources
   - Groups sources by their position or approach
   - Highlights agreements, disagreements, and gaps
   - Includes a comparison table where appropriate
   - Ends with open questions and suggested further reading
4. Save to `wiki/connections/<topic>.md` with frontmatter `type: connection`.
5. Update `_index.md`.
6. Print: how many sources were synthesized, key agreements/disagreements found.

### `eval <filename>`
Deep evaluation of a single wiki article against its original sources.
1. Read the wiki article (summary or concept).
2. Extract every factual claim it makes (findings, numbers, methodology descriptions, attributions).
3. For each claim, trace it back to the original source document in `raw/`.
4. Classify each claim as:
   - **Verified** — accurately reflects the source
   - **Distorted** — based on the source but overstated, understated, or subtly shifted
   - **Unsupported** — not found in any cited source (possible hallucination)
   - **Missing attribution** — claim is accurate but doesn't cite which source it came from
5. For concept articles, also check:
   - **Missing sources** — sources in the wiki that discuss this concept but aren't cited in the article
   - **Synthesis accuracy** — when the article compares or contrasts sources, verify it represents each source's position fairly
6. Save the eval report to `outputs/evals/eval-<filename>.md` with a summary table and detailed findings.
7. Print a summary: total claims, verified count, issues found, and severity.

### `eval-all`
Run `eval` on every file in `wiki/summaries/` and `wiki/concepts/`. Produce a roll-up report at `outputs/evals/_eval-summary.md` that includes:
- Overall fidelity score (% of claims verified across the wiki)
- List of articles sorted by issue count (worst first)
- Most common error types
- Specific articles that need attention
This is expensive — suggest running it after major compilation rounds, not after every ingest.

### `catalog`
Scan `raw/papers/` for any PDFs not yet in `_catalog.json`. For each new PDF:
1. Read the first 1–2 pages of the PDF.
2. Extract: title, authors, year, and 3–5 keywords that describe the paper's topic.
3. Note the filename and whether a corresponding `.md` extract and `wiki/summaries/` entry exist.
4. Add an entry to `raw/_catalog.json`.
5. After processing all new PDFs, regenerate `raw/_catalog.md` from the JSON.
6. Print: how many new entries were added, total catalog size.

`_catalog.json` format:
```json
[
  {
    "filename": "vaswani2017-attention.pdf",
    "title": "Attention Is All You Need",
    "authors": ["Vaswani", "Shazeer", "Parmar", "Uszkoreit", "Jones", "Gomez", "Kaiser", "Polosukhin"],
    "year": 2017,
    "keywords": ["transformer", "attention", "self-attention", "sequence-to-sequence", "neural-machine-translation"],
    "extracted": true,
    "ingested": true
  }
]
```

`_catalog.md` format (auto-generated, never hand-edited):
```markdown
---
title: "Source Catalog"
updated: YYYY-MM-DD
total: N
extracted: N
ingested: N
---

## All Sources

| # | Title | Authors | Year | Keywords | Extracted | Ingested |
|---|-------|---------|------|----------|-----------|----------|
| 1 | Attention Is All You Need | Vaswani et al. | 2017 | transformer, attention, self-attention | ✅ | ✅ |
| 2 | BERT: Pre-training of Deep... | Devlin et al. | 2019 | BERT, pre-training, NLP | ✅ | ❌ |
| 3 | (new, unprocessed) | — | — | — | ❌ | ❌ |

## Not Yet Extracted
- smith2024-something.pdf
- chen2025-other.pdf

## Extracted But Not Ingested
- devlin2019-bert.pdf
```

### `find <query>`
Search the catalog for papers matching a query.
1. Read `raw/_catalog.json`.
2. Search across `title`, `authors`, and `keywords` fields. Match is case-insensitive and partial (e.g., `find "attention"` matches titles and keywords containing "attention").
3. Return matching entries as a numbered list with title, authors, year, and status (extracted/ingested).
4. If matches include papers not yet ingested, ask: "Would you like to ingest any of these?"

Example interaction:
```
> find "transformer"

Found 3 matches:

1. "Attention Is All You Need" — Vaswani et al., 2017
   Keywords: transformer, attention, self-attention
   Status: ✅ extracted, ✅ ingested

2. "An Image is Worth 16x16 Words" — Dosovitskiy et al., 2021
   Keywords: vision-transformer, image-classification, patches
   Status: ✅ extracted, ❌ not ingested

3. "Scaling Transformers for Long Sequences" — Chen et al., 2024
   Keywords: transformer, long-context, efficiency
   Status: ❌ not extracted, ❌ not ingested

Papers #2 and #3 haven't been ingested yet. Want me to ingest them?
```

### `catalog-update`
Regenerate `raw/_catalog.md` from `raw/_catalog.json`. Also update the `extracted` and `ingested` flags by checking whether the corresponding `.md` file exists in `raw/papers/` and `wiki/summaries/`. Use this after manual file changes.

---

## Prompt Templates

When running `init`, create these files in `prompts/`:

### `prompts/compile-source.md`

```markdown
You are a research wiki compiler. Given a source document, produce a structured
summary to be saved in wiki/summaries/.

Output format (copy exactly):

---
title: "[Paper title]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: summary
sources:
  - [source-filename]
---

## Citation
Full bibliographic reference.

## TL;DR
2–3 sentences capturing the core contribution.

## Key Concepts
- [[concept-name-1]] — one-line description of how this paper relates to it
- [[concept-name-2]] — one-line description
(use lowercase-hyphenated names for wikilinks)

## Methodology
3–6 sentences. What approach, dataset, or framework was used?

## Key Findings
1. Finding one.
2. Finding two.
(one sentence each, be specific)

## Limitations
What did the authors not address? What are the weak points?

## Connections
How does this relate to other sources in the wiki? Use [[wikilinks]].
If you don't know what else is in the wiki, leave TODO markers.

## Open Questions
What follow-up questions does this paper raise?

---

Rules:
- Never invent findings not in the source.
- Preserve technical terminology exactly as the authors use it.
- Use [[double-bracket]] wikilinks for any concept that could be its own article.
- Keep concept link names consistent (always lowercase-hyphenated).
- If the source is ambiguous, say so rather than guessing.
```

### `prompts/write-concept.md`

```markdown
You are a research wiki compiler. Given a concept name and a set of source
summaries that discuss it, write a standalone concept article for wiki/concepts/.

Output format:

---
title: "[Concept Name]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
sources:
  - [source-1-filename]
  - [source-2-filename]
---

## Definition
Clear, concise definition of the concept. 2–3 sentences.

## Background
Brief context: where did this concept originate? Why does it matter?

## How It Works
Technical explanation. Use detail appropriate to a PhD-level reader.
Include equations or pseudocode if relevant.

## Key Results From Sources
Summarize what each source says about this concept:
- **[[source-1-summary]]**: what they found
- **[[source-2-summary]]**: what they found

## Open Problems
What remains unsolved or debated about this concept?

## Related Concepts
- [[related-concept-1]]
- [[related-concept-2]]

---

Rules:
- Synthesize across sources, don't just list them.
- If sources disagree, note the disagreement explicitly.
- Link to other concept articles and source summaries via [[wikilinks]].
```

### `prompts/lint-wiki.md`

```markdown
You are a wiki health checker. Scan all files in wiki/ and produce a report.

Check for:
1. Broken [[wikilinks]] — links that point to files that don't exist
2. Orphaned articles — files that nothing links to
3. Inconsistent naming — the same concept referred to by different link names
4. Contradictions — claims in one article that conflict with another
5. Missing frontmatter — articles without proper YAML frontmatter
6. Stale articles — concept articles that haven't been updated since their
   source summaries were modified
7. Suggested new articles — concepts mentioned in 3+ sources that don't
   have their own article yet

Output a structured report with counts and specific file references.
```

### `prompts/query.md`

```markdown
You are a research assistant working with a PhD knowledge base.
The user will ask a question. Answer it using ONLY information from the wiki.

Workflow:
1. Read _index.md to understand the wiki structure.
2. Identify the 3–8 most relevant articles.
3. Read them carefully.
4. Synthesize an answer that:
   - Directly addresses the question
   - Cites specific sources using [[wikilinks]]
   - Notes any disagreements or gaps in the literature
   - Suggests follow-up questions

If the wiki doesn't contain enough information to answer, say so and
suggest what sources to ingest to fill the gap.
```

### `prompts/update-chapter.md`

```markdown
You are helping a PhD researcher maintain their dissertation chapters.

Given a chapter file from research/ and the current state of wiki/:
1. Identify all [[wikilinks]] in the chapter.
2. Read the referenced wiki articles.
3. Check for:
   - New sources that are relevant but not yet cited in the chapter
   - Claims in the chapter that are contradicted by newer sources
   - Gaps in the argument that wiki content could fill
4. Suggest specific edits. For each suggestion:
   - Quote the current text
   - Propose the updated text
   - Explain why (citing the wiki source)

IMPORTANT: Preserve the researcher's voice and argumentation style.
You are suggesting edits, not rewriting. The chapter is THEIRS.
```

### `prompts/eval-source.md`

```markdown
You are a factual accuracy evaluator for a PhD research wiki.

Given a wiki article and its original source document(s), verify every
factual claim in the article against the sources.

For each claim, classify it as:

1. VERIFIED — accurately reflects the source material
2. DISTORTED — rooted in the source but overstated, understated, or
   subtly shifted in meaning. Explain what changed.
3. UNSUPPORTED — not found in any cited source. This may be a
   hallucination or an inference not warranted by the data.
4. MISSING ATTRIBUTION — the claim is accurate but doesn't specify
   which source it comes from.

Output format:

## Eval Report: [article filename]
**Date**: YYYY-MM-DD
**Claims checked**: N
**Verified**: N | **Distorted**: N | **Unsupported**: N | **Missing attribution**: N

### Issues

#### Issue 1: [short description]
- **Claim in article**: "[exact quote from article]"
- **Classification**: DISTORTED / UNSUPPORTED / MISSING ATTRIBUTION
- **Source says**: "[what the source actually says, or 'not found']"
- **Suggested fix**: "[corrected text]"

(repeat for each issue)

### Summary
[1–2 sentence overall assessment. Is this article trustworthy?
What should be re-checked or rewritten?]

---

Rules:
- Be strict. PhD-level accuracy matters.
- A claim that is "close but not quite" is DISTORTED, not VERIFIED.
- If a summary says "the authors found X significantly improves Y" but
  the paper says "X shows modest improvements in Y," that's distorted.
- Check numbers, percentages, and statistical claims especially carefully.
- Do not evaluate writing quality or style — only factual accuracy.
```

### `prompts/synthesize.md`

```markdown
You are a research synthesizer working with a PhD knowledge base.

Given a topic and a set of wiki articles that discuss it, produce a
cross-source synthesis document for wiki/connections/.

Output format:

---
title: "Synthesis: [Topic]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: connection
sources:
  - [list all source filenames referenced]
---

## Overview
2–3 sentence summary of what this synthesis covers and why it matters.

## State of Knowledge
What do the sources collectively tell us about this topic?
Write in prose, not as a list of papers. Synthesize, don't summarize.

## Approaches and Positions
Group sources by their approach or stance:

### Approach A: [descriptive name]
Which sources take this approach, what they argue, what evidence they provide.
Use [[wikilinks]] to reference specific summaries.

### Approach B: [descriptive name]
(same structure)

## Comparison

| Dimension | Approach A | Approach B |
|-----------|-----------|-----------|
| Key claim | ... | ... |
| Method | ... | ... |
| Strengths | ... | ... |
| Weaknesses | ... | ... |

## Agreements
What do ALL or MOST sources agree on?

## Disagreements
Where do sources conflict? Be specific about what each side claims.

## Gaps
What questions remain unanswered across all sources?

## Open Questions for Further Research
What should be investigated next?

---

Rules:
- Synthesize, don't just list. The reader should understand the
  landscape after reading this, not need to read each source.
- Every claim must be traceable to a specific source via [[wikilinks]].
- If you're uncertain whether sources agree or disagree, say so.
- Be fair to all positions — don't favor one source over another.
```

---

## Research Chapter Template

When running `init`, create these starter templates in `research/templates/`. Users can copy them into the root of `research/` when they are ready to draft chapters. The root chapter drafts are ignored by Git by default.

### `research/templates/chapter-1-current-state.md`

```markdown
---
title: "Chapter 1: Current State of the Field"
status: draft
updated: YYYY-MM-DD
---

## Research Question
> What is the central question this chapter addresses?
> (Write your question here)

## Current State of the Field
What is the current consensus on this topic? What do the major
sources agree on?

(Link to wiki articles: [[concept-1]], [[concept-2]])

## Key Debates and Disagreements
Where do sources diverge? What remains contested?

## Identified Gaps
What has NOT been studied? What questions remain unanswered?
This is where your research contribution fits.

## My Position
Your argument. What do YOU think, based on the evidence?

## Evidence Summary
| Claim | Supporting Sources | Contradicting Sources |
|-------|-------------------|----------------------|
| ...   | [[source-1]]      | [[source-2]]         |

## Open Questions
- Question 1
- Question 2

## TODO
- [ ] Items you still need to address
```

### `research/templates/_research-index.md`

```markdown
---
title: "Research Overview"
updated: YYYY-MM-DD
---

## Dissertation Structure

| Chapter | Title | Status | Last Updated |
|---------|-------|--------|-------------|
| 1 | Current State of the Field | draft | — |
| 2 | Methodology | not started | — |
| 3 | Findings | not started | — |

## Key Research Questions
1. (Your main research question)
2. (Sub-question 1)
3. (Sub-question 2)

## Source Coverage
- Total sources ingested: 0
- Sources cited in chapters: 0
- Sources ingested but not yet cited: 0
```

---

## .gitignore

When running `init`, create:

```
# Obsidian temporary files
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/

# OS files
.DS_Store
Thumbs.db

# Large binary files — PDFs are stored in Zotero or cloud storage
# Only the extracted .md versions are tracked in Git
raw/papers/*.pdf
raw/web/*.pdf

# Obsidian plugin cache (the plugin configs ARE tracked)
.obsidian/plugins/*/data.json

# Research chapters — excluded until you're ready to commit them.
# The README and templates stay tracked; your actual chapter drafts stay local.
research/*
!research/.gitkeep
!research/README.md
!research/templates/
!research/templates/*.md
```

---

## Git Workflow

### What gets tracked (and why)

| Directory | Tracked? | Why |
|-----------|----------|-----|
| `prompts/` | Yes | These are the "source code" of your system. Version them like code. |
| `CLAUDE.md` | Yes | LLM instructions. Track every change. |
| `wiki/` | Yes | Diffs show exactly what the LLM changed on each compilation. |
| `research/` | **Templates only** | Starter templates are tracked. Your actual chapter drafts stay local until you deliberately start tracking them. Back up drafts via cloud sync in the meantime. |
| `outputs/` | Yes | Eval reports, generated slides, figures — all worth keeping. |
| `raw/**/*.md` | Yes | Extracted text from papers — lightweight and important. |
| `raw/**/*.pdf` | No | Large binaries. Store in Zotero, Google Drive, or Git LFS. |
| `raw/notes/` | Yes | Your personal notes. |
| `raw/images/` | Yes | Figures extracted from sources. Usually small enough. |
| `.obsidian/` | Partially | Track plugin configs and appearance, ignore workspace state. |

### Commit conventions

After any operation, The LLM should suggest a commit with a prefixed message:

- `init: scaffold vault structure and prompt templates`
- `ingest: add smith2024-attention, 1 summary created, fidelity check passed`
- `ingest: batch ingest 5 papers, 5 summaries, 12 new concepts detected`
- `compile: generate 8 concept articles, update index and glossary`
- `synthesize: cross-source synthesis on attention-mechanisms (6 sources)`
- `eval: eval-all run, 94% fidelity, 3 issues fixed`
- `lint: fix 4 broken links, flag 2 contradictions`
- `prompt: revise compile-source.md — add "Related Work" section`

Note: no `research:` commits until you remove `research/` from `.gitignore`.

### Branching (optional but useful)

For risky operations like prompt changes that affect the whole wiki:
1. Create a branch: `git checkout -b prompt/new-compilation-format`
2. Run the recompilation on the branch.
3. Review the diffs — does the new format actually improve things?
4. Merge if good, discard if not.

This is especially valuable when you change `prompts/compile-source.md` or `prompts/write-concept.md`, since those affect every article in the wiki.

### When to commit

The LLM should suggest a commit after every command that changes tracked files:
- After `ingest` or `ingest-all`
- After `compile-concepts`
- After `synthesize`
- After `eval` (when fixes are applied)
- After `lint` (when fixes are applied)

Do NOT suggest commits for `update-chapter` — research files aren't tracked yet.

Never auto-commit without telling the user. Always print the suggested commit message and let the user confirm.

### Graduating research/ to Git

When you're ready to start tracking a chapter (or all of research/):
1. Remove or narrow the `research/*` rule in `.gitignore`
2. `git add research/`
3. Commit: `research: begin tracking chapter-1 (first complete draft)`

From that point on, The LLM should suggest commits after `update-chapter` as well. You can graduate one chapter at a time by narrowing the ignore rule to the specific files you still want excluded (e.g., `research/chapter-3-findings.md`).

---

## Conventions

- **Filenames**: lowercase-hyphenated. Papers: `authorYEAR-keyword` (e.g., `vaswani2017-attention`). Concepts: descriptive slug (e.g., `attention-mechanisms`).
- **Dates**: ISO 8601 (`YYYY-MM-DD`) everywhere.
- **Wikilinks**: always use the filename without extension, lowercase-hyphenated. Be consistent — if you call it `[[attention-mechanisms]]` once, always use that exact string.
- **Frontmatter**: every file in `wiki/` and `research/` must have YAML frontmatter.
- **Commit messages**: use the prefixed format described in Git Workflow above.
