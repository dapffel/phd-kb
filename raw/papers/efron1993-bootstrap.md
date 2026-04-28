# An Introduction to the Bootstrap

**Authors:** Bradley Efron, Robert J. Tibshirani
**Publisher:** Chapman & Hall/CRC
**Year:** 1993
**ISBN:** 0-412-04231-2

**Note:** Only an excerpt (11 pages covering front matter, introduction, and Chapter 2) was available in the PDF. This summary is based on that excerpt.

## Overview

The bootstrap is a computer-based method for assigning measures of accuracy to statistical estimates, invented by Efron in 1979. It is a data-based simulation method for statistical inference that can produce confidence intervals and standard error estimates automatically, even in complex situations.

## Core Idea

Given observed data x = (x₁, x₂, ..., xₙ) and a statistic of interest s(x):

1. Generate a bootstrap sample x* by randomly sampling n times, with replacement, from the original data
2. Compute the bootstrap replication s(x*)
3. Repeat B times (B = 50–200 for standard errors, more for confidence intervals)
4. The bootstrap estimate of standard error is the standard deviation of the B bootstrap replications

## Key Properties

- Works for any computable statistic s(x), not just the sample mean
- For the sample mean, the bootstrap standard error converges to the classical formula s/√n
- Enables accuracy assessment for statistics where no analytical formula exists (e.g., median, regression coefficients)
- Price: ~100× increase in computation (affordable with modern computers)

## Book Structure (from synopsis)

- Chapters 1–5: Introduction and background (random samples, empirical distribution, standard errors)
- Chapter 6: Bootstrap definition for estimating standard errors
- Chapters 7–9: Applications (principal components, curve fitting, regression)
- Chapters 10–11: Bias estimation and the jackknife
- Chapters 12–14: Bootstrap confidence intervals (bootstrap-t, percentile method, BCa)
- Chapters 15–16: Permutation tests and hypothesis testing
- Chapters 17–18: Prediction error estimation, cross-validation
- Chapter 19: Jackknife-after-bootstrap
- Chapters 20–25: Advanced topics (resampling, non-parametric inference, efficient computation, approximate likelihoods)
- Chapter 26: General issues

## Illustrative Example (from excerpt)

Mouse survival experiment: 16 mice (7 treatment, 9 control). Treatment group mean = 86.86 days, control = 56.22 days, difference = 30.63. Standard error of difference = 28.93, so difference is only 1.05 standard errors from zero — not statistically significant. Bootstrap applied to estimate standard error of the median (37.83 for B→∞), which has no simple analytical formula.
