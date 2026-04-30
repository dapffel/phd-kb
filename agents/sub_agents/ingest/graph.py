import re

from langgraph.graph import StateGraph, END

from agents.config import settings
from agents.llm import invoke, load_prompt
from agents.models import FidelityIssue, FidelityResult, IngestResult, IngestState
from agents.sub_agents.base import BaseAgent


class IngestAgent(BaseAgent[IngestState]):
    state_schema = IngestState

    def build_graph(self) -> StateGraph:
        g = StateGraph(IngestState)

        g.add_node("extract", self.extract)
        g.add_node("compile", self.compile)
        g.add_node("fidelity_check", self.fidelity_check)
        g.add_node("fix_summary", self.fix_summary)
        g.add_node("save", self.save)

        g.set_entry_point("extract")
        g.add_edge("extract", "compile")
        g.add_edge("compile", "fidelity_check")
        g.add_conditional_edges("fidelity_check", self.route_fidelity)
        g.add_edge("fix_summary", "fidelity_check")
        g.add_edge("save", END)

        return g

    def route_fidelity(self, state: IngestState) -> str:
        fidelity = state["fidelity"]
        if fidelity.passed:
            return "save"
        if state.get("attempts", 1) >= settings.max_fidelity_attempts:
            return "save"
        return "fix_summary"

    def extract(self, state: IngestState) -> dict:
        filename = state["filename"]
        existing = self.vault.read_extract(filename)
        if existing:
            return {"source_text": existing}

        text = self.vault.extract_pdf(filename)
        self.vault.save_extract(filename, text)
        return {"source_text": text}

    def compile(self, state: IngestState) -> dict:
        system = load_prompt("compile-source.md")
        summary = invoke(system, state["source_text"], strong=True)
        return {"summary": summary, "attempts": 1}

    def fidelity_check(self, state: IngestState) -> dict:
        system = load_prompt("eval-source.md")
        human = (
            f"## Source Text\n{state['source_text'][:8000]}\n\n"
            f"## Summary to Evaluate\n{state['summary']}"
        )
        raw = invoke(system, human)
        return {"fidelity": self._parse_fidelity(raw)}

    def fix_summary(self, state: IngestState) -> dict:
        issues = state["fidelity"].issues
        issue_text = "\n".join(f"- {i.classification}: {i.claim}" for i in issues)

        system = (
            "You are a research wiki editor. Fix the following summary based on "
            "the fidelity issues found. Return the complete corrected summary."
        )
        human = (
            f"## Issues Found\n{issue_text}\n\n"
            f"## Original Source\n{state['source_text'][:6000]}\n\n"
            f"## Current Summary\n{state['summary']}"
        )
        fixed = invoke(system, human, strong=True)
        return {"summary": fixed, "attempts": state.get("attempts", 1) + 1}

    def save(self, state: IngestState) -> dict:
        filename = state["filename"]
        stem = filename.rsplit(".", 1)[0]

        self.vault.save_article("summaries", f"{stem}.md", state["summary"])

        concepts = re.findall(r"\[\[([^\]]+)\]\]", state["summary"])
        existing = {f.stem for f in self.vault.list_concepts()}
        new_concepts = [c for c in concepts if c not in existing]

        self.vault.mark_ingested(filename)

        title_match = re.search(r'title:\s*"?([^"\n]+)"?', state["summary"])
        title = title_match.group(1) if title_match else filename
        self.vault.update_sources_file(filename, title)
        self.vault.regenerate_wiki_index()

        result = IngestResult(
            source_filename=filename,
            summary_path=f"wiki/summaries/{stem}.md",
            fidelity=state["fidelity"],
            detected_concepts=new_concepts,
            attempts=state.get("attempts", 1),
        )
        return {"detected_concepts": new_concepts, "result": result}

    def _parse_fidelity(self, raw: str) -> FidelityResult:
        verified = len(re.findall(r"VERIFIED", raw, re.IGNORECASE))
        distorted = len(re.findall(r"DISTORTED", raw, re.IGNORECASE))
        unsupported = len(re.findall(r"UNSUPPORTED", raw, re.IGNORECASE))
        missing = len(re.findall(r"MISSING.ATTRIBUTION", raw, re.IGNORECASE))

        issues = []
        for match in re.finditer(
            r"#### Issue \d+[^\n]*\n(.*?)(?=#### Issue|\Z)", raw, re.DOTALL
        ):
            block = match.group(1)
            claim = re.search(r"\*\*Claim.*?\*\*:\s*(.+)", block)
            classification = re.search(r"\*\*Classification\*\*:\s*(.+)", block)
            if claim:
                issues.append(FidelityIssue(
                    claim=claim.group(1).strip(),
                    classification=classification.group(1).strip() if classification else "unknown",
                ))

        return FidelityResult(
            claims_checked=verified + distorted + unsupported + missing,
            verified=verified,
            distorted=distorted,
            unsupported=unsupported,
            missing_attribution=missing,
            issues=issues,
        )
