import json

import pytest


class TestCatalogCRUD:
    def test_load_empty_catalog(self, vault):
        entries = vault.load_catalog()
        assert entries == []

    def test_save_and_load(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        loaded = vault.load_catalog()
        assert len(loaded) == 3
        assert loaded[0].filename == "smith2020-attention.pdf"
        assert loaded[1].ingested is False

    def test_mark_ingested(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        vault.mark_ingested("doe2021-climate.pdf")
        loaded = vault.load_catalog()
        doe = next(e for e in loaded if e.filename == "doe2021-climate.pdf")
        assert doe.ingested is True
        assert doe.extracted is True

    def test_catalog_md_regenerated(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        from agents.config import settings
        md = settings.catalog_md.read_text()
        assert "total: 3" in md
        assert "smith2020-attention.pdf" not in md  # title is shown, not filename
        assert "Attention in Ecology" in md

    def test_mark_ingested_missing_filename_is_noop(self, vault, sample_catalog_entries):
        vault.save_catalog(sample_catalog_entries)
        vault.mark_ingested("nonexistent.pdf")
        loaded = vault.load_catalog()
        assert len(loaded) == 3


class TestExtractDetection:
    def test_has_extract_false(self, vault):
        assert vault.has_extract("nonexistent.pdf") is False

    def test_has_extract_true(self, vault):
        from agents.config import settings
        (settings.papers_dir / "test.md").write_text("extracted content")
        assert vault.has_extract("test.pdf") is True

    def test_has_summary_false(self, vault):
        assert vault.has_summary("nonexistent.pdf") is False

    def test_has_summary_true(self, vault):
        from agents.config import settings
        (settings.wiki_dir / "summaries" / "test.md").write_text("summary")
        assert vault.has_summary("test.pdf") is True


class TestWikiStats:
    def test_empty_wiki(self, vault):
        stats = vault.stats()
        assert stats.summaries == 0
        assert stats.concepts == 0
        assert stats.total_words == 0

    def test_counts_articles(self, vault):
        from agents.config import settings
        (settings.wiki_dir / "summaries" / "paper-a.md").write_text(
            "---\ntitle: A\ncreated: 2024-01-01\nupdated: 2024-01-01\ntype: summary\nsources: [a]\n---\n"
            "Some words here about [[concept-x]] and [[concept-y]]."
        )
        (settings.wiki_dir / "concepts" / "concept-x.md").write_text(
            "---\ntitle: X\ncreated: 2024-01-01\nupdated: 2024-01-01\ntype: concept\nsources: [a]\n---\n"
            "Definition of concept-x. See [[paper-a]]."
        )
        stats = vault.stats()
        assert stats.summaries == 1
        assert stats.concepts == 1
        assert stats.total_words > 0
        assert "concept-y" in stats.broken_links

    def test_orphaned_detection(self, vault):
        from agents.config import settings
        (settings.wiki_dir / "summaries" / "orphan.md").write_text(
            "---\ntitle: O\ncreated: 2024-01-01\nupdated: 2024-01-01\ntype: summary\nsources: [o]\n---\n"
            "No links here."
        )
        stats = vault.stats()
        assert "orphan" in stats.orphaned


class TestIndexRegeneration:
    def test_regenerate_wiki_index(self, vault):
        from agents.config import settings
        (settings.wiki_dir / "summaries" / "alpha.md").write_text("---\ntitle: A\n---\n")
        (settings.wiki_dir / "summaries" / "beta.md").write_text("---\ntitle: B\n---\n")

        vault.regenerate_wiki_index()
        content = settings.wiki_index.read_text()
        assert "[[alpha]]" in content
        assert "[[beta]]" in content


class TestUnprocessedPdfs:
    def test_detects_uncataloged_pdfs(self, vault):
        from agents.config import settings
        (settings.papers_dir / "new-paper.pdf").write_text("fake pdf")
        result = vault.unprocessed_pdfs()
        assert "new-paper.pdf" in result

    def test_excludes_cataloged(self, vault, sample_catalog_entries):
        from agents.config import settings
        vault.save_catalog(sample_catalog_entries)
        (settings.papers_dir / "smith2020-attention.pdf").write_text("fake pdf")
        result = vault.unprocessed_pdfs()
        assert "smith2020-attention.pdf" not in result


class TestExtractPdf:
    def test_file_not_found(self, vault):
        with pytest.raises(FileNotFoundError, match="PDF not found"):
            vault.extract_pdf("nonexistent.pdf")
