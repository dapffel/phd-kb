from unittest import mock

from agents.models import FidelityResult, IngestState, Reference
from agents.sub_agents.ingest.graph import IngestAgent


class TestParseFidelity:
    def _parse(self, raw: str) -> FidelityResult:
        agent = IngestAgent.__new__(IngestAgent)
        return agent._parse_fidelity(raw)

    def test_standard_format(self):
        raw = """## Eval Report
**Claims checked**: 5
**Verified**: 4 | **Distorted**: 1 | **Unsupported**: 0 | **Missing attribution**: 0

### Issues

#### Issue 1: overstated claim
- **Claim in article**: "The authors found X significantly improves Y"
- **Classification**: DISTORTED
- **Source says**: "X shows modest improvements"
- **Suggested fix**: "X shows modest improvements in Y"
"""
        r = self._parse(raw)
        assert r.claims_checked == 5
        assert r.verified == 4
        assert r.distorted == 1
        assert len(r.issues) == 1
        assert r.issues[0].classification == "DISTORTED"
        assert r.passed is False

    def test_all_verified(self):
        raw = """## Eval Report
**Claims checked**: 3
**Verified**: 3 | **Distorted**: 0 | **Unsupported**: 0 | **Missing attribution**: 0

### Summary
All claims verified.
"""
        r = self._parse(raw)
        assert r.claims_checked == 3
        assert r.verified == 3
        assert r.distorted == 0
        assert r.unsupported == 0
        assert r.passed is True

    def test_unparseable_returns_retry(self):
        raw = "This is some random text with no fidelity markers at all."
        r = self._parse(raw)
        assert r.claims_checked == 0
        assert len(r.issues) == 1
        assert r.issues[0].classification == "RETRY"
        assert r.passed is False

    def test_header_total_overrides_count(self):
        raw = """**Claims checked**: 10
VERIFIED: claim 1.
VERIFIED: claim 2.
"""
        r = self._parse(raw)
        assert r.claims_checked == 10
        assert r.verified == 2

    def test_multiple_issues(self):
        raw = """
**Claims checked**: 5
**Verified**: 3 | **Distorted**: 1 | **Unsupported**: 1

#### Issue 1: first
- **Claim in article**: "Claim A"
- **Classification**: DISTORTED

#### Issue 2: second
- **Claim in article**: "Claim B"
- **Classification**: UNSUPPORTED
"""
        r = self._parse(raw)
        assert len(r.issues) == 2
        assert r.passed is False


class TestExtractReferences:
    def _run(self, llm_response: str) -> dict:
        agent = IngestAgent.__new__(IngestAgent)
        state = IngestState(source_text="some paper text")
        with mock.patch("agents.sub_agents.ingest.graph.invoke", return_value=llm_response):
            with mock.patch("agents.sub_agents.ingest.graph.load_prompt", return_value="prompt"):
                return agent.extract_references(state)

    def test_valid_json(self):
        raw = '[{"author": "Smith", "year": 2020, "title": "A paper"}]'
        result = self._run(raw)
        assert len(result["references"]) == 1
        assert result["references"][0].author == "Smith"
        assert result["references"][0].year == 2020

    def test_multiple_refs(self):
        raw = '[{"author": "Elith", "year": 2009, "title": "SDM"}, {"author": "Thuiller", "year": 2005, "title": "Plants"}]'
        result = self._run(raw)
        assert len(result["references"]) == 2

    def test_invalid_json_returns_empty(self):
        result = self._run("This is not JSON at all")
        assert result["references"] == []

    def test_markdown_fenced_json(self):
        raw = '```json\n[{"author": "Smith", "year": 2020, "title": "Test"}]\n```'
        result = self._run(raw)
        assert len(result["references"]) == 1
        assert result["references"][0].author == "Smith"

    def test_empty_list(self):
        result = self._run("[]")
        assert result["references"] == []

    def test_missing_fields_skipped(self):
        raw = '[{"author": "Smith", "year": 2020}, {"badkey": "val"}]'
        result = self._run(raw)
        assert len(result["references"]) == 1


class TestRouteFidelity:
    def test_passes_go_to_save(self):
        from agents.models import IngestState
        agent = IngestAgent.__new__(IngestAgent)
        state = IngestState(
            fidelity=FidelityResult(claims_checked=5, verified=5),
            attempts=1,
        )
        assert agent.route_fidelity(state) == "save"

    def test_fails_go_to_fix(self):
        from agents.models import IngestState
        agent = IngestAgent.__new__(IngestAgent)
        state = IngestState(
            fidelity=FidelityResult(claims_checked=5, verified=4, distorted=1),
            attempts=1,
        )
        assert agent.route_fidelity(state) == "fix_summary"

    def test_max_attempts_go_to_save(self):
        from agents.models import IngestState
        agent = IngestAgent.__new__(IngestAgent)
        state = IngestState(
            fidelity=FidelityResult(claims_checked=5, verified=4, distorted=1),
            attempts=3,
        )
        assert agent.route_fidelity(state) == "save"
