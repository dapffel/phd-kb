---
title: "Predicting species distributions for conservation decisions"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - guisan2013-sdm-conservation.pdf
---

## Citation
Guisan, A., Tingley, R., Baumgartner, J.B., Naujokaitis-Lewis, I., Sutcliffe, P.R., Tulloch, A.I.T., Regan, T.J., Brotons, L., McDonald-Madden, E., Mantyka-Pringle, C., Martin, T.G., Rhodes, J.R., Maggini, R., Setterfield, S.A., Elith, J., Schwartz, M.W., Wintle, B.A., Broennimann, O., Austin, M., Ferrier, S., Kearney, M.R., Possingham, H.P. & Buckley, Y.M. (2013) Predicting species distributions for conservation decisions. *Ecology Letters*, 16(12), 1424–1435. doi: 10.1111/ele.12189

## TL;DR
Despite widespread claims of conservation applicability, fewer than 1% of SDM papers demonstrably inform real-world conservation decisions; successful examples are mostly hidden in grey literature. The authors propose embedding SDMs within structured decision-making frameworks and illustrate this with case studies across four conservation domains: biological invasions, critical habitat identification, reserve selection, and translocation.

## Key Concepts
- [[structured-decision-making]] — the overarching framework proposed; SDMs should inform each stage: problem identification, objective definition, action definition, consequence evaluation, and trade-off assessment
- [[species-distribution-models]] — the modelling tools whose conservation impact the paper evaluates and advocates improving
- [[conservation-planning]] — the applied domain; SDMs are underutilised in practice despite being framed as conservation tools
- [[uncertainty-quantification]] — ensemble GCM projections capture only one source of uncertainty; model construction, species data errors, and SDM goodness-of-fit are often neglected
- [[reserve-selection]] — one of four decision domains; tools like Marxan and Zonation can incorporate SDM-derived uncertainty layers
- [[invasive-species-management]] — case study domain where false negative costs vary by decision stage (pre-border vs. post-border)
- [[critical-habitat]] — case study domain; hybrid SDM-population models for Ord's kangaroo rat showed 39% of predicted suitable habitat unlikely to support viable populations
- [[translocation]] — SDMs used to identify suitable recipient sites, but persistence predictions require coupling with population dynamics models

## Methodology
This is a review and framework paper, not an empirical study. The authors surveyed the SDM literature to quantify the fraction of papers that demonstrably inform conservation decisions, then examined grey literature for successful but unpublished examples. They propose a structured decision-making framework with SDMs embedded at each stage and illustrate it through four conservation domain case studies: (1) weed risk assessment in Australia (gamba grass), (2) critical habitat identification for Ord's kangaroo rat in Canada, (3) threatened bird conservation in Catalonia's Natura 2000, and (4) reserve selection in Madagascar and NSW, Australia. The framework explicitly addresses where false positive vs. false negative errors matter most, how uncertainty should propagate into decisions, and when investing in SDM construction is worthwhile vs. acting immediately.

## Key Findings
1. Fewer than 1% of SDM papers in peer-reviewed literature demonstrably target or inform real conservation decisions.
2. Successful examples of SDMs supporting conservation exist but are largely confined to grey literature (government reports, management plans).
3. SDMs can inform most stages of structured decision making, from problem framing through trade-off assessment.
4. The costs of false positives and false negatives vary by decision context — for invasive species management, false negatives at the pre-border stage are more serious than false positives.
5. Ensemble GCM projections capture only climate scenario uncertainty; SDM construction choices, species data quality, and model goodness-of-fit represent additional, often ignored, uncertainty sources.
6. Spatial conservation prioritisation tools (Marxan, Zonation) can incorporate SDM uncertainty directly into reserve design.
7. When population persistence predictions are needed (e.g., translocation, critical habitat), SDMs alone are insufficient and must be coupled with population dynamics models.
8. Time urgency affects whether investing in SDM construction is worthwhile — in some cases, immediate action may be preferable to waiting for better models.
9. "Translators" — people who understand both the modelling and the decision process — are needed to bridge the gap between modellers and decision makers.

## Limitations
- The paper is a framework proposal with illustrative case studies, not a systematic comparison of SDM-supported vs. non-SDM-supported conservation outcomes.
- The claim that <1% of SDM papers target conservation decisions depends on how "targeting decisions" is defined and measured.
- The grey literature examples, while compelling, are harder to evaluate for methodological rigor than peer-reviewed studies.
- The framework does not address how to resolve disagreements between modellers and decision makers about acceptable uncertainty thresholds.
- Political and institutional barriers to SDM uptake are acknowledged but not deeply explored.

## Connections
- Directly cites and builds on [[elith2009-sdm-review]] (Elith is a co-author) regarding the gap between SDM development and real-world application.
- The uncertainty discussion extends the [[ensemble-forecasting]] framework of [[araujo2007-ensemble-forecasting]] by identifying uncertainty sources beyond GCM ensembles.
- The discussion of model evaluation in decision contexts (false positive/negative trade-offs) connects to [[allouche2006-tss-accuracy]] and the choice of threshold-dependent metrics.
- The call for coupling SDMs with population dynamics models relates to [[elith2010-range-shifting]]'s integration of mechanistic and correlative models.
- The Marxan/Zonation discussion links to [[reserve-selection]] as a concept.

## Open Questions
- How can the conservation impact of SDMs be measured and tracked systematically?
- What institutional structures best support the "translator" role between modellers and decision makers?
- How should SDM uncertainty be communicated to non-technical decision makers without causing paralysis?
- Under what conditions does the additional investment in hybrid SDM-population models justify the cost over SDMs alone?
- Can the structured decision-making framework be standardised across conservation agencies?
