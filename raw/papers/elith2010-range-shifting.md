# The art of modelling range-shifting species

**Authors:** Jane Elith, Michael Kearney, Steven Phillips
**Journal:** Methods in Ecology and Evolution, 1(4), 330–342
**Year:** 2010
**DOI:** 10.1111/j.2041-210X.2010.00036.x

## Summary

Species shifting ranges through invasion or climate change violate two key SDM assumptions: equilibrium with environment and representative training data. Using the cane toad (Bufo marinus) invasion in Australia as a case study, the authors explore modelling approaches that minimize extrapolation errors and assess predictions against mechanistic model outputs. They use four SDM methods (GLM, GAM, BRT, MaxEnt), test data weighting schemes and background sample choices, and trial two methods for integrating mechanistic model information into correlative models. New tools implemented in MaxEnt include the multivariate environmental similarity surface (MESS) for quantifying extrapolation, site-level exploration of prediction components, and limiting-factor maps.

## Key Results

- Under current climate, predictions varied more with data treatment (especially absence/background choice) than with modelling method — pairwise correlations between methods using background samples were all >0.9.
- Under climate change scenarios, models that performed similarly for current climates diverged widely.
- Cross-validated AUC on current data did not predict agreement with the mechanistic model under future climates.
- Smoother model fits (fewer trees in BRT, higher regularization in MaxEnt) produced climate change predictions most consistent with mechanistic predictions.
- Absences drawn from mechanistic model predictions improved northern predictions.
- Proximal predictors from the mechanistic model were selected as important but caused only subtle prediction changes.
- The methods and tools developed are implemented in MaxEnt version 3.3.2.

## Key Recommendations

1. Explore data weighting schemes and absence/background delineation appropriate for non-equilibrium species
2. Assess environmental novelty in projected space using MESS
3. Explore modelled responses and predictor weightings in contentious regions
4. Enforce smoother responses for extrapolation
5. Integrate mechanistic predictions with correlative models
