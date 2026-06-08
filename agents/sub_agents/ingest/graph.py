import re

from langgraph.graph import StateGraph, END

from agents.config import settings
from agents.llm import invoke, load_prompt
from agents.models import FidelityIssue, FidelityResult, IngestResult, IngestState
from agents.state import state_get
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
        fidelity = state_get(state, "fidelity")
        if fidelity.passed:
            return "save"
        if state_get(state, "attempts", 0) >= settings.max_fidelity_attempts:
            return "save"
        return "fix_summary"

    def extract(self, state: IngestState) -> dict:
        filename = state_get(state, "filename", "")
        existing = self.vault.read_extract(filename)
        if existing:
            return {"source_text": existing}

        text = self.vault.extract_pdf(filename)
        self.vault.save_extract(filename, text)
        return {"source_text": text}

    def compile(self, state: IngestState) -> dict:
        system = load_prompt("compile-source.md")
        summary = invoke(system, state_get(state, "source_text", ""), strong=True)
        return {"summary": summary, "attempts": 1}

    def fidelity_check(self, state: IngestState) -> dict:
        system = load_prompt("eval-source.md")
        source_text = state_get(state, "source_text", "")
        summary = state_get(state, "summary", "")
        human = (
            f"## Source Text\n{source_text[:8000]}\n\n"
            f"## Summary to Evaluate\n{summary}"
        )
        raw = invoke(system, human)
        return {"fidelity": self._parse_fidelity(raw)}

    def fix_summary(self, state: IngestState) -> dict:
        issues = state_get(state, "fidelity").issues
        issue_text = "\n".join(f"- {i.classification}: {i.claim}" for i in issues)

        system = (
            "You are a research wiki editor. Fix the following summary based on "
            "the fidelity issues found. Return the complete corrected summary."
        )
        source_text = state_get(state, "source_text", "")
        summary = state_get(state, "summary", "")
        human = (
            f"## Issues Found\n{issue_text}\n\n"
            f"## Original Source\n{source_text[:6000]}\n\n"
            f"## Current Summary\n{summary}"
        )
        fixed = invoke(system, human, strong=True)
        return {"summary": fixed, "attempts": state_get(state, "attempts", 0) + 1}

    def save(self, state: IngestState) -> dict:
        filename = state_get(state, "filename", "")
        stem = filename.rsplit(".", 1)[0]
        summary = state_get(state, "summary", "")

        self.vault.save_article("summaries", f"{stem}.md", summary)

        concepts = re.findall(r"\[\[([^\]]+)\]\]", summary)
        existing = {f.stem for f in self.vault.list_concepts()}
        new_concepts = [c for c in concepts if c not in existing]

        self.vault.mark_ingested(filename)

        title_match = re.search(r'title:\s*"?([^"\n]+)"?', summary)
        title = title_match.group(1) if title_match else filename
        self.vault.update_sources_file(filename, title)
        self.vault.regenerate_wiki_index()

        result = IngestResult(
            source_filename=filename,
            summary_path=f"wiki/summaries/{stem}.md",
            fidelity=state_get(state, "fidelity"),
            detected_concepts=new_concepts,
            attempts=state_get(state, "attempts", 0),
        )
        return {"detected_concepts": new_concepts, "result": result}

    def _parse_fidelity(self, raw: str) -> FidelityResult:
        def _header_int(label: str) -> int | None:
            m = re.search(rf"\*?\*?{label}\*?\*?\s*[:\|]\s*(\d+)", raw, re.IGNORECASE)
            return int(m.group(1)) if m else None

        verified = _header_int("Verified")
        distorted = _header_int("Distorted")
        unsupported = _header_int("Unsupported")
        missing = _header_int("Missing.attribution")

        if verified is None:
            verified = len(re.findall(r"\bVERIFIED\b", raw, re.IGNORECASE))
        if distorted is None:
            distorted = len(re.findall(r"\bDISTORTED\b", raw, re.IGNORECASE))
        if unsupported is None:
            unsupported = len(re.findall(r"\bUNSUPPORTED\b", raw, re.IGNORECASE))
        if missing is None:
            missing = len(re.findall(r"\bMISSING.ATTRIBUTION\b", raw, re.IGNORECASE))

        header_match = re.search(r"Claims\s*checked\D*(\d+)", raw, re.IGNORECASE)
        if header_match:
            header_total = int(header_match.group(1))
        else:
            header_total = None

        issues = []
        for match in re.finditer(
            r"(?:####?\s*Issue\s*\d+|(?:^|\n)\d+\.\s*\*\*)[^\n]*\n(.*?)(?=(?:####?\s*Issue|(?:^|\n)\d+\.\s*\*\*)|\Z)",
            raw, re.DOTALL,
        ):
            block = match.group(1)
            claim = re.search(r"\*\*Claim[^*]*\*\*[:\s]*(.+)", block)
            classification = re.search(r"\*\*Classification\*\*[:\s]*(.+)", block)
            if claim:
                issues.append(FidelityIssue(
                    claim=claim.group(1).strip().strip('"'),
                    classification=classification.group(1).strip() if classification else "unknown",
                ))

        total = verified + distorted + unsupported + missing
        if header_total and header_total > total:
            total = header_total

        if total == 0:
            return FidelityResult(
                claims_checked=0,
                verified=0,
                issues=[FidelityIssue(
                    claim="Fidelity check produced unparseable output",
                    classification="RETRY",
                )],
            )

        return FidelityResult(
            claims_checked=total,
            verified=verified,
            distorted=distorted,
            unsupported=unsupported,
            missing_attribution=missing,
            issues=issues,
        )
