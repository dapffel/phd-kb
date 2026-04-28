---
title: "Synthesis: When Can We Trust an SDM?"
created: 2026-04-28
updated: 2026-04-28
type: connection
sources:
  - allouche2006-tss-accuracy.pdf
  - araujo2007-ensemble-forecasting.pdf
  - elith2009-sdm-review.pdf
  - elith2010-range-shifting.pdf
  - guisan2013-sdm-conservation.pdf
  - meyer2021-area-of-applicability.pdf
  - roberts2017-cross-validation.pdf
  - peterson2011-niches-distributions.pdf
---

## Overview
The question of when a species distribution model's predictions can be trusted runs through the entire SDM literature. Eight sources in this wiki address different facets of the problem — from the choice of accuracy metric to the delineation of geographic areas where predictions hold. Together, they reveal a field that has progressively discovered layers of overconfidence in its own outputs, and is still building the tools to correct for them.

## State of Knowledge

The reliability of an SDM depends on a chain of decisions, each of which can introduce false confidence. The chain starts with the accuracy metric: [[allouche2006-tss-accuracy]] showed that kappa, for years the standard, is prevalence-dependent — it systematically favours models of species at intermediate prevalence, regardless of true skill. Replacing kappa with TSS (Sensitivity + Specificity − 1) removes this bias, but the metric itself is only as meaningful as the data used to compute it.

That data-splitting problem is where [[roberts2017-cross-validation]] delivers its central warning: random cross-validation on structured ecological data consistently underestimates prediction error. The mechanism is twofold. First, spatial autocorrelation makes nearby hold-out points non-independent from training data, inflating apparent skill. Second — and more insidiously — models can overfit the dependence structure itself by absorbing spatial patterns through correlated predictors, a process that escapes detection precisely because it reduces residual autocorrelation. Block cross-validation addresses both problems by forcing evaluation on structurally independent data, but introduces its own complication: when spatial blocks correlate with environmental gradients, blocking inadvertently induces extrapolation between folds, potentially overestimating interpolation error.

Even with appropriate cross-validation, a model's current-climate performance says little about its reliability under novel conditions. [[elith2010-range-shifting]] demonstrated this directly: among four SDM methods applied to the cane toad invasion, cross-validated AUC on current data did not predict which model agreed best with a mechanistic benchmark under future climates. Models that performed identically on current data diverged wildly in their projections. The implication is stark: good evaluation scores are necessary but not sufficient for trusting projections.

The question then becomes: *where* in geographic space can we trust the projection? Two complementary tools address this. The MESS diagnostic ([[elith2010-range-shifting]]) flags locations where any predictor variable takes values outside the training-data range or enters novel multivariate combinations. The dissimilarity index and area of applicability (DI/AOA; [[meyer2021-area-of-applicability]]) go further — weighting predictor distances by their importance in the model, and deriving a threshold from cross-validation that delineates the area where the estimated model error holds. Outside the AOA, prediction error is dramatically and unpredictably higher.

Ensemble forecasting offers a different response to unreliability: if no single model is trustworthy, combine many. [[araujo2007-ensemble-forecasting]] showed that a simple consensus (median of ensemble members) reduced false-negative errors from 50% to 0% for British breeding birds. But ensembles capture inter-model variability, not systematic errors shared by all correlative models — a limitation [[guisan2013-sdm-conservation]] highlights when noting that ensemble GCM projections address only climate scenario uncertainty, leaving SDM construction, data quality, and goodness-of-fit as additional, often ignored, uncertainty sources.

Ultimately, [[guisan2013-sdm-conservation]] argues that the trustworthiness question cannot be answered in isolation from the decision context. False positives and false negatives carry different costs depending on the conservation application. For invasive species at the pre-border stage, false negatives (missing an invasion) are far more costly than false positives (flagging a non-invasion). This means that the acceptable level of model unreliability is decision-dependent — and that SDM uncertainty must be propagated into the decision framework, not merely reported alongside predictions.

## Approaches and Positions

### Approach A: Fix the evaluation pipeline
[[allouche2006-tss-accuracy]] and [[roberts2017-cross-validation]] focus on getting more honest performance estimates from the same models. Their argument: much of the apparent reliability problem is actually a measurement problem. If we use prevalence-independent metrics and structure-aware cross-validation, we get a more truthful picture of model skill — which in most cases is lower than previously reported, but at least accurately so. The fix is methodological: better evaluation practices applied to existing modelling workflows.

### Approach B: Delineate where predictions are trustworthy
[[elith2010-range-shifting]] and [[meyer2021-area-of-applicability]] accept that models have a limited domain of applicability and focus on mapping that domain explicitly. Rather than asking "how good is this model?" they ask "where is this model good?" The tools — MESS and DI/AOA — flag or mask regions where predictions cannot be trusted, transforming a global performance number into a spatially explicit reliability map.

### Approach C: Combine models to hedge against individual failure
[[araujo2007-ensemble-forecasting]] addresses unreliability by diversifying across models, parameterisations, and scenarios. The logic is borrowed from forecasting theory: combined predictions have lower mean error than individual ones, provided the models contain some independent information. The emphasis is on robustness through redundancy rather than perfection of any single model.

### Approach D: Embed SDMs in decision frameworks
[[guisan2013-sdm-conservation]] argues that the reliability question is incomplete without the decision context. A model that is "unreliable" for one application may be fit for purpose in another, depending on the relative costs of false positives and false negatives. The solution is not better models alone but structured decision-making that explicitly incorporates model uncertainty and its consequences.

