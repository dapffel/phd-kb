# Assessing the accuracy of species distribution models: prevalence, kappa and the true skill statistic (TSS)

**Authors:** Omri Allouche, Asaf Tsoar, Ronen Kadmon
**Journal:** Journal of Applied Ecology, 43(6), 1223–1232
**Year:** 2006
**DOI:** 10.1111/j.1365-2664.2006.01214.x

## Summary

The kappa statistic is the most widely used measure for presence–absence model performance, but it is inherently dependent on prevalence, introducing statistical artefacts. The authors provide a theoretical explanation for this dependence and introduce the true skill statistic (TSS) as an alternative that is independent of prevalence while retaining kappa's advantages.

## Theoretical Analysis

Kappa can be reformulated in terms of prevalence (P), sensitivity (Sn), and specificity (Sp). The analysis shows kappa responds unimodally to prevalence — the prevalence that maximizes kappa depends on the ratio between sensitivity and specificity. TSS is defined as: TSS = Sensitivity + Specificity − 1. Like kappa, TSS accounts for both omission and commission errors and success due to random guessing, ranging from −1 to +1. Unlike kappa, TSS is not affected by prevalence or the size of the validation set.

Computer simulations confirmed TSS scores were largely unaffected by prevalence while kappa exhibited a unimodal response.

## Empirical Analysis

128 species of woody plants in Israel were modeled using Mahalanobis distance with three climatic predictors (mean annual rainfall, mean daily temperature of August, mean minimum temperature of January). Validation used 96 independent sites of 5×5 km.

Results: Kappa showed a unimodal response to prevalence (quadratic term negative and highly significant, p < 0.001, R² = 0.12). TSS showed a decreasing linear response (R² = 0.13), matching AUC's pattern. Spearman correlation between AUC and TSS (0.85) was higher than between AUC and kappa (0.65).

## Key Conclusions

- Kappa is unsuitable for comparing model accuracy between species or regions due to prevalence dependence
- TSS compensates for kappa's shortcomings while keeping all advantages
- TSS is a special case of kappa when prevalence = 0.5
- TSS can easily accommodate unequal weighting of sensitivity and specificity
- TSS is recommended as the threshold-dependent accuracy measure alongside threshold-independent AUC

## TSS Formula

TSS = (ad − bc) / ((a+c)(b+d)) = Sensitivity + Specificity − 1

Where a = true positives, b = false positives, c = false negatives, d = true negatives.
