---
title: "Glossary"
updated: 2026-04-28
---

## Terms

**AOA** — Area of Applicability. The geographic area where a prediction model's cross-validation error estimate is expected to hold; delineated by thresholding the dissimilarity index. See [[area-of-applicability]], [[meyer2021-area-of-applicability]].

**AUC** — Area Under the Receiver Operating Characteristic Curve. A threshold-independent measure of model discrimination ability. See [[auc-roc]], [[model-evaluation]].

**BAM diagram** — A Venn diagram framework where species distributions arise from the intersection of Biotic (B), Abiotic (A), and Movement (M) factors. G_O = A ∩ B ∩ M. See [[bam-diagram]], [[peterson2011-niches-distributions]].

**Bioclimatic envelope** — The climatic conditions under which a species currently persists; the basis of correlative SDMs. See [[bioclimatic-envelope]], [[thuiller2005-climate-change-plants]].

**BIOMOD** — A software framework for ensemble species distribution modelling combining multiple algorithms (GLM, GAM, CTA, ANN). See [[ensemble-forecasting]], [[thuiller2005-climate-change-plants]].

**Block cross-validation** — Splitting data into non-random blocks (spatial, temporal, group, phylogenetic) to account for dependence structures. See [[block-cross-validation]], [[roberts2017-cross-validation]].

**Bootstrap** — A resampling method for estimating statistical accuracy by drawing samples with replacement from observed data. See [[bootstrap-resampling]], [[efron1993-bootstrap]].

**BRT** — Boosted Regression Trees. A machine learning method that fits many small decision trees sequentially, each correcting the errors of previous trees. See [[species-distribution-models]].

**DI** — Dissimilarity Index. Standardised minimum Euclidean distance in weighted predictor space from a new location to the nearest training point. See [[dissimilarity-index]], [[meyer2021-area-of-applicability]].

**Ecological niche** — The environmental conditions permitting a species to maintain populations. See [[ecological-niche]], [[peterson2011-niches-distributions]].

**Eltonian niche** — Niche defined by dynamically linked variables (resources, biotic interactions) at local scales. See [[eltonian-niche]], [[ecological-niche]].

**ENM** — Ecological Niche Modelling. Estimates niches in environmental space (E-space); related to but distinct from SDM. See [[species-distribution-models]], [[peterson2011-niches-distributions]].

**E-space** — Environmental space; the multidimensional space of scenopoetic variables. See [[e-space-g-space]], [[peterson2011-niches-distributions]].

**Ensemble forecasting** — Combining outputs from multiple models to produce more robust predictions. See [[ensemble-forecasting]], [[araujo2007-ensemble-forecasting]].

**Fundamental niche** — Hutchinson's hypervolume of all environmental conditions permitting species persistence, absent biotic interactions. See [[fundamental-niche]], [[ecological-niche]].

**GAM** — Generalised Additive Model. A flexible regression model using smooth functions of predictors. See [[species-distribution-models]].

**GLM** — Generalised Linear Model. A regression framework extending linear models to non-normal response distributions. See [[species-distribution-models]].

**Grinnellian niche** — Niche defined by scenopoetic (non-linked) variables at geographic scales. See [[grinnellian-niche]], [[ecological-niche]].

**G-space** — Geographic space; the spatial grid over which distributions are defined. See [[e-space-g-space]], [[peterson2011-niches-distributions]].

**Kappa** — Cohen's kappa statistic; measures classification agreement corrected for chance, but is prevalence-dependent. See [[kappa-statistic]], [[allouche2006-tss-accuracy]].

**MaxEnt** — Maximum Entropy modelling; a machine learning method for presence-only species distribution modelling. See [[species-distribution-models]].

**MESS** — Multivariate Environmental Similarity Surface. Identifies where projections involve novel environments relative to training data. See [[mess-analysis]], [[elith2010-range-shifting]].

**Prevalence** — The proportion of sites where a species is present in the dataset. See [[prevalence]], [[allouche2006-tss-accuracy]].

**Scenopoetic variables** — Environmental variables not dynamically modified by the species (climate, topography). See [[scenopoetic-variables]], [[ecological-niche]].

**SDM** — Species Distribution Model. A correlative model relating species occurrence to environmental characteristics. See [[species-distribution-models]].

**Sensitivity** — True positive rate; the proportion of actual presences correctly predicted. See [[sensitivity-specificity]], [[model-evaluation]].

**Specificity** — True negative rate; the proportion of actual absences correctly predicted. See [[sensitivity-specificity]], [[model-evaluation]].

**TSS** — True Skill Statistic. TSS = Sensitivity + Specificity − 1. A prevalence-independent accuracy metric. See [[true-skill-statistic]], [[allouche2006-tss-accuracy]].
