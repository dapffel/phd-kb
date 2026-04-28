---
title: "Species Distribution Models: Ecological Explanation and Prediction Across Space and Time"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - elith2009-sdm-review.pdf
---

## Citation
Elith, J. & Leathwick, J.R. (2009) Species distribution models: ecological explanation and prediction across space and time. *Annual Review of Ecology, Evolution, and Systematics*, 40, 677–697. doi: 10.1146/annurev.ecolsys.110308.120159

## TL;DR
A comprehensive review of species distribution models (SDMs) spanning terrestrial, freshwater, and marine realms. The authors argue that further advances in SDMs will come more from better integration of ecological theory, concepts, and practice than from improved methods alone. They distinguish interpolation (reliable) from extrapolation (risky) and identify weak theory–practice linkages as a key obstacle.

## Key Concepts
- [[species-distribution-models]] — defined as models relating species occurrence/abundance data to environmental and/or spatial characteristics of locations
- [[model-extrapolation]] — prediction to new geographic domains or climates; inherently risky because training data cannot directly support predictions in novel environments
- [[spatial-autocorrelation]] — geographic clumping from response to spatially autocorrelated environment and/or geographic processes; residual patterns indicate missing predictors or misspecification
- [[presence-only-data]] — records of known occurrences without information about absences; common from museum collections and opportunistic records
- [[model-evaluation]] — diverse opinions on important properties; common statistics include kappa, AUC, correlation coefficients
- [[ensemble-forecasting]] — referenced as model averaging/consensus approach for reducing uncertainty
- [[ecological-niche]] — debated relationship with SDMs; authors prefer neutral "SDM" terminology over "ecological niche model"
- [[biotic-interactions]] — very few SDMs explicitly include biotic predictors; critical gap especially for extrapolation

## Methodology
This is a review paper synthesizing the SDM literature across disciplines and biological realms. The authors deliberately focus on historical, conceptual, and cross-disciplinary features rather than methodological advice. They examine diverse uses of SDMs (explanation, interpolation, extrapolation) and identify emerging issues and underexplored topics.

## Key Findings
1. Modern SDMs emerged from the convergence of field-based ecology (GLMs) with GIS and spatial data technologies in the 1980s.
2. Differences in species mobility drive major differences in modeling approach across biological realms (sessile vs. mobile species, freshwater vs. marine).
3. The distinction between geographic and environmental space is fundamental: SDMs with only environmental predictors are ignorant of geographic proximity, and spatial patterns in predictions reflect autocorrelation of environment.
4. Functionally relevant (proximal) predictors produce better models than convenient (distal) proxies like elevation; this matters especially for extrapolation where correlations between distal and proximal predictors may not hold.
5. Machine learning methods (boosted regression trees, random forests, MaxEnt) can exceed conventional techniques in predictive performance.
6. Prediction takes two forms: interpolation to unsampled sites (usually reliable) and extrapolation to new domains/climates (violates key SDM assumptions).
7. Current linkages between SDM practice and ecological theory are often weak, hindering progress and limiting uptake by other disciplines.
8. Model evaluation remains fragmented; progress impeded by arguments about general validity of individual statistics rather than identifying proper use of each.

## Limitations
- As a review, the paper synthesizes rather than generates new empirical evidence.
- Limited to 120 references, meaning many relevant works are cited only in supplemental material.
- Does not provide specific methodological recommendations or benchmarks.
- The future issues identified (biotic interactions, uncertainty, presence-only data) remain substantially unresolved at time of publication.

## Connections
- Directly cites [[araujo2007-ensemble-forecasting]] regarding ensemble approaches for reducing model uncertainty and extrapolation.
- The model evaluation discussion connects to [[allouche2006-tss-accuracy]] via the critique of kappa and AUC statistics.
- The distinction between interpolation and extrapolation is central to [[model-extrapolation]] and [[model-uncertainty]].
- The presence-only data discussion links to MaxEnt and [[species-distribution-models]] methodology.
- TODO: connect to papers on specific methods (boosted regression trees, random forests, MaxEnt) as they are ingested.

## Open Questions
- How can stronger links between ecological theory and SDM practice be achieved systematically?
- What is the best approach for modeling biotic interactions within correlative SDMs?
- How should model evaluation be standardized across different SDM applications and data types?
- Can SDMs be reliably used for extrapolation, and if so, under what conditions?
- How should uncertainty in SDM predictions be communicated to decision-makers?
