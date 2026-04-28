---
title: "An Introduction to the Bootstrap"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - efron1993-bootstrap.pdf
---

## Citation
Efron, B. & Tibshirani, R.J. (1993) *An Introduction to the Bootstrap*. Chapman & Hall/CRC. ISBN: 0-412-04231-2.

**Note:** Only an excerpt (front matter, introduction, and Chapter 2) was available. This summary is based on that excerpt and does not cover the full book.

## TL;DR
The bootstrap is a computer-based resampling method for assessing statistical accuracy (standard errors, confidence intervals, bias) that works for any computable statistic, eliminating the need for analytical formulas. Invented by Efron in 1979, it generates many resampled datasets from the original data, computes the statistic on each, and uses the variability across replicates to estimate the statistic's accuracy.

## Key Concepts
- [[bootstrap-resampling]] — core method; sampling with replacement from observed data to estimate sampling distributions
- [[standard-error]] — the most common measure of an estimator's accuracy; bootstrap provides estimates even when no formula exists
- [[confidence-intervals]] — bootstrap methods include bootstrap-t, percentile method, and BCa (bias-corrected accelerated)
- [[cross-validation]] — discussed alongside bootstrap for prediction error estimation
- [[jackknife]] — a closed-form approximation to the bootstrap for standard error and bias estimation
- [[statistical-inference]] — the broader framework; bootstrap is a computer-based implementation of classical inference concepts

## Methodology
The bootstrap algorithm: (1) Given data x = (x₁, ..., xₙ) and statistic s(x), draw B bootstrap samples x* by sampling n items with replacement from x. (2) Compute s(x*) for each. (3) The standard deviation of the B replications estimates the standard error of s(x). B = 50–200 suffices for standard errors; more for confidence intervals. The method is illustrated with a mouse survival experiment (7 treatment, 9 control) where bootstrap estimates the standard error of the median (37.83), for which no simple formula exists.

## Key Findings
1. For the sample mean, the bootstrap standard error converges to the classical formula s/√n as B grows large.
2. The bootstrap enables accuracy assessment for any computable statistic, including medians, regression coefficients, and principal components.
3. The computational cost is roughly 100× that of computing the statistic once — affordable with modern computers.
4. Bootstrap confidence intervals require additional computation (×10 beyond standard errors) but extend inference to complex settings.
5. The method is distribution-free — it does not require assumptions about the underlying population distribution.

## Limitations
- Only an excerpt of the book was available; the full treatment of confidence intervals (BCa), regression applications, and advanced theory is not covered in this summary.
- The bootstrap can fail when the statistic is not smooth or when the data structure has dependencies not captured by simple resampling (e.g., time series, spatial data — though the book addresses some of these in later chapters).
- Computational cost, while manageable, scales with B × n and can be substantial for very large datasets.

## Connections
- Bootstrap resampling is foundational to [[cross-validation]] methods used in [[model-evaluation]] of [[species-distribution-models]].
- The jackknife (Chapter 11 of the book) relates to leave-one-out cross-validation used in SDM evaluation.
- [[ensemble-forecasting]] in ecology uses related ideas of combining multiple model runs.
- TODO: connect to specific SDM papers that use bootstrap for uncertainty estimation.

## Open Questions
- How does the bootstrap perform for spatially structured ecological data where independence assumptions are violated?
- What are the best bootstrap variants for presence-absence species distribution models?
- How does bootstrap-based uncertainty compare to Bayesian posterior uncertainty in SDM applications?
