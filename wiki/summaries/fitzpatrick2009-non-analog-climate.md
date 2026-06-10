---
title: "The projection of species distribution models and the problem of non-analog climate"
created: 2026-05-28
updated: 2026-05-28
type: summary
sources:
  - fitzpatrick2009-non-analog-climate
---

## Citation

Fitzpatrick MC, Hargrove WW (2009) The projection of species distribution models and the problem of non-analog climate. Biodiversity and Conservation, 18:2255–2261. DOI: 10.1007/s10531-009-9584-8

## TL;DR

Species distribution models routinely extrapolate into climatic conditions that have no modern analog, yet this extrapolation is both ecologically and statistically invalid. Fitzpatrick and Hargrove propose a "power of prediction analysis" — a companion model that maps where the calibration environment overlaps with the projection environment — so that non-analog regions are explicitly identified and reported alongside species projections.

## Key Concepts

- [[non-analog-climate]] — central focus: future climatic conditions with no present-day equivalent undermine SDM projections
- [[model-extrapolation]] — paper argues extrapolation into non-analog conditions is statistically invalid and must be flagged
- [[species-distribution-models]] — the class of models whose projections are threatened by non-analog environments
- [[ensemble-forecasting]] — case studies use BIOMOD ensemble of six algorithms (ANN, CTA, GAM, GLM, MDA, RF)
- [[clamping]] — Maxent's univariate clamping is critiqued as insufficient for detecting multivariate non-analog combinations
- [[model-evaluation]] — power of prediction analysis proposed as a complement to standard SDM outputs

## Methodology

The authors propose calibrating a model on the entire study region (all locations treated as "presences") versus the remaining background ("absences"), then projecting this region-level model onto the target environment (future climate or novel geography). Areas predicted as absent in this companion model represent non-analog environments where species-level predictions should not be attempted. Two case studies demonstrate the approach using BIOMOD ensemble forecasting in R: (1) projecting the Caspian Sea onto the Great Lakes using six remote-sensing variables at 4-km resolution (~7,500 presence points), and (2) projecting a southwestern Australian biodiversity hotspot under two 2080 climate scenarios (CSIRO-Mk2 A1B and HadCM3 A1F) using seven climate variables at 2.5-km resolution.

## Key Findings

1. By 2100, a quarter or more of Earth's land surface may experience climatic conditions with no modern analog, concentrated in regions of high biodiversity.
2. Projecting SDMs into non-analog conditions is ecologically and statistically invalid, yet it is general practice to not report or flag such areas.
3. Maxent's univariate clamping may fail to detect multivariate combinations of non-analog conditions.
4. In the Great Lakes case study, interiors of Lakes Superior, Huron, and Michigan are non-analogous to the Caspian Sea, while near-shore areas and Lake Erie show high similarity — meaning invasive species predictions are reliable only near shore.
5. For southwestern Australia under 2080 climate change, the extent of non-analog conditions varies dramatically between scenarios: under A1B most of the hotspot remains predictable, while under A1F most of it becomes non-analogous.
6. Some apparent non-analog conditions may actually represent expansion of existing conditions from adjacent biomes, suggesting the issue can partly be addressed by expanding the calibration region.
7. Failure to identify non-analog regions can lead to both overestimation of species loss and misidentification of conservation priority areas, or underestimation of invasion risk.

## Limitations

- The paper is a brief communication with only two case studies and no formal quantitative evaluation of the method's performance against alternatives (e.g., MESS maps).
- Delineating the appropriate calibration region is acknowledged as non-trivial, but no systematic guidance is provided.
- The approach does not address how much extrapolation beyond the calibration envelope might be tolerable — it flags the problem but does not quantify acceptable thresholds.
- No comparison with other non-analog detection methods (e.g., the multivariate environmental similarity surface approach later formalised by Elith et al. 2010).
- The method inherits all limitations of the underlying SDM algorithm used for the region-level model.

## Connections

- Directly related to [[model-extrapolation]]: this paper provides one of the earlier explicit treatments of extrapolation risk in SDM projections, complementing the MESS approach discussed in [[elith2010-range-shifting]].
- The ensemble framework used (BIOMOD) is the same discussed in [[araujo2007-ensemble-forecasting]] and used in [[thuiller2005-climate-change-plants]].
- The concept of areas where predictions are unreliable connects to [[meyer2021-area-of-applicability]], which later formalised a dissimilarity index approach to delineate the area of applicability — a more quantitative descendant of Fitzpatrick and Hargrove's "power of prediction analysis."
- The conservation implications of unreliable projections connect to concerns raised in [[guisan2013-sdm-conservation]] about SDMs being used for real conservation decisions.
- The Venn diagram framework (regions A, B, C) offers a conceptual complement to the BAM diagram in [[peterson2011-niches-distributions]], partitioning environmental space by prediction validity rather than niche dimensions.

## Open Questions

- How much extrapolation beyond the calibration envelope is tolerable before predictions become unreliable?
- How should the calibration region be delineated when the species' dispersal potential or biogeographic boundaries are uncertain?
- Can the power of prediction analysis be integrated directly into ensemble frameworks (e.g., as a weighting or masking layer) rather than run as a separate companion analysis?
- How does the severity of the non-analog problem vary across SDM algorithms — are some inherently more robust to mild extrapolation than others?
