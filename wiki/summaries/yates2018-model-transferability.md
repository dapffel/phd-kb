---
title: "Outstanding Challenges in the Transferability of Ecological Models"
created: 2026-06-03
updated: 2026-06-03
type: summary
sources:
  - yates2018-model-transferability
---

## Citation

Yates, K.L., Bouchet, P.J., Caley, M.J., Mengersen, K., Randin, C.F., Parnell, S., Fielding, A.H., ... & Sequeira, A.M.M. (2018). Outstanding challenges in the transferability of ecological models. *Trends in Ecology & Evolution*, 33(10), 790–802. DOI: 10.1016/j.tree.2018.08.001

## TL;DR

Fifty experts used a modified Delphi technique to identify twelve priority challenges (six fundamental, six technical) for improving model transferability in ecology. The highest-priority gap is the absence of widely applicable transferability metrics; the most immediate path to improvement is building models grounded in well-established mechanisms rather than purely correlative approaches.

## Key Concepts

- [[model-extrapolation]] — central topic; transferability defined as a model's capacity to produce accurate predictions for conditions different from training data
- [[species-distribution-models]] — the primary class of models discussed; transferability of SDMs varies by species traits, model complexity, and environmental dissimilarity
- [[model-evaluation]] — "how should transferability be assessed?" emerged as the highest-priority knowledge gap among all twelve challenges
- [[ecological-niche]] — transferability should be greater in models fitted to observations documenting the full fundamental niche, but most datasets fall short
- [[nonstationarity]] — species–environment relationships are rarely static, varying with resource availability, ontogeny, and population density; a key obstacle to successful transfers
- [[model-complexity]] — parsimonious models generally transfer better, but simplicity is not always beneficial; optimal complexity depends on species traits and study context

## Methodology

Modified Delphi technique involving 50 experts who identified and prioritised knowledge gaps related to model transferability. Challenges were divided into fundamental (conceptual obstacles) and technical (best-practice) categories. The review synthesises evidence across taxa, ecosystems, and modelling approaches, drawing on published transferability studies spanning terrestrial, marine, and freshwater systems.

## Key Findings

1. Geographic separation is a poor predictor of model transferability; environmental dissimilarity between reference and target systems is what matters most for successful transfers.
2. Body size and trophic position are strong indicators of ecological predictability; models for wide-ranging generalists are harder to transfer than those for narrow-ranging specialists.
3. Parsimonious models with smooth univariate response curves and few predictors generally achieve greater transferability, but simple models can also yield misleading predictions in new contexts — optimal complexity is case-specific.
4. No "silver bullet" algorithm exists; species' characteristics can matter more than model choice, and model averaging can reduce overreliance on any single technique.
5. The highest-priority knowledge gap is the absence of widely applicable, standardised transferability metrics that enable direct comparisons among studies, systems, and taxa.
6. Mechanistic models could enhance transferability by grounding predictions in causal processes, but they remain mostly untested and are constrained by limited availability of experimental data; some studies find correlative and mechanistic models perform equally well.
7. Uncertainty arises from many sources (sampling, data quality, model specification, predictor choice), propagates multiplicatively through model phases, and remains generally underappreciated; clear protocols for measuring and reporting uncertainty are largely lacking.
8. Temporal transfers are particularly challenging because future events cannot be validated directly; hindcasting and space-for-time substitution offer partial solutions.
9. Better transferability might not equate to better decisions if uncertainties are not suitably measured, reported, and communicated to end-users and decision makers.
10. The fastest way to enhance predictions is to use them as tools for learning — rigorous documenting of transfer failures is essential but rarely practised.

## Limitations

- The review synthesises expert opinion via a Delphi process, which may reflect disciplinary biases of participants (predominantly SDM and marine/terrestrial ecology experts).
- Spatial transferability dominates the literature (and this review), not because it is more important than temporal transferability but because temporal transfers are harder to evaluate.
- The paper does not provide quantitative benchmarks or thresholds for "acceptable" transferability — this remains an open question.
- Most evidence comes from single-species SDMs; community- and ecosystem-level transferability studies remain scarce.

## Connections

- Directly extends [[model-extrapolation]] and connects to [[fitzpatrick2009-non-analog-climate]] and [[meyer2021-area-of-applicability]], which provide specific tools (MESS, AOA) for diagnosing non-analog conditions and extrapolation limits.
- The emphasis on environmental dissimilarity over geographic distance complements [[williams2007-novel-climates]], which identifies where novel climates will emerge.
- The finding that model complexity and algorithm choice matter less than species traits and data quality resonates with [[elith2010-range-shifting]] (data treatment > algorithm choice) and [[araujo2006-sdm-challenges]] (within-model variation as large as between-model variation).
- The call for standardised evaluation metrics connects to [[model-evaluation]], [[allouche2006-tss-accuracy]], and [[santini2021-sdm-reliability]], which address the limitations of current validation practices.
- The nonstationarity challenge directly relates to [[pearman2008-niche-dynamics]], which shows niche shifts can occur rapidly in invasive species, violating the stationarity assumption underlying model transfers.
- The correlative vs. mechanistic model discussion connects to [[peterson2011-niches-distributions]] on niche theory and to [[ensemble-forecasting]] as one strategy for reducing model-choice uncertainty.

## Open Questions

- What is the minimum level of environmental similarity required between reference and target systems for a model transfer to be reliable?
- Can standardised transferability metrics be developed that work across taxa, ecosystems, and modelling approaches?
- Under what conditions do mechanistic models actually outperform correlative models in transfer settings?
- How should uncertainty be propagated and communicated to decision makers who lack statistical expertise?
