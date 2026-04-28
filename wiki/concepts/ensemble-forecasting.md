---
title: "Ensemble Forecasting"
created: 2026-04-28
updated: 2026-04-28
type: concept
sources:
  - araujo2007-ensemble-forecasting.pdf
  - elith2009-sdm-review.pdf
  - thuiller2005-climate-change-plants.pdf
  - efron1993-bootstrap.pdf
---

## Definition
Ensemble forecasting in species distribution modelling is the practice of running multiple models — varying in algorithm, parameterisation, initial conditions, or climate scenario — and combining their outputs to produce more robust predictions than any single model alone. The combined forecast has lower mean error than individual forecasts, provided individual models contain some independent information.

## Background
The approach was imported into ecology from meteorology and economics, where combining forecasts had long been shown to outperform individual predictions (Bates and Granger, 1969). In species distribution modelling, the impetus came from the observation that different modelling techniques applied to the same species and data can yield dramatically different projections — for South African plants, nine models predicted range changes from −92% to +322% for the same species ([[araujo2007-ensemble-forecasting]]). This inter-model variability makes single-model reliance untenable for conservation decisions.

## How It Works
Ensembles can vary along four axes ([[araujo2007-ensemble-forecasting]]):

1. **Initial Conditions (IC)**: different starting datasets (e.g., different sampling of occurrences).
2. **Model Class (MC)**: different algorithms (GLM, GAM, BRT, MaxEnt, neural networks, etc.).
3. **Model Parameters (MP)**: different settings within the same algorithm (e.g., regularisation values, number of trees).
4. **Boundary Conditions (BC)**: different climate scenarios or GCMs.

**Three approaches to analysing ensembles:**

| Approach | Description | Use case |
|----------|-------------|----------|
| **Bounding box** | Full range of predictions without averaging | Conservative risk assessment |
| **Consensus** | Central tendency (mean or median) of ensemble | General-purpose; guaranteed better than ≥50% of members |
| **Probabilistic** | Construct probability distributions from large ensembles | Comprehensive uncertainty quantification |

The BIOMOD framework ([[thuiller2005-climate-change-plants]]) implements ensemble forecasting operationally by running four modelling techniques (GLM, GAM, classification trees, neural networks) and selecting the most consensual projection via PCA.

Conceptually, ensemble forecasting shares logic with [[bootstrap-resampling]] ([[efron1993-bootstrap]]): both use repeated sampling/modelling to estimate the variability of a statistic or prediction.

## Key Results From Sources
- **[[araujo2007-ensemble-forecasting]]**: Combined forecasts yield lower mean error than any individual forecast. A simple consensus (median) implementation reduced false-negative errors from an average of 50% to 0% for British breeding birds. Ensemble forecasting complements rather than replaces the effort to build better individual models.
- **[[thuiller2005-climate-change-plants]]**: The BIOMOD ensemble of four SDM techniques, combined via consensus PCA, projected >50% of 1,350 European plant species as vulnerable by 2080. Scenario variability (across GCMs and IPCC storylines) was substantial: 27–42% mean species loss.
- **[[elith2009-sdm-review]]**: Ensemble approaches referenced as model averaging/consensus for reducing uncertainty. Machine learning methods can outperform classical methods individually, but the ensemble framework provides robustness across methods.
- **[[efron1993-bootstrap]]**: Bootstrap resampling provides a general framework for estimating uncertainty via repeated computation — the same logic underlying ensemble prediction, applied to statistical inference.

## Open Problems
- When does weighting ensemble members (e.g., Bayesian model averaging based on cross-validation performance) outperform simple unweighted consensus?
- Even large ensembles only sparsely sample the IC–MC–MP–BC combination space, so resulting probability distributions remain conditional on the sampling strategy.
- Ensemble uncertainty captures inter-model variability but not systematic biases shared by all models (e.g., all correlative models ignoring biotic interactions).
- How to communicate ensemble results to conservation decision-makers who may lack statistical training.
- At what ensemble size does the marginal value of adding more models or parameterisations diminish?

## Related Concepts
- [[species-distribution-models]]
- [[model-uncertainty]]
- [[model-evaluation]]
- [[climate-change-biodiversity]]
- [[bootstrap-resampling]]
- [[bounding-box-forecasting]]
- [[consensus-forecasting]]
- [[probabilistic-forecasting]]
