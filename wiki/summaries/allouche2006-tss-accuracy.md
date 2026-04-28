---
title: "Assessing the accuracy of species distribution models: prevalence, kappa and the true skill statistic (TSS)"
created: 2026-04-28
updated: 2026-04-28
type: summary
sources:
  - allouche2006-tss-accuracy.pdf
---

## Citation
Allouche, O., Tsoar, A. & Kadmon, R. (2006) Assessing the accuracy of species distribution models: prevalence, kappa and the true skill statistic (TSS). *Journal of Applied Ecology*, 43(6), 1223–1232. doi: 10.1111/j.1365-2664.2006.01214.x

## TL;DR
Cohen's kappa, the most widely used accuracy measure for presence–absence species distribution models, is inherently dependent on species prevalence, producing a unimodal bias. The authors introduce the true skill statistic (TSS = Sensitivity + Specificity − 1) as a prevalence-independent alternative and validate it both theoretically and empirically using 128 woody plant species in Israel.

## Key Concepts
- [[model-evaluation]] — central topic; comparing accuracy metrics for species distribution models
- [[true-skill-statistic]] — the proposed prevalence-independent accuracy measure (TSS = Sensitivity + Specificity − 1)
- [[kappa-statistic]] — widely used but shown to be prevalence-dependent, producing unimodal bias
- [[species-distribution-models]] — the class of models being evaluated
- [[sensitivity-specificity]] — the two components of TSS; sensitivity quantifies omission errors, specificity quantifies commission errors
- [[auc-roc]] — threshold-independent measure shown to correlate more strongly with TSS (r=0.85) than with kappa (r=0.65)
- [[prevalence]] — proportion of sites where a species is present; the source of kappa's bias

## Methodology
The authors first derive kappa analytically in terms of prevalence, sensitivity, and specificity to show why it responds unimodally to prevalence. Computer simulations (100,000 confusion matrices per prevalence level, 99 levels) confirmed the theoretical predictions. Empirical validation used Mahalanobis distance models for 128 woody plant species in Israel, with three climatic predictors (mean annual rainfall, August mean daily temperature, January mean minimum temperature) and 96 independent 5×5 km validation sites. Five accuracy measures (kappa, TSS, AUC, sensitivity, specificity) were regressed against prevalence using linear and quadratic models.

## Key Findings
1. Kappa responds unimodally to prevalence; the prevalence maximizing kappa depends on the ratio of sensitivity to specificity.
2. TSS (Sensitivity + Specificity − 1) is mathematically independent of both prevalence and validation set size.
3. In the empirical analysis, kappa showed a significant unimodal response to prevalence (quadratic R² = 0.12, p < 0.001), while TSS showed a decreasing linear response (R² = 0.13) matching AUC's pattern.
4. The correlation between AUC and TSS (0.85) was substantially higher than between AUC and kappa (0.65), supporting TSS as a better threshold-dependent companion to AUC.
5. The decreasing TSS with increasing prevalence reflects a true ecological phenomenon: widespread species occupy wider niches, increasing commission errors (reduced specificity).
6. TSS is a special case of kappa when prevalence equals 0.5 (equal presences and absences).
7. TSS can accommodate unequal weighting of sensitivity and specificity in a straightforward manner, unlike kappa.

## Limitations
- The empirical test used only one modeling technique (Mahalanobis distance); generalizability to other SDM methods was not tested.
- TSS has high variance at extreme prevalence levels (very rare or very common species), though its coefficient of variation is similar to kappa's.
- The paper does not address how TSS performs with presence-only models (which cannot produce confusion matrices without a threshold).
- The study is restricted to one geographic region (Israel) and one taxonomic group (woody plants).

## Connections
- Directly relevant to [[ensemble-forecasting]] (Araújo & New, 2007), where model evaluation metrics are needed to assess ensemble members.
- The Mahalanobis distance method used here connects to [[species-distribution-models]] techniques.
- TSS originates from weather forecast verification, linking to the [[model-evaluation]] literature in meteorology (Heidke 1926, also known as the Hanssen–Kuipers discriminant).
- TODO: connect to other SDM evaluation papers in the wiki.

## Open Questions
- Does TSS maintain its advantages across different SDM techniques (not just Mahalanobis distance)?
- How should TSS be used when models produce continuous probability outputs rather than binary predictions?
- Is the observed negative relationship between prevalence and accuracy (TSS, AUC) consistent across regions and taxa?
- How do TSS-based model comparisons change conclusions relative to kappa-based comparisons in published studies?
