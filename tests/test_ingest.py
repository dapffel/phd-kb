from agents.models import FidelityResult
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
