---
title: "From pattern extraction to design and inference: the evolving role of the macroecologist"
created: 2026-05-10
updated: 2026-05-10
type: summary
sources:
  - GEB-2026-macroecology.pdf
---

## Citation
Bates, A. E., Greentree, W. L., Clark, L., Dingwall, J., Herrington, C., Nikoo, M. L., Spriel, B., Weir, E., Qiao, H. J., Sheard, C. & Belmaker, J. (2026) From pattern extraction to design and inference: the evolving role of the macroecologist. *Global Ecology and Biogeography*.

## TL;DR
Macroecology's core value has shifted from pattern extraction (fitting models to large datasets) to design-and-inference (deciding what data should be collected, and interrogating what fitted models can causally support). AI tools have commodified the middle of the research workflow, relocating intellectual labour to the upstream (study design, data-stream architecture) and downstream (model interrogation, causal inference) ends.

## Key Concepts
- [[macroecology]] — the paper redefines the discipline's intellectual contribution in the AI era
- [[pattern-extraction]] — the historically dominant mode of macroecological work, now commodified by ML
- [[design-and-inference]] — the proposed new locus of macroecological value
- [[causal-inference]] — the paper argues macroecology must shift from correlative to explicitly causal methods
- [[model-interrogation]] — adversarial testing, structured holdouts, sensitivity analysis as core practice
- [[natural-experiments]] — undervalued source of causal evidence at macroecological scales (e.g., pink salmon, COVID lockdowns, marine heatwaves)
- [[data-stream-architecture]] — macroecologists as designers of future data infrastructure, not just users
- [[wallacean-shortfall]] — geographic and taxonomic sampling bias that AI cannot resolve and may amplify
- [[species-distribution-models]] — cited as an example of pattern-extraction now achievable with a single command
- [[model-extrapolation]] — models trained on temperate data will confidently misclassify tropical observations

## Methodology
This is a perspective/opinion piece, not an empirical study. The authors use a bibliometric analysis of Global Ecology and Biogeography (via Wiley advanced search, 26 January 2025) comparing frequency of correlative terms ("correlat*", "regression") against causal-inference terms ("structural equation model*", "path analysis", "acyclic"). They find a ~30:1 ratio of correlative to causal methods in the journal's archive. The paper synthesizes arguments from a graduate seminar (BIOL 550 Macroecology, University of Victoria, January 2025) and editorial experience at GEB.

## Key Findings
1. Pattern extraction has been commodified: a graduate student in 2026 can run a deep SDM with a single command and generate global projections in an afternoon.
2. The intellectual value of a macroecology paper has migrated from the analysis (middle of workflow) to study design (upstream) and model interrogation (downstream).
3. AI tools are effective within bounded problems but macroecology is largely an open-world problem requiring value-laden, contingency-dependent decisions that resist automation.
4. GEB's archive contains ~30 times more articles using correlative statistics than articles using explicitly causal tools (DAGs, SEMs, path analysis).
5. The durable human contributions are: deciding what is worth measuring, recognising what is missing from the data, and choosing among options not yet on any list.
6. Natural experiments (pink salmon cycles, COVID lockdowns, marine heatwaves) are an undervalued source of causal evidence that no algorithm could have planned.
7. Models trained on geographically biased data (temperate, Global North) will reproduce and amplify those biases when extrapolated.
8. The authors propose eight properties of impactful future macroecology papers, including: novel data collection, open code/data/workflow, model interrogation, explicit causal claims, confronting geographic bias, leveraging natural experiments, crediting AI pipelines, and declaring what the paper does not support.

## Limitations
- The bibliometric analysis is limited to a single journal (GEB) and uses simple keyword counts rather than content analysis.
- The paper does not empirically test whether the proposed shift has actually improved inference quality.
- The boundary between "bounded" and "open-world" problems is asserted rather than formally defined.
- The perspective is written primarily from a Western academic standpoint despite advocating for Global South inclusion.
- No concrete metrics are proposed for evaluating whether the eight properties improve research quality.

## Connections
- Directly relevant to [[species-distribution-models]] — SDMs are cited as the prime example of commodified pattern extraction.
- Connects to [[model-extrapolation]] — the paper warns that models trained on biased data produce flawed conclusions when transferred to under-sampled regions.
- Relates to [[model-evaluation]] — the call for structured holdouts (by biome, continent, decade) rather than random holdouts extends current evaluation thinking.
- The Wallacean shortfall discussion connects to geographic bias issues raised in [[species-distribution-models]].

## Open Questions
- How should funding agencies and journals operationalise the proposed shift in evaluation criteria?
- What specific training curricula would prepare macroecologists for design-and-inference work?
- Can the boundary between bounded and open-world problems be formalised, or will it shift as AI capabilities expand?
- How should macroecologists balance the slower, higher-effort work the paper advocates with career incentive structures that reward publication volume?
- What governance structures should determine AI pipeline transparency requirements?
