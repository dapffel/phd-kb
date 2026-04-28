---
title: "The art of modelling range-shifting species"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - elith2010-range-shifting.pdf
---

## Citation
Elith, J., Kearney, M. & Phillips, S.J. (2010) The art of modelling range-shifting species. *Methods in Ecology and Evolution*, 1(4), 330–342. doi: 10.1111/j.2041-210X.2010.00036.x

## TL;DR
Species undergoing range shifts (via invasion or climate change) violate two core SDM assumptions: equilibrium with environment and representative training data. Using the cane toad (*Bufo marinus*) invasion of Australia as a case study, the authors test four correlative SDM methods and show that data treatment choices (background selection, weighting) matter more than model algorithm, and that smoother model fits extrapolate more reliably to novel climates.

## Key Concepts
- [[model-extrapolation]] — central challenge; correlative models trained on current ranges must predict into environmental conditions not represented in training data
- [[species-distribution-models]] — four methods compared: GLM, GAM, BRT, MaxEnt
- [[non-equilibrium-species]] — species not yet occupying all climatically suitable habitat, violating the equilibrium assumption underlying most SDMs
- [[mess-analysis]] — multivariate environmental similarity surface; new tool for quantifying where projections involve extrapolation into novel environments
- [[mechanistic-models]] — biophysical models used as benchmark; NicheMapper predictions of cane toad physiological limits served as reference for evaluating correlative model extrapolations
- [[model-complexity]] — smoother fits (fewer trees in BRT, higher regularisation in MaxEnt) produced climate-change projections most consistent with mechanistic model predictions
- [[background-selection]] — choice of absence/background data influenced predictions more than choice of modelling algorithm under current climate

## Methodology
The authors modelled the Australian distribution of the invasive cane toad using four correlative SDM methods (GLM, GAM, BRT, MaxEnt) with varying data treatments: different background sample extents, weighting schemes for presence vs. background points, and complexity settings. Predictions were evaluated against independent invasion records and against outputs from NicheMapper, a mechanistic biophysical model of cane toad thermal physiology. Two methods for integrating mechanistic information into correlative models were tested: using mechanistic predictions to define absences, and including mechanistic-derived proximal variables as predictors. New diagnostic tools (MESS maps, limiting-factor maps, prediction-component exploration) were implemented in MaxEnt 3.3.2.

## Key Findings
1. Under current climate, predictions varied more with data treatment (especially absence/background choice) than with modelling method — pairwise correlations between methods using the same background samples were all >0.9.
2. Under climate change scenarios, models that performed similarly for current climates diverged widely in their future projections.
3. Cross-validated AUC on current data did not predict which model would agree best with the mechanistic model under future climates.
4. Smoother model fits (fewer trees in BRT, higher regularisation in MaxEnt) produced climate-change predictions most consistent with mechanistic predictions.
5. Using absences drawn from mechanistic model predictions improved predictions in the northern (expanding) range.
6. Including proximal predictors derived from the mechanistic model as covariates caused only subtle changes to predictions despite being selected as important.
7. The MESS diagnostic revealed extensive areas of environmental novelty in projected future climate space that standard evaluation metrics would not flag.

## Limitations
- The study uses a single species (cane toad) as a case study; generalisability to other taxa and geographic contexts is untested.
- The mechanistic model benchmark is itself a model with its own assumptions and errors, not ground truth.
- The study does not address biotic interactions, dispersal limitations, or evolutionary adaptation.
- Only four correlative methods were compared; other approaches (e.g., random forests, neural networks) were not included.
- Climate change projections relied on a single GCM scenario rather than an ensemble.

## Connections
- Directly extends [[elith2009-sdm-review]] (same lead author) by addressing the extrapolation problem identified as a key challenge in that review.
- The MESS diagnostic connects to the [[model-uncertainty]] and [[model-extrapolation]] concerns raised by [[araujo2007-ensemble-forecasting]].
- The finding that current-climate AUC does not predict future performance challenges evaluation approaches discussed in [[allouche2006-tss-accuracy]].
- The integration of mechanistic and correlative models relates to [[guisan2013-sdm-conservation]]'s call for combining SDMs with population dynamics models for conservation decisions.

## Open Questions
- How should modellers choose the appropriate level of model complexity (smoothness) when extrapolating to novel environments?
- Can the MESS framework be extended to flag not just environmental novelty but also where specific response shapes are unreliable?
- Under what conditions does integrating mechanistic and correlative models yield meaningful improvements over either alone?
- How should background/pseudo-absence selection be standardised for non-equilibrium species?
