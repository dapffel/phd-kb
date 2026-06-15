from agents.commands import (
    build_citation_network,
    find_catalog,
    init_vault,
    match_reference_to_catalog,
    suggest_reading,
)
from agents.models import CatalogEntry, Reference


class TestFindCatalog:
    def test_matches_title(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = find_catalog(vault, "attention")
        assert "Attention in Ecology" in result
        assert "smith2020" not in result or "Smith" in result

    def test_matches_keyword(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = find_catalog(vault, "climate")
        assert "Climate Impacts" in result

    def test_matches_author(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = find_catalog(vault, "doe")
        assert "Climate Impacts" in result

    def test_no_match(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = find_catalog(vault, "quantum computing")
        assert "No catalog matches" in result

    def test_case_insensitive(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = find_catalog(vault, "ATTENTION")
        assert "Attention in Ecology" in result

    def test_empty_query(self, vault):
        result = find_catalog(vault, "")
        assert "Usage" in result

    def test_flags_not_ingested(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = find_catalog(vault, "climate")
        assert "not ingested" in result.lower() or "not been ingested" in result.lower()


class TestInitVault:
    def test_idempotent(self, vault):
        report1, changed1 = init_vault()
        report2, changed2 = init_vault()
        assert changed2 is False


class TestMatchReferenceToCatalog:
    def _catalog(self):
        return [
            CatalogEntry(
                filename="elith2009-sdm.pdf", title="SDM Review",
                authors=["Elith", "Leathwick"], year=2009, keywords=["sdm"],
            ),
            CatalogEntry(
                filename="thuiller2005-plants.pdf", title="Plants Under Climate Change",
                authors=["Thuiller", "Lavorel"], year=2005, keywords=["plants"],
            ),
        ]

    def test_first_author_match(self):
        ref = {"author": "Elith", "year": 2009}
        assert match_reference_to_catalog(ref, self._catalog()).filename == "elith2009-sdm.pdf"

    def test_case_insensitive(self):
        ref = {"author": "elith", "year": 2009}
        assert match_reference_to_catalog(ref, self._catalog()) is not None

    def test_second_author_match(self):
        ref = {"author": "Lavorel", "year": 2005}
        match = match_reference_to_catalog(ref, self._catalog())
        assert match is not None
        assert match.filename == "thuiller2005-plants.pdf"

    def test_no_match_wrong_year(self):
        ref = {"author": "Elith", "year": 2020}
        assert match_reference_to_catalog(ref, self._catalog()) is None

    def test_no_match_wrong_author(self):
        ref = {"author": "Nobody", "year": 2009}
        assert match_reference_to_catalog(ref, self._catalog()) is None

    def test_missing_fields_returns_none(self):
        assert match_reference_to_catalog({"author": "Elith"}, self._catalog()) is None
        assert match_reference_to_catalog({"year": 2009}, self._catalog()) is None
        assert match_reference_to_catalog({}, self._catalog()) is None


class TestBuildCitationNetwork:
    def test_generates_file(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        summary_content = (
            '---\ntitle: "Test Paper"\ntype: summary\n'
            'references:\n  - author: Doe\n    year: 2021\n    title: Climate\n---\n\nContent.\n'
        )
        vault.save_article("summaries", "smith2020-attention.md", summary_content)
        result = build_citation_network(vault)
        assert "citation-network.md" in result.lower() or "cross-citation" in result.lower()
        network_path = vault.root / "wiki" / "connections" / "citation-network.md"
        assert network_path.exists()

    def test_empty_vault(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = build_citation_network(vault)
        assert "0" in result or "papers" in result.lower()


class TestSuggestReading:
    def test_no_summaries_returns_message(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        result = suggest_reading(vault)
        assert "no frequently" in result.lower() or "need >= 2" in result.lower()

    def test_finds_frequent_external_refs(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        ref_block = (
            '  - author: External\n    year: 2018\n    title: Some paper\n'
        )
        for name in ["paper-a.md", "paper-b.md"]:
            content = (
                f'---\ntitle: "{name}"\ntype: summary\n'
                f'references:\n{ref_block}---\n\nContent.\n'
            )
            vault.save_article("summaries", name, content)
        result = suggest_reading(vault)
        assert "External" in result or "external" in result.lower()
