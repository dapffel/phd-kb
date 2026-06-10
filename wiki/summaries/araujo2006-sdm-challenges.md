---
title: "Five (or so) challenges for species distribution modelling"
created: 2026-05-28
updated: 2026-05-28
type: summary
sources:
  - araujo2006-sdm-challenges
---

## Citation

Araújo, M.B. & Guisan, A. (2006). Five (or so) challenges for species distribution modelling. *Journal of Biogeography*, 33, 1677–1688. DOI: 10.1111/j.1365-2699.2006.01584.x

## TL;DR

Araújo and Guisan identify five high-priority challenges for niche-based species distribution modelling: clarifying the niche concept, improving sampling designs, improving parameterization, improving model selection and predictor contribution, and improving model evaluation. The essay argues for deeper debate on the strengths and limitations of SDM approaches, with more rigorous sensitivity analyses of model outcomes.

## Key Concepts

- [[ecological-niche]] — re-reads Hutchinson (1957) and argues the fundamental/realized dichotomy is artificial; endorses Chase & Leibold's (2003) modern Grinnellian definition
- [[species-distribution-models]] — central subject; the authors argue SDMs need more rigorous methodological foundations
- [[model-evaluation]] — evaluation should be linked to model purpose (description, understanding, or prediction), each requiring different validation strategies
- [[model-extrapolation]] — projecting to future climates with models trained on current data raises transferability concerns
- [[cross-validation]] — split-sample and bootstrap approaches assume independence, but spatial autocorrelation can violate this assumption
- [[sampling-design]] — model-based environmental stratifications can reduce sampling bias compared to opportunistic museum/collection data

## Methodology

This is a conceptual essay rather than an empirical study. The authors review the SDM literature and organise the field's methodological challenges into five thematic areas. They draw on examples from the ecological modelling literature to illustrate each challenge and propose directions for improvement.

## Key Findings

1. SDMs' relationship to the ecological niche is ambiguous: Soberón & Peterson (2005) argue they approximate the fundamental niche, while others view them as representing the realized niche; the authors argue that biotic interactions beyond competition (e.g., mutualism, facilitation) should be part of the fundamental niche, making the fundamental/realized dichotomy artificial.
2. Chase & Leibold's (2003) modern Grinnellian definition — environmental conditions allowing a species to satisfy minimum requirements so that birth rate ≥ death rate — provides a more workable niche concept than Hutchinson's original formulation.
3. SDMs are sensitive to sample size and spatial biases in occurrence data; model-based environmental stratifications offer a better approach to target additional sampling effort than opportunistic collection.
4. Within-model variation (alternative parameterizations of the same technique) can be as large as between-model variation, making diagnostic tools (residual analysis, link function assessment, autocorrelation checks) essential.
5. Stepwise variable selection is a high-variance operation; alternatives include coupling stepwise with cross-validation, shrinkage rules (ridge regression, lasso), and model averaging (AIC-based).
6. Model evaluation should match the model's purpose: description requires only verification, understanding requires robustness of inferred mechanisms, and prediction requires generality and transferability via validation with independent data.
7. Most SDM studies projecting to the future use resubstitution (same data for training and testing), which is inadequate; true validation requires data from different regions or times, but even then models predict potential distributions while being tested against realized distributions, creating a conceptual mismatch.

## Limitations

- The essay identifies additional challenges (spatial/temporal autocorrelation effects, geographical extent and resolution, pseudo-absence selection, probability-to-presence/absence thresholds) but does not discuss them in detail.
- The authors do not provide quantitative benchmarks or concrete decision rules for resolving the challenges they outline.
- The niche concept discussion is primarily theoretical and does not offer an empirical test to distinguish fundamental from realized niche in practice.

## Connections

- Directly relevant to [[model-evaluation]]: the three-purpose evaluation framework (description, understanding, prediction) provides a conceptual foundation that later work by [[roberts2017-cross-validation]] operationalises with block cross-validation strategies.
- The concern about resubstitution-based evaluation anticipates [[santini2021-sdm-reliability]], which empirically demonstrates that split-sample validation overestimates true SDM accuracy.
- The niche concept discussion connects to [[peterson2011-niches-distributions]], which formalises niche theory with the BAM diagram and Grinnellian vs. Eltonian distinction.
- The emphasis on predictor selection and parameterization uncertainty resonates with [[ensemble-forecasting]] approaches (e.g., [[araujo2007-ensemble-forecasting]]) that address model uncertainty by combining multiple techniques.
- The transferability concern links to [[model-extrapolation]], [[fitzpatrick2009-non-analog-climate]], and [[meyer2021-area-of-applicability]].

## Open Questions

- How can the fundamental niche be estimated empirically in practice, given that manipulative experiments are costly and field-based SDMs capture only the realized niche?
- What is the minimum sample size and optimal spatial stratification design needed to produce reliable SDM outputs?
- How should model evaluation change when the goal is projection into novel climatic or geographic conditions?
