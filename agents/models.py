from datetime import date
from pydantic import BaseModel, Field


# --- Domain models ---

class CatalogEntry(BaseModel):
    filename: str
    title: str
    authors: list[str]
    year: int
    keywords: list[str]
    extracted: bool = False
    ingested: bool = False


class FidelityIssue(BaseModel):
    claim: str
    classification: str


class FidelityResult(BaseModel):
    claims_checked: int = 0
    verified: int = 0
    distorted: int = 0
    unsupported: int = 0
    missing_attribution: int = 0
    issues: list[FidelityIssue] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        if self.claims_checked == 0 and self.issues:
            return False
        return self.distorted == 0 and self.unsupported == 0


class WikiArticle(BaseModel):
    path: str
    title: str
    type: str
    sources: list[str] = Field(default_factory=list)
    created: date | None = None
    updated: date | None = None
    content: str = ""


class WikiStats(BaseModel):
    summaries: int = 0
    concepts: int = 0
    connections: int = 0
    total_words: int = 0
    broken_links: list[str] = Field(default_factory=list)
    orphaned: list[str] = Field(default_factory=list)
    missing_concepts: list[str] = Field(default_factory=list)


class Reference(BaseModel):
    author: str
    year: int
    title: str = ""


class CatalogResult(BaseModel):
    entries_added: int = 0
    total: int = 0
    entries: list[CatalogEntry] = Field(default_factory=list)
    report: str = ""


class IngestResult(BaseModel):
    source_filename: str
    summary_path: str = ""
    fidelity: FidelityResult = Field(default_factory=FidelityResult)
    detected_concepts: list[str] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)
    attempts: int = 0


class BrokenLink(BaseModel):
    link: str
    suggestion: str


class LintResult(BaseModel):
    broken_links: list[BrokenLink] = Field(default_factory=list)
    orphaned: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    stale: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    missing_frontmatter: list[str] = Field(default_factory=list)


# --- Agent states ---

class SupervisorState(BaseModel):
    command: str = "status"
    args: str = ""
    output: str = ""


class IngestState(BaseModel):
    filename: str = ""
    source_text: str = ""
    summary: str = ""
    fidelity: FidelityResult = Field(default_factory=FidelityResult)
    attempts: int = 0
    detected_concepts: list[str] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)
    result: IngestResult | None = None


class CatalogState(BaseModel):
    new_files: list[str] = Field(default_factory=list)
    entries_added: int = 0
    report: str = ""
    result: CatalogResult | None = None


class CompileState(BaseModel):
    concept_names: list[str] = Field(default_factory=list)
    created: list[str] = Field(default_factory=list)
    updated: list[str] = Field(default_factory=list)
    report: str = ""


class SynthesizeState(BaseModel):
    topic: str = ""
    relevant_articles: list[str] = Field(default_factory=list)
    synthesis: str = ""
    report: str = ""


class LintState(BaseModel):
    result: LintResult | None = None
    report: str = ""


class QueryState(BaseModel):
    question: str = ""
    context: list[str] = Field(default_factory=list)
    answer: str = ""


class EvalState(BaseModel):
    filename: str = ""
    eval_report: str = ""
    report: str = ""


class StatusState(BaseModel):
    report: str = ""
