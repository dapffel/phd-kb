---
title: "Ecological Niches and Geographic Distributions"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - peterson2011-niches-distributions.pdf
---

## Citation
Peterson, A.T., Soberón, J., Pearson, R.G., Anderson, R.P., Martínez-Meyer, E., Nakamura, M. & Araújo, M.B. (2011) *Ecological Niches and Geographic Distributions*. Monographs in Population Biology, No. 49. Princeton University Press, Princeton. 328 pp. ISBN 978-0-691-13688-2

## TL;DR
A foundational monograph providing a rigorous conceptual framework for understanding the relationships between ecological niches and species geographic distributions. The authors formalise the distinction between Grinnellian niches (scenopoetic, non-linked variables at geographic scales) and Eltonian niches (dynamically linked variables at local scales), introduce the BAM diagram (Biotic–Abiotic–Movement) as a thinking framework, and develop formal definitions linking niche theory to species distribution modelling and ecological niche modelling.

## Key Concepts
- [[ecological-niche]] — the central concept; the authors provide formal operational definitions distinguishing multiple niche types based on the BAM framework
- [[grinnellian-niche]] — niche defined by scenopoetic (non-linked) variables at geographic scales; the subset of environmental space (E-space) where intrinsic growth rate r > 0
- [[eltonian-niche]] — niche defined by dynamically linked variables (consumed resources, biotic interactions) at local scales; requires mechanistic consumer-resource models
- [[bam-diagram]] — Biotic (B), Abiotic (A), Movement (M): three intersecting sets in geographic space whose overlap determines species distributions; GO = A ∩ B ∩ M (occupied area), GI = A ∩ B ∩ M^C (invadable area)
- [[fundamental-niche]] — Hutchinson's hypervolume of environmental conditions permitting species persistence; estimated via physiology experiments or biophysical models, independent of observed localities
- [[scenopoetic-variables]] — environmental variables not dynamically modified by the species (climate, topography); contrasted with bionomic variables that are consumed or modified
- [[species-distribution-models]] — correlative approaches estimating Grinnellian niches from occurrence data and environmental layers; distinguished from but complementary to ecological niche modelling (ENM)
- [[e-space-g-space]] — the duality between environmental space (E-space, multidimensional predictor space) and geographic space (G-space, the spatial grid); Hutchinson's Duality

## Methodology
This is a monograph (328 pages) synthesising conceptual, theoretical, and practical aspects of niche-distribution relationships. Part I (Theory) develops formal niche definitions using spatially explicit Lotka-Volterra population equations, defines the BAM diagram, and establishes the E-space/G-space duality. Part II (Practice) covers occurrence data, environmental data, modelling algorithms (from envelope methods to machine learning), model evaluation, and extrapolation. Part III (Applications) reviews uses in biodiversity discovery, conservation planning, species invasions, disease transmission, and evolutionary niche dynamics. The authors explicitly avoid reviewing specific software, focusing instead on establishing a common terminological and conceptual framework.

## Key Findings
1. The Grinnellian niche (scenopoetic variables, geographic scale) and Eltonian niche (dynamically linked variables, local scale) require fundamentally different mathematical representations: the former as subsets of E-space, the latter as zero-growth isoclines in resource-consumer models.
2. The BAM diagram provides a unified framework: a species' occupied distribution GO is the intersection of regions where abiotic conditions support positive growth (A), biotic interactions permit persistence (B), and the area is accessible to dispersal (M).
3. The distinction between scenopoetic and bionomic (dynamically linked) variables is not about biotic vs. abiotic, but about whether the variable is modified by the species' population dynamics.
4. The fundamental niche can include environmental combinations not currently existing in the study region (non-analogue environments), leading to the concept of the "existing fundamental niche" (intersection of fundamental niche with available E-space).
5. SDM and ENM are related but not equivalent: SDM estimates areas in G-space; ENM estimates niches in E-space. Both use correlative approaches but address different questions.
6. Model evaluation, algorithm choice, calibration region extent, and spatial resolution all interact and must be considered as a coherent system rather than independently.
7. Applications across conservation, invasive species, disease ecology, and evolutionary biology all benefit from the formal niche-distribution framework but require domain-specific adaptations.

## Limitations
- The book focuses on correlative approaches; process-based physiological models are acknowledged as complementary but not deeply developed.
- The framework is primarily theoretical; practical guidance on implementation is secondary to conceptual clarity.
- The Eltonian niche is acknowledged as important but largely set aside due to data and modelling complexity, leaving the Grinnellian perspective dominant.
- The 2011 publication date means it predates major advances in spatial cross-validation, deep learning methods, and the AOA framework.
- The distinction between SDM and ENM, while rigorous, has not been widely adopted in the subsequent literature where the terms remain loosely interchanged.

## Connections
- The Grinnellian niche framework directly underpins [[elith2009-sdm-review]]'s distinction between proximal and distal predictors and the interpolation/extrapolation dichotomy.
- The BAM diagram provides the theoretical foundation for understanding why [[non-equilibrium-species]] violate SDM assumptions, as explored by [[elith2010-range-shifting]].
- The E-space/G-space duality is operationalised by tools like MESS ([[elith2010-range-shifting]]) and the DI/AOA ([[meyer2021-area-of-applicability]]) that quantify environmental novelty.
- The [[fundamental-niche]] vs. realised niche distinction underlies [[guisan2013-sdm-conservation]]'s argument that SDMs alone cannot predict population viability.
- The scenopoetic variable framework informs the choice of predictors discussed across all SDM sources in the wiki.

## Open Questions
- Can the BAM framework be made quantitative rather than heuristic — i.e., can the sizes and overlaps of A, B, and M be estimated empirically?
- How should Eltonian niche effects be integrated into geographic-scale SDMs without requiring impractical data on local biotic interactions?
- Does the Grinnellian/Eltonian distinction hold at intermediate spatial scales, or is a continuum of niche types more appropriate?
- How should the framework be updated to accommodate new modelling paradigms (deep learning, spatially explicit process-based models)?
