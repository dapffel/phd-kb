---
title: "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - roberts2017-cross-validation.pdf
---

## Citation
Roberts, D.R., Bahn, V., Ciuti, S., Boyce, M.S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J.J., Schröder, B., Thuiller, W., Warton, D.I., Wintle, B.A., Hartig, F. & Dormann, C.F. (2017) Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, 40(8), 913–929. doi: 10.1111/ecog.02881

## TL;DR
Random cross-validation on structured ecological data consistently underestimates prediction error because it does not account for dependence structures (spatial, temporal, hierarchical, phylogenetic). Block cross-validation — splitting data strategically along these structures — provides more realistic error estimates and is recommended even when no autocorrelation is visible in model residuals, because overfitting to dependence structure can mask the problem.

## Key Concepts
- [[block-cross-validation]] — splitting data into blocks along dependence structures (spatial, temporal, group, phylogenetic) rather than randomly, to achieve more independent training–test splits
- [[spatial-autocorrelation]] — nearby observations being more similar than distant ones; creates non-independence that random CV ignores
- [[model-evaluation]] — central topic; random CV is shown to produce overly optimistic performance estimates for structured data
- [[overfitting]] — two distinct problems: non-independence of residuals, and models absorbing structured residual variation via correlated predictors (structural overfitting)
- [[spatial-cross-validation]] — blocking by contiguous geographic space; forces evaluation on spatially distant records, reducing spatial dependence
- [[model-extrapolation]] — blocking in space or time can inadvertently induce extrapolation by restricting predictor-space coverage in training folds
- [[forecast-horizon]] — conceptual framework for the threshold dissimilarity beyond which model predictions become too unreliable to use

## Methodology
This is a review, simulation, and case-study paper. The authors review the ecological literature on non-random cross-validation, then present four demonstration analyses: (1) a spatial simulation on a 50×50 grid modelled with Random Forest, comparing resubstitution, random CV, spatial block CV, and buffered leave-one-out; (2) elk resource selection functions with blocking by individual animals; (3) phylogenetic blocking for comparative analyses; (4) blocking in predictor space for extrapolation assessment. Each demonstration compares random CV error estimates against blocked CV estimates and, where possible, against true independent prediction error.

## Key Findings
1. Random cross-validation on structured data consistently underestimates prediction error, sometimes dramatically (resubstitution and random CV both produced error estimates far below the true independent-data error in the spatial simulation).
2. Block cross-validation produces error estimates closer to the true error for predictions to new structures (new locations, new time periods, new individuals, new clades).
3. Even models that explicitly account for dependence structures (spatial autoregressive models, mixed models, PGLS) still benefit from block CV because structural overfitting through correlated predictors can persist.
4. Blocking can inadvertently induce extrapolation when dependence structures correlate with environmental gradients (e.g., latitude–temperature), potentially overestimating interpolation error.
5. For the elk resource selection case, blocking by individual animals revealed much lower and more variable model performance than random CV, even when mixed models were used.
6. The "forecast horizon" concept provides a framework for determining the limit of model applicability by testing performance across increasingly dissimilar blocks.
7. The price of slightly conservative validation (blocking when not strictly necessary) is small compared to the cost of false confidence from random CV.

## Limitations
- The demonstrations are illustrative rather than exhaustive; optimal block size and strategy remain context-dependent and under-explored.
- When data are scarce or cover limited spatial/temporal extent, achieving independence between blocks may be impossible.
- Irregular sampling can lead to blocks with highly variable sample sizes or prevalence, complicating error estimation.
- The paper does not address how structural overfitting affects parameter estimation or causal inference, focusing primarily on predictive error.
- No single blocking strategy is universally optimal — the choice requires understanding of both the data structure and the modelling objective.

## Connections
- Directly relevant to [[model-evaluation]] — challenges the standard use of random CV for SDMs, connecting to the evaluation discussions in [[allouche2006-tss-accuracy]] and [[elith2009-sdm-review]].
- The spatial blocking recommendations inform how the AOA threshold should be derived in [[meyer2021-area-of-applicability]], since the AOA depends on the CV strategy used.
- The extrapolation concern from blocking connects to [[model-extrapolation]] and the MESS framework of [[elith2010-range-shifting]].
- The finding that current-data CV does not reflect future performance echoes [[elith2010-range-shifting]]'s result that cross-validated AUC did not predict agreement with mechanistic models under climate change.
- The ensemble-model perspective in [[araujo2007-ensemble-forecasting]] would benefit from block CV to avoid overestimating individual model skill.

## Open Questions
- What is the optimal block size for spatial CV as a function of autocorrelation range, spatial extent, and sample size?
- How should block CV be implemented for species with complex movement patterns that span multiple spatial blocks?
- Can adaptive blocking strategies (data-driven block size selection) be developed that balance independence against predictor-space coverage?
- How does the choice of blocking strategy interact with ensemble model selection and weighting?
