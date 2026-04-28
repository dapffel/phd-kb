---
title: "Climate change threats to plant diversity in Europe"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - thuiller2005-climate-change-plants.pdf
---

## Citation
Thuiller, W., Lavorel, S., Araújo, M.B., Sykes, M.T. & Prentice, I.C. (2005) Climate change threats to plant diversity in Europe. *Proceedings of the National Academy of Sciences*, 102(23), 8245–8250. doi: 10.1073/pnas.0409902102

## TL;DR
Projecting future distributions for 1,350 European plant species under seven climate change scenarios using the BIOMOD ensemble framework, this study shows that more than half of studied species could become vulnerable or threatened by 2080 under no-migration assumptions. Mountain regions are disproportionately sensitive, while projected species loss across Europe is strongly and linearly related to changes in just two bioclimatic variables: growing-degree days and moisture availability.

## Key Concepts
- [[climate-change-biodiversity]] — central topic; quantifying risks to European plant diversity from projected climate change
- [[species-distribution-models]] — BIOMOD framework combining GLMs, GAMs, classification tree analysis, and artificial neural networks
- [[ensemble-forecasting]] — consensus PCA used to select the most representative niche-based model projection from among four techniques, following the ensemble logic of reducing inter-model variability
- [[bioclimatic-envelope]] — the modelling paradigm; species' current climatic envelopes are assumed to reflect environmental preferences retained under future climate
- [[species-turnover]] — metric of compositional change; turnover = 100 × (L + G) / (SR + G), calculated per pixel under universal migration
- [[dispersal-limitation]] — two extreme assumptions tested: no migration (species cannot move) and universal migration (no dispersal constraints)
- [[conservation-planning]] — IUCN Red List criteria applied to projected range losses to assess species-level extinction risk

## Methodology
Species distribution data for 1,350 plants on a 50 × 50 km European grid were modelled using the BIOMOD framework, which runs four niche-based modelling techniques (GLM, GAM, classification tree analysis, neural networks) and selects the most consensual projection via a consensus PCA. Seven climate scenarios (four IPCC storylines × three GCMs: HadCM3, CGCM2, CSIRO2) projected distributions for 2051–2080 relative to a 1961–1990 baseline. Seven bioclimatic variables were used: mean annual, winter, and summer precipitation; mean annual temperature; minimum temperature of coldest month; growing degree days (>5°C); and a moisture availability index. Species loss (no migration), species gain, and turnover (universal migration) were calculated per pixel. IUCN Red List criteria (A3c) were applied to projected range-size reductions.

## Key Findings
1. Under no migration, more than half of the 1,350 species studied become vulnerable or threatened by 2080; under the most severe scenario (A1-HadCM3), 22% become critically endangered and 2% extinct.
2. Mean European species loss ranges from 27% (B1-HadCM3) to 42% (A1-HadCM3); mean turnover ranges from 45% to 63%.
3. Regional variability is extreme: species loss per pixel ranges from 2.5% to 86% across scenarios.
4. Species loss depends strongly and linearly on anomalies in just two bioclimatic variables — growing-degree days and a moisture availability index — which together explain 60% of the variance across scenarios in a multiple regression.
5. Mountain regions (mid-altitude Alps, Pyrenees, Cevennes, Balkans, Carpathians) are disproportionately sensitive (~60% species loss), owing to narrow habitat tolerances of specialised mountain flora.
6. The boreal region is projected to lose few species but gain many from southward immigration, leading to high turnover (66%).
7. The Mediterranean–Euro-Siberian transition zone shows the greatest species mixing and turnover, acting as both a crossing point and historical refuge.
8. Under universal migration, impacts are less severe — 67–76% of species remain at low risk depending on the scenario.

## Limitations
- The 50 × 50 km grid resolution may hide potential microrefugia and environmental heterogeneity that could enhance species survival, especially in mountains.
- The two extreme migration assumptions (none vs. universal) bracket reality but do not model actual dispersal processes.
- Land-use change is not considered, despite its potential to compound climate effects.
- Physiological CO₂ responses (e.g., changed water-use efficiency) are not included.
- The IUCN Red List application is simplistic — it considers only range-size reduction and uses modified time thresholds (80 years instead of 20).
- Biotic interactions, adaptation, and evolutionary responses are ignored.
- The study predates the consensus on spatial CV; model evaluation may be overly optimistic.

## Connections
- Uses the BIOMOD framework, which implements the [[ensemble-forecasting]] approach later formalised by [[araujo2007-ensemble-forecasting]] (Araújo is a co-author of both).
- The finding that model projections vary widely across scenarios and methods motivates the ensemble approach advocated by [[araujo2007-ensemble-forecasting]].
- The bioclimatic envelope assumption and its limitations connect to [[elith2009-sdm-review]]'s discussion of [[model-extrapolation]] — projecting envelopes to future climates is inherently extrapolation.
- The conservation implications (IUCN Red List application) connect to [[guisan2013-sdm-conservation]]'s framework for embedding SDMs in conservation decisions.
- The mountain sensitivity finding is relevant to [[climate-change-biodiversity]] as a concept article topic.

## Open Questions
- How much do microrefugia and fine-scale topographic heterogeneity mitigate the projected losses at coarse resolution?
- What realistic dispersal rates should be assumed for European plant species, given current landscape fragmentation?
- How would inclusion of land-use change alter the spatial patterns of vulnerability?
- Do the two bioclimatic predictors that explain species loss (growing-degree days, moisture) also predict functional diversity loss?
