from agents.models import FidelityIssue, FidelityResult, CatalogEntry, Reference, WikiStats


class TestFidelityResult:
    def test_passed_when_no_issues(self):
        r = FidelityResult(claims_checked=5, verified=5)
        assert r.passed is True

    def test_fails_with_distorted(self):
        r = FidelityResult(claims_checked=5, verified=4, distorted=1)
        assert r.passed is False

    def test_fails_with_unsupported(self):
        r = FidelityResult(claims_checked=5, verified=4, unsupported=1)
        assert r.passed is False

    def test_passes_with_missing_attribution_only(self):
        r = FidelityResult(claims_checked=5, verified=4, missing_attribution=1)
        assert r.passed is True

    def test_empty_result_passes(self):
        r = FidelityResult()
        assert r.passed is True

    def test_serialization_roundtrip(self):
        r = FidelityResult(
            claims_checked=3,
            verified=2,
            distorted=1,
            issues=[FidelityIssue(claim="test claim", classification="DISTORTED")],
        )
        data = r.model_dump()
        r2 = FidelityResult.model_validate(data)
        assert r2.claims_checked == 3
        assert r2.issues[0].claim == "test claim"
        assert r2.passed is False


class TestCatalogEntry:
    def test_defaults(self):
        e = CatalogEntry(filename="test.pdf", title="T", authors=["A"], year=2020, keywords=["k"])
        assert e.extracted is False
        assert e.ingested is False

    def test_serialization(self):
        e = CatalogEntry(filename="test.pdf", title="T", authors=["A", "B"], year=2020,
                         keywords=["k1", "k2"], extracted=True, ingested=True)
        data = e.model_dump()
        assert data["filename"] == "test.pdf"
        assert data["extracted"] is True
        e2 = CatalogEntry.model_validate(data)
        assert e2.title == "T"


class TestReference:
    def test_defaults(self):
        r = Reference(author="Smith", year=2020)
        assert r.title == ""

    def test_serialization_roundtrip(self):
        r = Reference(author="Araújo", year=2006, title="Five challenges for SDMs")
        data = r.model_dump()
        r2 = Reference.model_validate(data)
        assert r2.author == "Araújo"
        assert r2.year == 2006
        assert r2.title == "Five challenges for SDMs"

    def test_list_serialization(self):
        refs = [
            Reference(author="Elith", year=2009, title="SDM review"),
            Reference(author="Thuiller", year=2005),
        ]
        data = [r.model_dump() for r in refs]
        restored = [Reference.model_validate(d) for d in data]
        assert len(restored) == 2
        assert restored[0].author == "Elith"
        assert restored[1].title == ""


class TestWikiStats:
    def test_defaults(self):
        s = WikiStats()
        assert s.summaries == 0
        assert s.broken_links == []
        assert s.missing_concepts == []
