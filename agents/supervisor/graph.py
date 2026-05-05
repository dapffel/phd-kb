from datetime import date

from langgraph.graph import StateGraph, END

from agents.models import (
    IngestState, SynthesizeState, EvalState, QueryState,
    SupervisorState,
)
from agents.vault import Vault
from agents.config import settings
from agents.git_ops import has_changes
from agents.llm import invoke, load_prompt
from agents.sub_agents.status.graph import StatusAgent
from agents.sub_agents.catalog.graph import CatalogAgent
from agents.sub_agents.ingest.graph import IngestAgent
from agents.sub_agents.compile_concepts.graph import CompileConceptsAgent
from agents.sub_agents.synthesize.graph import SynthesizeAgent
from agents.sub_agents.eval_agent.graph import EvalAgent
from agents.sub_agents.lint.graph import LintAgent
from agents.sub_agents.query.graph import QueryAgent


class Supervisor:
    def __init__(self):
        self.vault = Vault()

    def build_graph(self) -> StateGraph:
        g = StateGraph(SupervisorState)
        g.add_node("route", self.route)
        g.set_entry_point("route")
        g.add_edge("route", END)
        return g

    def run(self, command: str, args: str = "") -> str:
        graph = self.build_graph().compile()
        result = graph.invoke({"command": command, "args": args})
        if isinstance(result, dict):
            return result.get("output", "")
        return result.output

    def route(self, state: SupervisorState) -> dict:
        command = state.command
        args = state.args

        handler = {
            "init": self._init,
            "status": self._status,
            "catalog": self._catalog,
            "catalog-update": self._catalog_update,
            "find": self._find,
            "ingest": self._ingest,
            "ingest-all": self._ingest_all,
            "compile-concepts": self._compile_concepts,
            "synthesize": self._synthesize,
            "slides": self._slides,
            "eval": self._eval,
            "eval-all": self._eval_all,
            "lint": self._lint,
            "query": self._query,
            "update-chapter": self._update_chapter,
        }.get(command)

        if not handler:
            return {"output": f"Unknown command: {command}"}

        return {"output": handler(args)}

    def _with_commit_suggestion(self, output: str, message: str) -> str:
        if has_changes(["wiki/", "raw/_catalog.json", "raw/_catalog.md", "outputs/"]):
            return f"{output}\n\nSuggested commit: `{message}`"
        return output

    def _init(self, args: str) -> str:
        dirs = [
            "raw/papers", "raw/notes", "raw/web", "raw/images",
            "wiki/summaries", "wiki/concepts", "wiki/connections",
            "research", "outputs/reports", "outputs/evals",
            "outputs/slides", "outputs/figures", "prompts",
        ]
        for dirname in dirs:
            (settings.vault_root / dirname).mkdir(parents=True, exist_ok=True)

        created = []
        files = {
            settings.raw_dir / "_catalog.json": "[]\n",
            settings.raw_dir / "_catalog.md": (
                "---\ntitle: \"Source Catalog\"\nupdated: "
                f"{date.today().isoformat()}\ntotal: 0\nextracted: 0\ningested: 0\n---\n\n## All Sources\n\n"
            ),
            settings.wiki_index: "---\ntitle: \"Wiki Index\"\nupdated: \n---\n\n## Summaries\n\n## Concepts\n\n## Connections\n",
            settings.wiki_sources: "---\ntitle: \"Source Catalog\"\nupdated: \n---\n\n## Ingested Sources\n",
            settings.wiki_glossary: "---\ntitle: \"Glossary\"\nupdated: \n---\n\n## Terms\n",
            settings.vault_root / ".gitignore": (
                "# Obsidian temporary files\n.obsidian/workspace.json\n"
                ".obsidian/workspace-mobile.json\n.trash/\n\n# OS files\n.DS_Store\nThumbs.db\n\n"
                "# Large binary files\nraw/papers/*.pdf\nraw/web/*.pdf\n\nresearch/\n"
            ),
            settings.prompts_dir / "compile-source.md": "You are a research wiki compiler. Summarize one source into the wiki summary format.\n",
            settings.prompts_dir / "write-concept.md": "You are a research wiki compiler. Synthesize concept articles from source summaries.\n",
            settings.prompts_dir / "lint-wiki.md": "You are a wiki health checker. Report broken links, stale articles, contradictions, and gaps.\n",
            settings.prompts_dir / "query.md": "Answer questions using only the wiki content and cite [[wikilinks]].\n",
            settings.prompts_dir / "update-chapter.md": "Suggest chapter updates while preserving the researcher's voice.\n",
            settings.prompts_dir / "synthesize.md": "Produce a cross-source synthesis document with traceable [[wikilinks]].\n",
            settings.prompts_dir / "eval-source.md": "Evaluate wiki factual claims against their original sources.\n",
            settings.vault_root / "research" / "chapter-1-current-state.md": self._chapter_template("Chapter 1: Current State of the Field"),
            settings.vault_root / "research" / "chapter-2-methodology.md": self._chapter_template("Chapter 2: Methodology"),
            settings.vault_root / "research" / "chapter-3-findings.md": self._chapter_template("Chapter 3: Findings"),
            settings.vault_root / "research" / "_research-index.md": (
                "---\ntitle: \"Research Overview\"\nupdated: \n---\n\n"
                "## Dissertation Structure\n\n"
                "| Chapter | Title | Status | Last Updated |\n"
                "|---------|-------|--------|-------------|\n"
                "| 1 | Current State of the Field | not started | — |\n"
                "| 2 | Methodology | not started | — |\n"
                "| 3 | Findings | not started | — |\n"
            ),
        }
        for path, content in files.items():
            if not path.exists():
                path.write_text(content)
                created.append(str(path.relative_to(settings.vault_root)))

        report = f"Initialized vault structure. Created {len(created)} files; existing files were left untouched."
        if not created:
            return report
        return self._with_commit_suggestion(report, "init: scaffold vault structure and prompt templates")

    def _chapter_template(self, title: str) -> str:
        return (
            "---\n"
            f'title: "{title}"\n'
            "status: draft\n"
            "updated: \n"
            "---\n\n"
            "## Research Question\n\n"
            "## Current State\n\n"
            "## Key Debates and Disagreements\n\n"
            "## Identified Gaps\n\n"
            "## My Position\n\n"
            "## TODO\n"
            "- [ ] Draft this chapter\n"
        )

    def _status(self, args: str) -> str:
        return StatusAgent(self.vault).run().report

    def _catalog(self, args: str) -> str:
        result = CatalogAgent(self.vault).run()
        return self._with_commit_suggestion(result.report, f"catalog: {result.report}")

    def _catalog_update(self, args: str) -> str:
        catalog = self.vault.load_catalog()
        for entry in catalog:
            entry.extracted = self.vault.has_extract(entry.filename)
            entry.ingested = self.vault.has_summary(entry.filename)
        self.vault.save_catalog(catalog)
        report = f"Catalog updated. Total: {len(catalog)}."
        return self._with_commit_suggestion(report, "catalog: update extracted and ingested flags")

    def _find(self, args: str) -> str:
        query = args.strip().strip('"').lower()
        if not query:
            return "Usage: find <query>"

        matches = []
        for entry in self.vault.load_catalog():
            haystack = " ".join([
                entry.title,
                " ".join(entry.authors),
                " ".join(entry.keywords),
            ]).lower()
            if query in haystack:
                matches.append(entry)

        if not matches:
            return f"No catalog matches for: {args}"

        lines = [f"Found {len(matches)} matches:", ""]
        not_ingested = []
        for i, entry in enumerate(matches, 1):
            authors = ", ".join(entry.authors[:3])
            if len(entry.authors) > 3:
                authors += " et al."
            ext = "extracted" if entry.extracted else "not extracted"
            ing = "ingested" if entry.ingested else "not ingested"
            if not entry.ingested:
                not_ingested.append(entry.filename)
            lines += [
                f"{i}. \"{entry.title}\" — {authors}, {entry.year}",
                f"   Keywords: {', '.join(entry.keywords)}",
                f"   Status: {ext}, {ing}",
                "",
            ]
        if not_ingested:
            lines.append("Some matches have not been ingested yet. Run `ingest <filename>` for any you want to add.")
        return "\n".join(lines).rstrip()

    def _ingest(self, args: str) -> str:
        if not args:
            unprocessed = self.vault.unprocessed_pdfs()
            uningested = self.vault.uningested_papers()
            targets = unprocessed or uningested
            if not targets:
                return "Nothing to ingest."
            args = targets[0]

        result = IngestAgent(self.vault).run(IngestState(filename=args))

        lines = [f"Ingested: {args}"]
        if result.result:
            f = result.result.fidelity
            lines.append(
                f"Fidelity: {f.claims_checked} claims, {f.verified} verified, "
                f"{f.distorted} distorted, {f.unsupported} unsupported "
                f"(attempts: {result.result.attempts})"
            )
            if result.detected_concepts:
                lines.append(f"New concepts detected: {', '.join(result.detected_concepts)}")

        output = "\n".join(lines)
        return self._with_commit_suggestion(output, f"ingest: add {args.rsplit('.', 1)[0]}")

    def _ingest_all(self, args: str) -> str:
        unprocessed = self.vault.unprocessed_pdfs()
        uningested = self.vault.uningested_papers()
        targets = list(set(unprocessed + uningested))

        if not targets:
            return "All papers already ingested."

        results = [self._ingest(filename) for filename in targets]
        return "\n\n".join(results)

    def _compile_concepts(self, args: str) -> str:
        result = CompileConceptsAgent(self.vault).run()
        return self._with_commit_suggestion(
            result.report,
            f"compile: generate {len(result.created)} concept articles",
        )

    def _synthesize(self, args: str) -> str:
        if not args:
            return "Usage: synthesize <topic>"
        result = SynthesizeAgent(self.vault).run(SynthesizeState(topic=args))
        return self._with_commit_suggestion(result.report, f"synthesize: {args}")

    def _slides(self, args: str) -> str:
        if not args:
            return "Usage: slides <topic>"
        topic = args.strip()
        all_files = self.vault.list_summaries() + self.vault.list_concepts() + self.vault.list_connections()
        relevant = [
            path.read_text()
            for path in all_files
            if topic.lower() in path.read_text().lower() or topic.lower() in path.stem.lower()
        ][:10]
        if not relevant:
            return f"No relevant wiki articles found for slides topic: {topic}"

        system = (
            "You are creating a Marp slide deck from a PhD research wiki. "
            "Return only markdown. Include Marp frontmatter and cite wiki sources with [[wikilinks]]."
        )
        human = f"Topic: {topic}\n\nWiki context:\n\n" + "\n---\n".join(relevant)
        deck = invoke(system, human, strong=True)
        slug = topic.lower().replace(" ", "-")
        path = settings.outputs_dir / "slides" / f"{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(deck)
        return self._with_commit_suggestion(
            f"Slide deck saved to outputs/slides/{slug}.md",
            f"synthesize: create slides for {slug}",
        )

    def _eval(self, args: str) -> str:
        if not args:
            return "Usage: eval <filename>"
        result = EvalAgent(self.vault).run(EvalState(filename=args))
        return self._with_commit_suggestion(result.report or "Eval complete.", f"eval: check {args}")

    def _eval_all(self, args: str) -> str:
        reports = []
        articles = self.vault.list_summaries() + self.vault.list_concepts()
        for path in articles:
            result = EvalAgent(self.vault).run(EvalState(filename=path.name))
            reports.append(result.report or f"Eval complete for {path.name}.")

        summary_path = settings.outputs_dir / "evals" / "_eval-summary.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(
            "# Eval Summary\n\n"
            f"Date: {date.today().isoformat()}\n\n"
            + "\n".join(f"- {line}" for line in reports)
            + "\n"
        )
        return self._with_commit_suggestion(
            f"Eval-all complete for {len(reports)} articles. Roll-up saved to outputs/evals/_eval-summary.md",
            "eval: eval-all run",
        )

    def _lint(self, args: str) -> str:
        result = LintAgent(self.vault).run()
        return self._with_commit_suggestion(result.report, "lint: update wiki health report artifacts")

    def _query(self, args: str) -> str:
        if not args:
            return "Usage: query <question>"
        result = QueryAgent(self.vault).run(QueryState(question=args))
        return result.answer

    def _update_chapter(self, args: str) -> str:
        if not args:
            return "Usage: update-chapter <chapter-name>"
        chapter = args if args.endswith(".md") else f"{args}.md"
        path = settings.vault_root / "research" / chapter
        if not path.exists():
            matches = list((settings.vault_root / "research").glob(f"*{args}*.md"))
            if len(matches) == 1:
                path = matches[0]
            else:
                return f"No chapter found for: {args}"

        content = path.read_text()
        links = sorted(set(__import__("re").findall(r"\[\[([^\]]+)\]\]", content)))
        wiki_files = {p.stem: p for p in self.vault.list_summaries() + self.vault.list_concepts() + self.vault.list_connections()}
        referenced = [wiki_files[link].read_text() for link in links if link in wiki_files]

        system = load_prompt("update-chapter.md")
        human = (
            f"Chapter file: {path.name}\n\n## Chapter\n{content}\n\n"
            f"## Referenced wiki articles\n\n" + "\n---\n".join(referenced)
        )
        suggestions = invoke(system, human, strong=True)
        return suggestions
