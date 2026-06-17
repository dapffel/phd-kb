import json

from langgraph.graph import StateGraph, END

from agents.llm import invoke
from agents.models import CatalogEntry, CatalogResult, CatalogState
from agents.sub_agents.base import BaseAgent


EXTRACT_METADATA_PROMPT = """You are a research paper metadata extractor. Given the first pages of a PDF, extract:

Return ONLY valid JSON (no markdown fencing):
{
  "title": "Full paper title",
  "authors": ["LastName1", "LastName2"],
  "year": 0,
  "keywords": ["keyword1", "keyword2", "keyword3"]
}

Extract 3-5 keywords describing the paper's topic. Use lowercase."""


class CatalogAgent(BaseAgent[CatalogState]):
    state_schema = CatalogState

    def build_graph(self) -> StateGraph:
        g = StateGraph(CatalogState)
        g.add_node("scan", self.scan)
        g.add_node("process", self.process)
        g.set_entry_point("scan")
        g.add_edge("scan", "process")
        g.add_edge("process", END)
        return g

    def scan(self, state: CatalogState) -> dict:
        return {"new_files": self.vault.unprocessed_pdfs()}

    def process(self, state: CatalogState) -> dict:
        new_files = state.new_files
        if not new_files:
            result = CatalogResult(
                total=len(self.vault.load_catalog()),
                report="No new PDFs found.",
            )
            return {"entries_added": 0, "report": result.report, "result": result}

        catalog = self.vault.load_catalog()
        added_entries: list[CatalogEntry] = []

        for filename in new_files:
            text = self.vault.extract_pdf(filename)
            raw = invoke(EXTRACT_METADATA_PROMPT, text[:3000])

            try:
                meta = json.loads(raw)
            except json.JSONDecodeError:
                continue

            entry = CatalogEntry(
                filename=filename,
                title=meta.get("title", filename),
                authors=meta.get("authors", []),
                year=meta.get("year", 0),
                keywords=meta.get("keywords", []),
                extracted=self.vault.has_extract(filename),
                ingested=self.vault.has_summary(filename),
            )
            catalog.append(entry)
            added_entries.append(entry)

        self.vault.save_catalog(catalog)
        report = f"Added {len(added_entries)} new entries. Catalog total: {len(catalog)}."
        result = CatalogResult(
            entries_added=len(added_entries),
            total=len(catalog),
            entries=added_entries,
            report=report,
        )
        return {
            "entries_added": len(added_entries),
            "report": report,
            "result": result,
        }
