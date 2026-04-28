---
title: "Species Distribution Models"
created: 2026-04-28
updated: 2026-04-28
type: concept
sources:
  - elith2009-sdm-review.pdf
  - araujo2007-ensemble-forecasting.pdf
  - allouche2006-tss-accuracy.pdf
  - elith2010-range-shifting.pdf
  - guisan2013-sdm-conservation.pdf
  - meyer2021-area-of-applicability.pdf
  - roberts2017-cross-validation.pdf
  - thuiller2005-climate-change-plants.pdf
  - peterson2011-niches-distributions.pdf
---

## Definition
Species distribution models (SDMs) are statistical or machine learning models that relate species occurrence or abundance data to environmental and/or spatial characteristics of locations, in order to explain or predict the spatial distribution of species. They are also referred to as bioclimatic envelope models, habitat suitability models, or ecological niche models (ENMs), though [[peterson2011-niches-distributions]] argues these terms are not interchangeable.

## Background
Modern SDMs emerged in the 1980s from the convergence of field-based ecology (particularly generalised linear models) with GIS and the growing availability of spatially continuous environmental data ([[elith2009-sdm-review]]). The dramatic increase in digitised species occurrence records (museums, herbaria, citizen science) and high-resolution environmental layers (climate, topography, remote sensing) made correlative modelling of species–environment relationships practical at regional to global scales. SDMs have become one of the most widely published tools in ecology, yet fewer than 1% of SDM papers demonstrably inform real conservation decisions ([[guisan2013-sdm-conservation]]).

## How It Works
The general workflow:

1. **Occurrence data**: presence-only records (e.g., museum specimens) or presence–absence data from surveys. See [[presence-only-data]].
2. **Environmental predictors**: scenopoetic variables (climate, topography, soil) that are not dynamically linked to the species ([[peterson2011-niches-distributions]]). Proximal predictors (direct physiological drivers) are preferred over distal proxies (e.g., elevation), especially for extrapolation ([[elith2009-sdm-review]]).
3. **Algorithm**: ranges from simple envelope methods (BIOCLIM) through regression (GLM, GAM) to machine learning (BRT, Random Forest, MaxEnt, neural networks). Different methods can yield dramatically different projections under climate change, even when they perform similarly on current data ([[elith2010-range-shifting]]).
4. **Evaluation**: using held-out data or cross-validation with metrics such as AUC, TSS ([[allouche2006-tss-accuracy]]), or kappa. Block cross-validation is recommended for spatially structured data ([[roberts2017-cross-validation]]).
5. **Projection**: applying the fitted model to new geographic areas or future climate scenarios. The reliability of these projections depends on whether the new environments fall within the model's area of applicability ([[meyer2021-area-of-applicability]]).

Key assumptions: (1) the species is in equilibrium with its environment, (2) the training data adequately represent the species–environment relationship, (3) the modelled relationships hold under projection conditions. All three are routinely violated, especially for range-shifting species ([[elith2010-range-shifting]]) and future climate projections.

## Key Results From Sources
- **[[elith2009-sdm-review]]**: SDMs emerged from the convergence of ecology and GIS. Weak links between ecological theory and modelling practice remain the key obstacle to progress. Machine learning methods outperform classical methods in predictive benchmarks, but the distinction between interpolation (reliable) and extrapolation (risky) is fundamental.
- **[[araujo2007-ensemble-forecasting]]**: Single SDM forecasts are unreliable — nine models applied to the same South African plant species predicted range changes from −92% to +322%. Ensemble forecasting (combining multiple models) is necessary for robust predictions.
- **[[elith2010-range-shifting]]**: For non-equilibrium species, data treatment choices (background selection, weighting) matter more than algorithm choice. Cross-validated AUC on current data does not predict model reliability under future climates.
- **[[guisan2013-sdm-conservation]]**: SDMs can inform all stages of structured decision-making but are rarely embedded in actual conservation decisions. They must be coupled with population dynamics models when persistence predictions are needed.
- **[[peterson2011-niches-distributions]]**: SDMs estimate areas in geographic space (G-space); ENMs estimate niches in environmental space (E-space). Both use correlative approaches but answer different questions. The BAM diagram formalises the factors determining distributions: Biotic interactions, Abiotic conditions, and Movement/dispersal.
- **[[roberts2017-cross-validation]]**: Standard random cross-validation overestimates SDM performance on structured data. Block CV produces more realistic error estimates.
- **[[meyer2021-area-of-applicability]]**: SDM predictions should be restricted to the area of applicability where cross-validation error holds. Outside this area, predictions are unreliable.
- **[[thuiller2005-climate-change-plants]]**: BIOMOD ensemble of four SDM methods projected >50% of 1,350 European plant species as vulnerable or threatened by 2080.
- **[[allouche2006-tss-accuracy]]**: TSS is a better accuracy metric than kappa for SDMs because it is independent of species prevalence.

## Open Problems
- How to reliably extrapolate SDMs to novel (non-analogue) climates where training data offer no guidance.
- Integrating biotic interactions into correlative SDMs at geographic scales.
- Bridging the gap between SDM development and real-world conservation decision-making.
- Standardising model evaluation practices across the field, particularly regarding spatial cross-validation.
- Reconciling the Grinnellian niche focus of correlative SDMs with the Eltonian processes that also shape distributions.

## Related Concepts
- [[ecological-niche]]
- [[model-extrapolation]]
- [[ensemble-forecasting]]
- [[model-evaluation]]
- [[conservation-planning]]
- [[presence-only-data]]
- [[bam-diagram]]
