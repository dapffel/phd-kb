---
title: "Predicting into unknown space? Estimating the area of applicability of spatial prediction models"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - meyer2021-area-of-applicability.pdf
---

## Citation
Meyer, H. & Pebesma, E. (2021) Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Methods in Ecology and Evolution*, 12(9), 1620–1633. doi: 10.1111/2041-210X.13650

## TL;DR
Machine learning models for spatial mapping can only be reliably applied where prediction environments resemble training data. The authors propose the "area of applicability" (AOA), delineated via a dissimilarity index (DI) that measures weighted distance in predictor space from new locations to the nearest training data. Within the AOA, cross-validation error holds; outside it, predictions are unreliable.

## Key Concepts
- [[area-of-applicability]] — the geographic area where a trained model can be expected to perform comparably to its cross-validation error estimate
- [[dissimilarity-index]] — DI: standardised minimum Euclidean distance to nearest training point in the weighted predictor space; values >1 indicate greater dissimilarity than the average training-data pair
- [[model-extrapolation]] — the core problem: spatial prediction beyond training data environments, where ML models are especially unreliable
- [[spatial-cross-validation]] — the AOA threshold is derived from cross-validation, and the choice of CV strategy (random vs. spatial) directly determines both the performance estimate and the size of the AOA
- [[model-transferability]] — AOA provides a principled way to assess whether a model trained in one region can be applied in another
- [[species-distribution-models]] — one of the key application domains; AOA addresses concerns about SDM reliability in novel environments

## Methodology
The authors define the DI as the minimum Euclidean distance from a new prediction location to the nearest training data point in a scaled, variable-importance-weighted predictor space, normalised by the average pairwise distance between training points. The AOA threshold is the outlier-removed maximum DI observed across cross-validation folds of the training data. Predictions are shown only within the AOA. A further extension maps DI-dependent performance estimates using the relationship between DI and cross-validated RMSE via a shape-constrained additive model. The method was validated using 972 simulated scenarios mimicking ecological spatial prediction tasks with bioclimatic predictors across Europe, and illustrated with both randomly distributed and spatially clustered sampling designs using Random Forest models.

## Key Findings
1. Across 972 simulations, prediction error within the AOA was comparable to the cross-validation error of the trained model, while outside the AOA, prediction error was substantially higher.
2. The DI correlated well with true absolute prediction error (r = 0.71 in the case study), unlike Random Forest ensemble standard deviations, which showed spatial patterns unrelated to the true error.
3. Weighting predictor variables by their model importance improved the DI's agreement with true error compared to unweighted distances (r = 0.71 vs. 0.62).
4. The AOA depends on the cross-validation strategy: spatial CV yields a larger AOA (with correspondingly higher but more realistic error estimates) than random CV on clustered data.
5. A quantitative uncertainty map can be produced by modelling the DI–RMSE relationship, allowing users to restrict predictions to areas meeting a specified performance threshold.
6. The relationship between DI and performance was well captured by shape-constrained additive models (R² = 0.82–0.83).
7. The method applies to any supervised prediction model (not just Random Forest) because it operates in predictor space, not model-internal space.

## Limitations
- Validated only on simulated data where the response is a clear function of predictors; for weak prediction tasks, DI may be less informative because missing predictor coverage is not the dominant error source.
- The AOA provides no guarantee that predictions within it are reliable — unmeasured factors can still affect the response.
- The method considers only predictor-space novelty, not changes in predictor–response relationships (e.g., due to non-stationarity).
- Only Euclidean distance is used; other distance metrics or non-linear manifold-based approaches are not explored.
- The outlier-removal threshold (1.5× IQR) for the DI is a heuristic that may not be optimal in all settings.

## Connections
- The DI is related to but distinct from the [[mess-analysis]] (MESS) of [[elith2010-range-shifting]]: MESS identifies univariate extrapolation and novel combinations, while DI is a single multivariate distance metric weighted by variable importance.
- Directly addresses the [[model-extrapolation]] concerns raised by [[elith2009-sdm-review]] regarding the reliability of SDMs in novel environments.
- The dependence of AOA on cross-validation strategy connects to [[roberts2017-cross-validation]]'s analysis of how blocking strategy affects error estimation.
- Relevant to [[guisan2013-sdm-conservation]]'s argument that SDM uncertainty must be quantified for conservation decisions — AOA maps provide spatially explicit uncertainty.

## Open Questions
- How should the AOA approach be adapted for models that explicitly account for spatial autocorrelation (e.g., spatial random effects)?
- Can the DI be extended to detect changes in predictor–response relationships (non-stationarity) beyond simple distance in predictor space?
- What is the optimal balance between AOA conservatism and spatial coverage for conservation planning applications?
- How does the AOA framework perform with very high-dimensional predictor spaces typical of remote sensing applications?
