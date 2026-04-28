---
title: "Model Evaluation"
created: 2026-04-28
updated: 2026-04-28
type: concept
sources:
  - allouche2006-tss-accuracy.pdf
  - elith2009-sdm-review.pdf
  - roberts2017-cross-validation.pdf
  - elith2010-range-shifting.pdf
---

## Definition
Model evaluation in the context of species distribution modelling encompasses the methods and metrics used to assess how well a model's predictions match observed data, and whether its performance estimates are reliable for the intended application. It includes the choice of accuracy metrics (AUC, TSS, kappa), the data-splitting strategy (random vs. block cross-validation), and the interpretation of performance in the context of the modelling objective (interpolation vs. extrapolation).

## Background
Model evaluation has been contentious in the SDM field. Early practice relied on resubstitution (testing on training data) or random hold-out splits, both of which overestimate performance on structured ecological data ([[roberts2017-cross-validation]]). The choice of metric has also been debated: kappa was long standard but is prevalence-dependent ([[allouche2006-tss-accuracy]]), AUC is threshold-independent but has been criticised for equating commission and omission errors, and TSS was introduced as a prevalence-free alternative. [[elith2009-sdm-review]] noted that progress has been impeded by arguments about the general validity of individual statistics rather than identifying the proper use of each.

## How It Works
**Accuracy metrics** for presence–absence predictions:

| Metric | Formula | Prevalence-dependent? | Threshold-dependent? |
|--------|---------|----------------------|---------------------|
| Kappa | Agreement corrected for chance | Yes (unimodal bias) | Yes |
| TSS | Sensitivity + Specificity − 1 | No | Yes |
| AUC | Area under ROC curve | No | No |
| Sensitivity | TP / (TP + FN) | No | Yes |
| Specificity | TN / (TN + FP) | No | Yes |

TSS ranges from −1 to +1, where +1 indicates perfect agreement and 0 indicates no better than random ([[allouche2006-tss-accuracy]]).

**Cross-validation strategies:**

- **Random k-fold CV**: splits data randomly. Appropriate only when data have no dependence structure and the goal is interpolation.
- **Spatial block CV**: groups data into spatially contiguous blocks. Reduces spatial autocorrelation between folds and provides error estimates relevant to spatial prediction ([[roberts2017-cross-validation]]).
- **Temporal / group / phylogenetic blocking**: analogous strategies for other dependence structures.
- **Buffered leave-one-out**: removes observations within a buffer distance around each test point.

The choice of CV strategy directly affects both the performance estimate and the derived area of applicability ([[meyer2021-area-of-applicability]]).

**Key insight from [[elith2010-range-shifting]]**: cross-validated AUC on current data does not predict which model will perform best under future climate conditions. Good current-climate evaluation does not guarantee good extrapolation.

## Key Results From Sources
- **[[allouche2006-tss-accuracy]]**: Kappa responds unimodally to prevalence; TSS is independent of prevalence and correlates more strongly with AUC (r = 0.85) than kappa does (r = 0.65). TSS should replace kappa as the standard threshold-dependent metric.
- **[[elith2009-sdm-review]]**: Model evaluation is fragmented across the field. Diverse opinions exist on which properties matter most. The authors argue for matching evaluation methods to the specific application rather than seeking a single best metric.
- **[[roberts2017-cross-validation]]**: Random CV consistently underestimates prediction error on structured data. Block CV provides estimates closer to the true independent-data error. Even models that account for spatial autocorrelation parametrically (e.g., spatial autoregressive models) still benefit from block CV because structural overfitting through correlated predictors can persist.
- **[[elith2010-range-shifting]]**: AUC evaluated on current-climate hold-out data did not predict agreement between correlative and mechanistic models under climate change. This challenges the assumption that good current-climate evaluation implies reliable projections.

## Open Problems
- No consensus on which metric(s) should be standard across the field.
- Optimal block size for spatial CV as a function of autocorrelation range, extent, and sample size remains unresolved.
- How to evaluate models when the goal is extrapolation to genuinely novel conditions, where no independent test data exist.
- The relationship between threshold-independent (AUC) and threshold-dependent (TSS) metrics needs clearer guidance for practitioners.
- Evaluation of ensemble predictions raises additional questions about whether to evaluate the ensemble output or individual member models.

## Related Concepts
- [[species-distribution-models]]
- [[true-skill-statistic]]
- [[block-cross-validation]]
- [[spatial-cross-validation]]
- [[model-extrapolation]]
- [[area-of-applicability]]
- [[auc-roc]]
