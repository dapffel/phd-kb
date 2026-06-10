# Five (or so) challenges for species distribution modelling

**Authors:** Miguel B. Araújo, Antoine Guisan
**Journal:** Journal of Biogeography (2006) 33:1677–1688
**DOI:** 10.1111/j.1365-2699.2006.01584.x
**Type:** Essay / Special Issue

---

## Summary

Araújo and Guisan identify five high-priority challenges for niche-based species distribution modelling: (1) clarification of the niche concept, (2) improved sampling designs, (3) improved parameterization, (4) improved model selection and predictor contribution, and (5) improved model evaluation. The essay argues that the SDM community needs deeper debate on the strengths and limitations of available approaches, with more rigorous assessments of the sensitivity of model outcomes to initial assumptions and parameters.

## Challenge 1: Clarification of the niche concept

Conflicting views exist on whether SDMs represent the fundamental or realized niche. Soberón & Peterson (2005) argued SDMs approximate the fundamental niche; others (Austin et al. 1990; Guisan & Zimmermann 2000; Pearson & Dawson 2003) view them as representing the realized niche. Ambiguities arise from Hutchinson's (1957) original formulation. The authors re-read Hutchinson to argue that biotic interactions other than competition (e.g. mutualism, facilitation) should be part of the fundamental niche. This makes the fundamental/realized dichotomy artificial. They suggest Chase & Leibold's (2003) modern Grinnellian definition suffices: the environmental conditions allowing a species to satisfy minimum requirements so that birth rate equals or exceeds death rate. They also argue for clearer distinction between niche models (projecting potential habitats) and spatial-explicit models (projecting potential geographical distributions when dispersal is incorporated).

## Challenge 2: Improved sampling designs

SDMs are sensitive to sample size and biases. Museum/collection data are often incomplete and biased. Sub-sampling can reduce biases but requires large datasets. Model-based environmental stratifications offer a better approach to target additional sampling effort. These ideas are in their infancy and need further testing.

## Challenge 3: Improved parameterization

Different techniques and implementations yield different results. Within-model variation (alternative parameterizations of the same technique) can be as large as between-model variation. Diagnostic tools (residual distributions, link function appropriateness, autocorrelation, complexity of response curves) should be used more systematically.

## Challenge 4: Improved model selection and predictor contribution

Model outputs are driven by predictor choice; differences among predictions can be very large when projecting to independent situations. Stepwise variable selection is a high-variance operation. Alternatives include coupling stepwise with cross-validation, shrinkage rules (ridge regression, lasso), model averaging (AIC-based). Hierarchical partitioning and variance partitioning help assess predictor contributions but have limitations (non-additive contributions, non-OLS frameworks, interaction terms). Automated selection should not substitute for ecologically informed predictor choice.

## Challenge 5: Improved model evaluation

Model evaluation should be linked to the model's purpose: description (verification sufficient), understanding (robustness of inferred mechanisms), or prediction (generality/transferability via validation). Most studies projecting to the future use resubstitution (same data for training and testing). Split-sample, bootstrap, and jackknife approaches assume independence but spatial autocorrelation can violate this. True validation requires data from different regions or times. Hind-casting offers one alternative. Even with independent data, models predict potential distributions but are tested against realized distributions, creating a conceptual mismatch.

## Additional challenges noted but not discussed in detail

1. Effects of spatial and temporal autocorrelation
2. Effects of geographical extent and resolution
3. Strategies for selecting pseudo-absences
4. Rules for transforming probabilities to presence/absence
