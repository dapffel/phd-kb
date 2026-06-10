---
title: "Assessing the reliability of species distribution projections in climate change research"
created: 2026-06-03
updated: 2026-06-03
type: summary
sources:
  - santini2021-sdm-reliability
---

## Citation

Santini L, Benítez-López A, Maiorano L, Čengić M, Huijbregts MAJ (2021) Assessing the reliability of species distribution projections in climate change research. Diversity and Distributions, 27:1035–1050. DOI: 10.1111/ddi.13252

## TL;DR

A literature review of 250 SDM papers (2015–2019) reveals widespread poor practices (small samples, no biological variable selection, split-sample-only validation, routine binarization). A virtual species simulation with GLM, MaxEnt, and random forest shows that split-sample validation consistently over-estimates true predictive accuracy, binarization severely degrades predictions, and violations of equilibrium and random-sampling assumptions inflate estimated accuracy while decreasing real accuracy — meaning many published SDM-based climate change forecasts may be unreliable.

## Key Concepts

- [[species-distribution-models]] — the paper directly evaluates the reliability of SDMs as climate change projection tools
- [[model-evaluation]] — central focus: split-sample vs. spatial block validation, AUC vs. TSS, estimated vs. true accuracy
- [[model-extrapolation]] — future projections perform worse than present predictions, especially when environmental dissimilarity is high
- [[virtual-species]] — methodological approach using simulated species with known truth to benchmark SDM performance
- [[sample-size]] — one of the strongest predictors of true (but not estimated) accuracy; asymptotic improvement stabilising around 200–500 points
- [[binarization]] — converting continuous suitability to presence/absence dramatically reduces predictive ability and should be avoided for range change quantification

## Methodology

Two-part study. First, a literature review of 250 randomly selected SDM papers from Web of Science (2015–2019), of which 92 projected models to different time periods. Second, a virtual species simulation: 50 species generated with known niches (6 bioclimatic variables, Gaussian tolerances), projected under present and future (2050, RCP 8.5, CHELSA 0.1° resolution) conditions. Seven treatment dimensions were crossed (sample size 10–1,000; sample prevalence; background extent; environmental bias; niche filling; 0–6 relevant predictors; 0–6 irrelevant predictors), yielding 500 model settings sampled via conditional Latin hypercube from 7,560 combinations. Three algorithms tested: GLM (stepwise AIC), MaxEnt (cloglog, linear + quadratic), random forest (500 trees). Validation by both split-sample (80/20, 10 repeats) and spatial block (3×3 leave-one-out). True accuracy measured against the known virtual distribution.

## Key Findings

1. In the literature review, 65% of studies relied on single models, 62% used N < 50 presence points, 85% used presence-only data, 74% binarized outputs, and 94% used split-sample validation only.
2. Split-sample validation consistently over-estimates true predictive accuracy for both present and future predictions.
3. Spatial block validation provides a more honest estimate of future accuracy, except when datasets are environmentally biased.
4. Binarization of predicted probabilities reduces predictive ability considerably: true TSS is substantially lower than true AUC.
5. Sample size is one of the main predictors of true model accuracy but has little influence on estimated (cross-validated) accuracy; the relationship is asymptotic, stabilising around 200–500 points.
6. Including ecologically irrelevant predictors increases estimated accuracy but decreases true accuracy, leading to biased estimates of range contraction and expansion.
7. Violations of equilibrium and random-sampling assumptions increase estimated accuracy while decreasing true accuracy — a "false sense of accuracy."
8. GLM and MaxEnt work best with low sample prevalence (many background points); random forest works best with high sample prevalence.
9. Environmental similarity between present and future conditions is an important predictor of projection accuracy; highly dissimilar futures yield the poorest predictions.
10. Even under optimal settings with full ecological knowledge, future binary predictions show low discrimination ability.

## Limitations

- Virtual species have perfectly Gaussian niches along known axes — real species have more complex niche shapes and unknown true niches.
- Only three algorithms tested (GLM, MaxEnt, RF); ensemble approaches and newer methods (e.g., GBMs, joint SDMs) not evaluated.
- Niche filling was simulated only via human footprint; real non-equilibrium arises from diverse causes (dispersal limitation, biotic interactions) that may affect models differently.
- Study area extents in the simulation (330–1,100 km) may not capture the full range of scales used in real studies.
- Only RCP 8.5 (high-emission) tested for future projections; lower emission scenarios with less climate dissimilarity might yield different performance patterns.

## Connections

- Directly supports the argument in [[roberts2017-cross-validation]] that random CV under-estimates error on structured data; Santini et al. go further to show that even spatial block validation is not a panacea when data are environmentally biased.
- Reinforces the importance of the accuracy metric critique in [[allouche2006-tss-accuracy]]: TSS-based binary discrimination performs far worse than AUC on continuous outputs, especially for future projections.
- The finding that environmental dissimilarity degrades projections connects to the non-analog climate problem in [[fitzpatrick2009-non-analog-climate]] and [[williams2007-novel-climates]] — novel climates are precisely where models perform worst.
- The model transferability concern aligns with [[meyer2021-area-of-applicability]]: predictions outside the area of applicability are unreliable, and Santini et al. show this quantitatively via the MESS-based environmental similarity predictor.
- The observation that irrelevant predictors inflate estimated accuracy echoes concerns in [[elith2010-range-shifting]] about smoother models and careful variable selection for extrapolation.
- The recommendation to avoid binarization and instead examine probability trends is relevant to conservation applications discussed in [[guisan2013-sdm-conservation]].

## Open Questions

- Can validation approaches be developed that are robust to both spatial non-independence and environmental bias simultaneously?
- What is the real-world distribution of SDM true accuracy across published studies, given that most use the practices shown here to be problematic?
- How should conservation decisions be made when even well-constructed SDMs have low true predictive accuracy for future distributions?
- Could ensemble approaches that weight models by transferability (e.g., MESS-based weighting) meaningfully improve projection reliability?
