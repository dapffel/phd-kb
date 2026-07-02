import json

from langgraph.graph import StateGraph, END

from agents.llm import invoke
from agents.models import CatalogEntry, CatalogResult, CatalogState
from agents.sub_agents.base import BaseAgent


EXTRACT_METADATA_PROMPT = """You are a document metadata extractor for a pizza restaurant operations system.
Given the first pages of a document (supplier invoice, price list, recipe card, or operations doc), extract:

Return ONLY valid JSON (no markdown fencing):
{
  "title": "Document title or description",
  "authors": ["SupplierName or Author"],
  "year": 0,
  "keywords": ["keyword1", "keyword2", "keyword3"]
}

Rules:
- "title" = descriptive title (e.g., "Farina Caputo Price List Q2 2026", "Margherita Recipe Card")
- "authors" = supplier name, vendor, or author (e.g., ["Caputo"], ["Casa Mozzarella"])
- "year" = document year as integer
- "keywords" = 3-5 lowercase tags describing content (e.g., "flour", "pricing", "dough", "inventory")"""


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
