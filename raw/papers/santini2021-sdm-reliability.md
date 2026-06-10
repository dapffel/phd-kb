# Assessing the reliability of species distribution projections in climate change research

**Authors:** Luca Santini, Ana Benítez-López, Luigi Maiorano, Mirza Čengić, Mark A. J. Huijbregts
**Journal:** Diversity and Distributions (2021) 27:1035–1050
**DOI:** 10.1111/ddi.13252
**Type:** Biodiversity Research

---

## Abstract

Forecasting changes in species distribution under future scenarios is one of the most prolific areas of application for species distribution models (SDMs). However, no consensus yet exists on the reliability of such models for drawing conclusions on species' distribution response to changing climate. The authors provide an overview of common modelling practices (literature review of 250 papers, 2015–2019) and assess the reliability of model predictions using a virtual species approach with three SDM algorithms (GLM, MaxEnt, random forest).

## Literature review (2015–2019)

Among 250 papers reviewed, 92 included correlative SDMs projected to different time periods. Key findings:

- 65% relied on single models; MaxEnt was the most common (78.3%), followed by GLM (30.4%), GAM (26.1%), RF (27.2%), GBM (20.7%)
- 62% used small sample sizes (N < 50); only 18.4% had minimum samples > 50
- 85% used presence-only data (with pseudo-absences or background points)
- 74% binarized model output (e.g., max TSS threshold)
- 94% used split-sample validation; only 3% used spatial block validation
- >50% included all bioclimatic variables without biological justification; ~50% of those reduced variables using automated approaches (correlations, VIF, best fit)
- 48.7% of papers using pseudo-absences/background did not report the sampling area

## Simulation study design

50 virtual species generated using the "virtualspecies" R package. For each:
- Study area: random extent 3–10 decimal degrees (~330–1,100 km)
- Niche: 6 random bioclimatic variables, Gaussian tolerances from local conditions
- Projections: present and future (2050, RCP 8.5) using CHELSA bioclimatic variables at 0.1° resolution

Seven treatment dimensions varied across 500 model settings (conditional Latin hypercube sampling from 7,560 combinations):
1. Number of presences: 10, 25, 50, 100, 250, 500, 1,000
2. Sample prevalence: 0.01, 0.1, 1
3. Background buffer: 0%, 100%, 500%, 5,000%, 50,000% of MCP
4. Environmental bias: presences sampled below 33%, 66%, or 100% quantile of a relevant predictor
5. Niche filling: presences sampled below 33%, 66%, or 100% quantile of human footprint index
6. Relevant predictors: 0, 3, or 6 (true niche axes)
7. Irrelevant predictors: 0, 3, or 6 (spurious correlates)

Three algorithms: GLM (stepwise AIC, linear + quadratic), MaxEnt (cloglog, linear + quadratic features), random forest (500 trees, stratified sampling).

Two validation approaches: (a) repeated split-sample (80/20, 10 repeats) and (b) spatial block (3×3 blocks, leave-one-block-out).

True accuracy measured by comparing predictions against virtual reality (known true distribution).

## Key results

### Estimated vs. true accuracy
- Split-sample validation consistently over-estimates true predictive accuracy, for both present and future predictions
- Spatial block validation slightly over-estimates present AUC but approximates future AUC well; TSS from spatial blocks slightly under-estimates true values
- Binary predictions (TSS) have substantially lower accuracy than continuous outputs (AUC)
- Future predictions and contraction/expansion areas show lower performance than present, especially when binarized

### Under optimal vs. poor settings
- Optimal settings (large sample, relevant predictors, no assumption violations): models perform reasonably by AUC but poorly for binary outputs
- Poor settings (small sample, irrelevant predictors, assumption violations): split-sample estimated accuracy remains high but true accuracy drops dramatically; spatial block validation still over-estimates when data are environmentally biased

### Determinants of estimated accuracy (split-sample)
- Most important: species prevalence, environmental gradient sampled (inverse of bias), geographic extent
- Sample prevalence important for RF; number of presences important for GLM
- Number of relevant/irrelevant predictors: weak positive effect on estimated accuracy regardless of model

### Determinants of true accuracy
- Present: species prevalence, number of presences, environmental gradient sampled
- Future: relevant predictors and niche filling become especially influential; irrelevant predictors decrease performance; environmental similarity between present and future is a key predictor
- Sample size relationship with true accuracy is asymptotic, stabilizing around 200–500 points
- Violation of equilibrium and random sampling assumptions increases estimated accuracy but decreases true accuracy — a false sense of accuracy

### Range shift estimates
- Irrelevant predictors and assumption violations increase both estimated contraction and expansion
- Environmental dissimilarity between present and future negatively affects contraction and expansion accuracy

## Discussion and recommendations

### 1. Aim for large sample sizes
- Sample size has little influence on estimated (cross-validated) accuracy but is one of the most important predictors of true accuracy
- Relationship is asymptotic, stabilizing around 200–500 points
- Previous recommendations of 14–25 points (van Proosdij et al. 2016) were assessed under ideal conditions only
- SDMs trained on insufficient samples may be detrimental rather than useful

### 2. Emphasize sample prevalence, not absolute background points
- GLM and MaxEnt work best with very low sample prevalence (many background points relative to presences)
- Random forest performs best with high sample prevalence (equal presences and background)
- No rule of thumb exists; settings should be model- and sample-specific

### 3. Choose predictors carefully
- Irrelevant predictors deceitfully increase estimated performance
- When projecting under different conditions, few biologically meaningful variables are better than many unclear ones
- Spatial block validation is sensitive to irrelevant predictors (unlike split-sample)

### 4. Geographic extents
- Sampling over large areas inflates estimated accuracy
- Effect on true accuracy is inconsistent across metrics and models
- Appropriate extent varies by species and study objective

### 5. Noise is inevitable
- Species prevalence is an unknown factor always affecting predictive ability
- When future conditions are very dissimilar from present, projections perform poorly — paradoxically, these are the situations where projections matter most

### 6. Violation of assumptions gives false accuracy
- Non-equilibrium and non-random sampling inflate split-sample accuracy
- Spatial block validation helps detect non-equilibrium but not environmental bias
- Citizen science data are particularly prone to sample bias
- Niche tends to be under-estimated, making projections pessimistic on average

### 7. Binarization
- High AUC can correspond to low TSS
- Threshold optimized on training data may not discriminate well under different conditions
- Binary outputs should never be used to quantify changes in distribution areas
- Alternative: examine trends in predicted probabilities per area

### Additional uncertainty sources (not tested)
- Spatial accuracy of data points
- Taxonomic accuracy
- Intraspecific variation and local adaptation
- Phenotypic plasticity (ΔTraitSDMs can reduce pessimistic bias)
