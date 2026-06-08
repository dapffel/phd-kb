from agents.commands import find_catalog, init_vault


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