## Comparison

| Dimension | Fix evaluation (A) | Map applicability (B) | Ensemble (C) | Decision framing (D) |
|-----------|-------------------|----------------------|--------------|---------------------|
| Core claim | We overestimate skill via biased metrics and CV | Predictions are only valid where training data support them | Combining models is more robust than trusting any one | Trustworthiness is relative to the decision's error costs |
| Key tool | TSS, block CV | MESS, DI/AOA maps | BIOMOD, ensemble consensus | Structured decision-making, Marxan/Zonation |
| What it fixes | Inflated performance estimates | Silent extrapolation into novel environments | Single-model instability | Disconnect between models and decisions |
| What it doesn't fix | Whether any model is reliable under novel conditions | The quality of predictions within the AOA | Systematic biases shared by all models | The models themselves |
| Temporal scope | Retrospective (evaluation of existing predictions) | Prospective (flagging unreliable future projections) | Both | Prospective (planning under uncertainty) |

## Agreements

All sources converge on several points:

1. **Standard evaluation practices overstate SDM reliability.** Whether through prevalence-biased metrics ([[allouche2006-tss-accuracy]]), random CV on structured data ([[roberts2017-cross-validation]]), or current-climate AUC applied to future projections ([[elith2010-range-shifting]]), the field's default evaluation practices produce optimistic estimates.

2. **Extrapolation is qualitatively different from interpolation.** This is stated explicitly by [[elith2009-sdm-review]], operationalised by [[elith2010-range-shifting]] and [[meyer2021-area-of-applicability]], grounded theoretically by [[peterson2011-niches-distributions]] (non-analogue environments are expected, not anomalous), and accommodated in the cross-validation framework by [[roberts2017-cross-validation]].

3. **No single model should be trusted in isolation.** Whether the remedy is ensemble combination ([[araujo2007-ensemble-forecasting]]), spatially explicit reliability mapping ([[meyer2021-area-of-applicability]]), or decision-theoretic framing ([[guisan2013-sdm-conservation]]), all sources reject the idea that a single correlative model with a good AUC is sufficient.

4. **Uncertainty must be communicated, not hidden.** Every source that touches on applications emphasises that unquantified uncertainty is the biggest barrier to SDM utility.

## Disagreements

The sources do not directly contradict each other, but they differ in emphasis in ways that matter:

- **Metric reform vs. structural reform:** [[allouche2006-tss-accuracy]] implies that better metrics (TSS over kappa) substantially improve evaluation. [[roberts2017-cross-validation]] argues that even with perfect metrics, the data-splitting strategy dominates — the metric is secondary to whether the hold-out data are truly independent. [[elith2010-range-shifting]] goes further: even with the right metric and the right CV, current-climate evaluation doesn't predict future reliability. These represent an escalating critique, each subsuming the previous.

- **Masking vs. projecting with uncertainty:** [[meyer2021-area-of-applicability]] advocates masking predictions outside the AOA (show nothing rather than show unreliable predictions). [[araujo2007-ensemble-forecasting]] and [[guisan2013-sdm-conservation]] implicitly favour showing predictions everywhere but with uncertainty bounds attached. The choice depends on whether unreliable predictions with caveats are more dangerous than visible gaps in coverage.

- **Model complexity for extrapolation:** [[elith2010-range-shifting]] found smoother models (fewer parameters) extrapolated better. This is in some tension with the general machine learning literature and with the high-complexity models that dominate current SDM practice. No other source in the wiki directly addresses this tension.

## Gaps

1. **No empirical comparison of MESS vs. DI/AOA.** Both diagnose extrapolation, but via different mechanisms (univariate minimum similarity vs. weighted multivariate distance). Whether they flag the same regions or capture complementary aspects of novelty is untested.

2. **No guidance on combining the four approaches.** The evaluation, applicability-mapping, ensemble, and decision-framing approaches are presented independently. A practical workflow integrating all four — "use block CV with TSS, restrict to the AOA, report ensemble spread, frame uncertainty for the decision" — does not exist in the literature reviewed.

3. **Non-stationarity remains unaddressed.** All extrapolation diagnostics assume that the species–environment relationship is stable and ask only whether the environment is novel. None detects situations where the relationship itself has changed (e.g., a species evolving new thermal tolerance, or a new competitor arriving).

4. **Temporal extrapolation is underserved.** Most tools focus on spatial prediction. The specific challenges of projecting to future climates — including cascading uncertainty from GCM to downscaling to SDM — are acknowledged by [[guisan2013-sdm-conservation]] but not addressed mechanistically.

5. **Biotic interactions are the elephant in the room.** [[peterson2011-niches-distributions]] formalises their role (the B in BAM), [[elith2009-sdm-review]] identifies them as a critical gap, and no source offers a practical solution for incorporating them into correlative models at geographic scales.

## Open Questions for Further Research

1. Can a unified reliability framework combine block CV, AOA mapping, and ensemble uncertainty into a single "trustworthiness surface" for SDM predictions?
2. What is the empirical relationship between MESS novelty scores and DI values — do they agree on which regions are unreliable?
3. How should the AOA framework be extended to detect non-stationarity in species–environment relationships, not just novelty in predictor space?
4. At what model complexity level does the trade-off between current-climate fit and extrapolation reliability tip — and is this consistent across taxa and regions?
5. Can the decision-theoretic framework of [[guisan2013-sdm-conservation]] be operationalised into a tool that automatically adjusts SDM confidence thresholds based on the cost structure of the conservation decision?
