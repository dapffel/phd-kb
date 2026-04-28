---
title: "Ensemble forecasting of species distributions"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - araujo2007-ensemble-forecasting.pdf
---

## Citation
Araújo, M.B. and New, M. (2007) Ensemble forecasting of species distributions. *Trends in Ecology and Evolution*, 22(1), 42–47. doi: 10.1016/j.tree.2006.09.010

## TL;DR
Projections of species distributions under climate change vary so widely across modelling techniques that single-model forecasts can be unreliable for policy decisions. The authors advocate an ensemble forecasting framework — running multiple models and combining their outputs via bounding box, consensus, or probabilistic approaches — to produce more robust predictions.

## Key Concepts
- [[ensemble-forecasting]] — central framework proposed; combining multiple model outputs to reduce forecast uncertainty
- [[species-distribution-models]] — the class of correlative (bioclimatic envelope) models whose inter-model variability motivates the ensemble approach
- [[model-uncertainty]] — the paper's core problem; different models yield dramatically different range-shift predictions for the same species
- [[consensus-forecasting]] — one of three ensemble combination strategies; uses central tendency (mean or median) of ensemble members
- [[bounding-box-forecasting]] — conservative ensemble strategy that identifies the full range of predictions without averaging
- [[probabilistic-forecasting]] — the "end game" of ensemble analysis; constructs probability distributions from large ensembles
- [[climate-change-biodiversity]] — the applied domain; ensemble methods are needed to support conservation planning under climate uncertainty

## Methodology
This is a review and opinion piece, not an empirical study. The authors survey the ensemble forecasting literature across disciplines (economics, meteorology, climatology) and apply the framework to bioclimatic modelling of species distributions. They draw on published case studies — particularly Pearson et al. (2006) on South African plants, Thuiller et al. (2004) on European plants, Araújo et al. (2006) on European amphibians and reptiles, and Araújo et al. (2005) on British breeding birds — to illustrate the scale of inter-model disagreement and the benefits of ensemble approaches. The paper defines the four axes of variation that generate ensembles: initial conditions (IC), model classes (MC), model parameters (MP), and boundary conditions (BC).

## Key Findings
1. Predicted distribution changes from nine bioclimatic models applied to the same South African plant species ranged from a 92% loss to a 322% gain, demonstrating that single-model reliance is untenable.
2. Combined forecasts yield lower mean error than any individual constituent forecast, provided individual forecasts contain some independent information (Bates and Granger, 1969).
3. Consensus forecasting (median of ensemble) is guaranteed to be more accurate than at least half of the individual forecasts, regardless of the distribution of predictions.
4. A simple consensus implementation reduced false-negative errors from an average of 50% to 0% in predictions of distribution shifts among British breeding birds.
5. Three distinct approaches to analysing ensembles — bounding box, consensus, and probabilistic — are suited to different questions and risk tolerances.
6. Ensemble forecasting complements rather than replaces the effort to build better individual models; better individual forecasts yield better combined forecasts.
7. The most comprehensive ensemble studies at the time had spawned no more than 40 projections per species, but climate modelling developments would rapidly push this to thousands.

## Limitations
- The paper is a review advocating a framework, not a systematic empirical comparison of ensemble methods against single models across many taxa.
- Probabilistic forecasting requires very large ensembles (tens of thousands of simulations) that were not yet feasible for species distribution modelling at the time of writing.
- Even large ensembles only sparsely sample the possible IC–MC–MP–BC combination space, so resulting PDFs remain conditional on the sampling strategy.
- The authors acknowledge uncertainty about whether model stability (where adding more ensemble members stops changing the forecast distribution) can ever truly be achieved.
- The paper focuses on correlative bioclimatic envelope models; process-based models are mentioned but not deeply addressed.
- Practical software infrastructure for running and combining large ensembles was identified as a major bottleneck.

## Connections
- Relates to [[biomod]] (Thuiller, 2003) as an early software platform for multi-model species distribution modelling.
- The four uncertainty axes (IC, MC, MP, BC) connect to broader [[uncertainty-quantification]] frameworks in ecological modelling.
- The conservation planning discussion links to [[reserve-selection]] under climate change (Araújo et al., 2004).
- TODO: connect to any sources in the wiki on specific ensemble methods (random forests, boosted regression trees, MAXENT).

## Open Questions
- When does weighting ensemble members (e.g., Bayesian model averaging) outperform simple unweighted consensus?
- How should ensemble results be communicated to conservation decision-makers who may lack statistical training?
- Can hybrid approaches combining bounding box with consensus or probabilistic forecasting improve decision-making?
- At what ensemble size does the marginal value of adding more models or parameterisations diminish?
- How do ensemble approaches perform when extrapolating to novel (non-analogue) climates where all constituent models may be equally wrong?
