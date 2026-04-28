---
title: "Model Extrapolation"
created: 2026-04-28
updated: 2026-04-28
type: concept
sources:
  - elith2009-sdm-review.pdf
  - elith2010-range-shifting.pdf
  - meyer2021-area-of-applicability.pdf
  - roberts2017-cross-validation.pdf
  - peterson2011-niches-distributions.pdf
---

## Definition
Model extrapolation is the application of a fitted model to environmental conditions outside those represented in the training data. In species distribution modelling, this arises when projecting to new geographic regions, future climates, or environments occupied by range-shifting species. Extrapolation is inherently riskier than interpolation because training data cannot directly support predictions in novel environments.

## Background
The interpolation–extrapolation distinction is fundamental to SDM reliability ([[elith2009-sdm-review]]). Most SDMs are calibrated on current distributions under current climate, then projected to future scenarios or new regions — conditions that may include environmental combinations never observed during training. This problem is amplified for machine learning models, which can fit highly complex relationships but offer no reliable behaviour outside their training domain ([[meyer2021-area-of-applicability]]). The problem was formalised early in the niche modelling literature through the concept of non-analogue environments — climate combinations that exist in the projection domain but have no counterpart in the calibration domain ([[peterson2011-niches-distributions]]).

## How It Works
Extrapolation occurs along two dimensions:

1. **Univariate novelty**: a predictor variable takes values outside the range observed in training data (e.g., temperature exceeding any training-data maximum).
2. **Multivariate novelty**: predictor combinations are unprecedented even if individual variables are within range (e.g., a hot-wet combination never observed together).

**Diagnostic tools:**
- **MESS** (Multivariate Environmental Similarity Surface): identifies where projections involve novel environments by computing, for each prediction location, the minimum similarity across all predictors to the training data ([[elith2010-range-shifting]]). Negative MESS values indicate extrapolation.
- **DI/AOA** (Dissimilarity Index / Area of Applicability): measures the weighted Euclidean distance in predictor space from a new location to the nearest training point, normalised by average training-data distances ([[meyer2021-area-of-applicability]]). The AOA threshold delineates where the cross-validation error estimate is expected to hold.

**Model behaviour under extrapolation** varies by algorithm. Smoother models (fewer trees in BRT, higher regularisation in MaxEnt) extrapolate more consistently with mechanistic predictions, while complex models may produce erratic responses in novel environments ([[elith2010-range-shifting]]).

**Block cross-validation** can deliberately induce extrapolation between folds by withholding entire environmental gradients, providing error estimates relevant to the extrapolation task ([[roberts2017-cross-validation]]). However, blocking that inadvertently removes environmental space from training folds can overestimate interpolation error.

## Key Results From Sources
- **[[elith2009-sdm-review]]**: Prediction takes two forms — interpolation to unsampled sites (usually reliable) and extrapolation to new domains/climates (violates key SDM assumptions). Proximal predictors produce more reliable extrapolations because their relationships with species are mechanistically grounded.
- **[[elith2010-range-shifting]]**: Models that performed similarly under current climate diverged widely under climate change. Cross-validated AUC did not predict which model extrapolated best. Smoother fits produced projections most consistent with the mechanistic benchmark. The MESS diagnostic flagged extensive areas of environmental novelty invisible to standard evaluation.
- **[[meyer2021-area-of-applicability]]**: Outside the AOA, prediction error was dramatically higher than within it. The DI correlated well with true prediction error (r = 0.71), unlike Random Forest ensemble uncertainty measures that failed to capture novelty-driven error.
- **[[roberts2017-cross-validation]]**: Blocking in space or time can induce extrapolation in cross-validation folds, which is desirable when the modelling goal is extrapolation but problematic when it is not. The "forecast horizon" concept quantifies the dissimilarity threshold beyond which predictions become too unreliable.
- **[[peterson2011-niches-distributions]]**: The fundamental niche may include environmental combinations not currently existing in the study region. Extrapolation into these non-analogue environments is a theoretical expectation, not just a practical nuisance.

## Open Problems
- No consensus on how to handle predictions in novel environments: should they be flagged, masked, or constrained?
- Whether MESS and DI/AOA capture the same or complementary aspects of environmental novelty.
- How to detect non-stationarity — changes in species–environment relationships, not just novel predictor values.
- The appropriate level of model complexity (smoothness) for extrapolation remains context-dependent with no general rule.
- Integrating mechanistic constraints into correlative models to improve extrapolation reliability.

## Related Concepts
- [[species-distribution-models]]
- [[area-of-applicability]]
- [[mess-analysis]]
- [[model-evaluation]]
- [[model-uncertainty]]
- [[non-equilibrium-species]]
- [[fundamental-niche]]
