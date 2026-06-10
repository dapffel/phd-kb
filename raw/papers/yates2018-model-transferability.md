# Outstanding Challenges in the Transferability of Ecological Models

**Authors:** Katherine L. Yates, Phil J. Bouchet, M. Julian Caley, Kerrie Mengersen, Christophe F. Randin, Stephen Parnell, Alan H. Fielding, + 43 additional authors (50 experts total)
**Journal:** Trends in Ecology & Evolution (2018) 33(10):790–802
**DOI:** 10.1016/j.tree.2018.08.001
**Type:** Review

---

## Summary

Fifty experts identified priority knowledge gaps that, if filled, would most improve model transfers in ecology. These are summarised into six fundamental and six technical challenges, which underlie the need to intensify research on the determinants of ecological predictability and develop best practices for transferring models. The highest-priority gap is the identification of a widely applicable set of transferability metrics, and the most immediate way to improve transferability is encouraging models grounded in well-established mechanisms.

## Fundamental Challenges

### 1. Is model transferability trait- or taxon-specific?
Body size and trophic position are strong indicators of ecological predictability. Models for wide-ranging organisms with broad niches are harder to transfer than those for narrow-ranging specialists. Butterflies with long flight seasons had less accurate transfers; vascular plants with higher dispersal ability had better transferability. Species with greater behavioural or adaptive plasticity may be harder to model regardless of range size.

### 2. Which response variables make models more or less transferable?
Abundance data should facilitate greater transferability than presence–absence or presence-only data, though fitting abundance models remains difficult. Stronger correlations between abundance and occurrence expected for rare organisms. Community- and ecosystem-level models fitting shared environmental responses for multiple species could achieve higher transferability, but results are inconsistent. Integrated models uniting presence-only and presence–absence data offer further promise.

### 3. To what extent does data quality influence model transferability?
Accuracy of species records can be more important for transferability than spatial extent. Data of unverifiable quality should be avoided even if available over broader areas. Transfers hampered by imperfect detectability, spatial/temporal biases, insufficient sample sizes, omission of known drivers, and use of proxy variables. Virtual species simulations are a critical resource for tackling this gap.

### 4. How can sampling be optimized to maximize model transferability?
Samples encompassing full range of environmental conditions should avoid incomplete niche characterisation. Data often collected opportunistically. Data resolution influences model fit, prediction, and transferability. Combining geographically and environmentally distinct regions should increase transferability. Temporal replication helps capture natural variability.

### 5. How does model complexity influence model transferability?
Excessively complex models risk overfitting and producing predictions too specific to be transferable. Greater transferability generally expected in parsimonious models with smooth univariate response curves and few predictors. However, simplicity is not always beneficial — simple models can yield misleading predictions in new contexts. As complexity grows, potential for mismatch between reference and target conditions increases.

### 6. Are there spatial and temporal limits to extrapolation in model transfers?
Model transferability appears little related to geographic/temporal separation. Environmental dissimilarity is what matters most. Minimum level of environmental similarity required for transferable models remains unknown. Some authors caution against seeking inference beyond one-tenth of sampled covariate range. The "forecast horizon" defines the point beyond which sufficiently useful predictions can no longer be made.

## Technical Challenges

### 1. How can non-analog conditions be accounted for when transferring models?
Transferring into non-analogous environments brings well-documented perils, but predictive performance under novel conditions is rarely tested explicitly. Tools exist to visualise departure from initial covariate ranges (e.g., MESS, ExDet), but these cannot predict species' responses to novel conditions. Further development of these tools is needed.

### 2. How can nonstationarity and interactions be incorporated?
Species–environment relationships are rarely static — they vary with resource availability, ontogeny, population density. Species–environment relationships are context-specific. Methods incorporating functional responses and nonstationary coefficients enable enhanced transferability. Biotic interactions shape species' ranges at large spatial scales.

### 3. Do specific modeling approaches result in better transferability?
Mixed results across benchmarking studies. Random forests, boosted regression trees, MaxEnt, and GLM/GAMs all show high performance in some contexts. No "silver bullet" algorithm — species' characteristics can matter more than model choice. Model averaging avoids overreliance on a single technique. Mechanistic models could enhance transferability but remain mostly untested.

### 4. How should uncertainty be quantified, propagated, and communicated?
Uncertainty arises from sampling, data quality, environmental stochasticity, model specification, predictor choice, algorithm selection, and parameter estimation. Uncertainty varies spatially, propagates through multiple model phases, and has multiplicative effects such that its magnitude remains generally underappreciated. Clear protocols for measuring and reporting uncertainty are largely lacking.

### 5. How can we best transfer models through time?
Temporal transfers are often impossible to validate because future events are unknown. Hindcasting offers one solution but is limited by data biases. Space-for-time substitution assumes spatial heterogeneity approximates temporal variability. Some models project more reliably over centuries than shorter or longer timescales.

### 6. How should transferability be assessed?
Emerged as the highest-priority knowledge gap. True validation requires independent data, which are often unavailable. Cross-validation can approximate independence if structured to mimic prediction conditions. Consistent assessments require unified, widely applicable standard metrics enabling direct comparisons among studies, systems, and taxa.

## Correlative vs. Mechanistic Models (Box 3)

Correlative models draw statistical linkages between responses and environment but fail to capture underlying processes. Mechanistic models are built around explicit biological mechanisms and parameters. If formulated appropriately, mechanistic models can achieve greater realism and transferability. However, they suffer from the same nonstationarity issues and are not immune to inaccurate extrapolation. Limited availability of experimental data constrains mechanistic models. Some studies find both model types perform equally well. Arguments for blending approaches: using mechanistic knowledge to validate correlative models, using mechanistic variables as inputs to correlative models, or combining predictions from each class.

## Why Can Model Transfers Fail? (Box 4)

Models tightly fitted to calibration data often do not extrapolate well. Models assume quasi-equilibrium. Biotic interactions, disturbance, habitat loss, stochastic mortality, dispersal constraints prevent species from persisting in or accessing favourable habitats. Nonstationarity undermines transferability. Population density effects on apparent habitat preferences. Sampling biases, spatial/temporal autocorrelation. Scale mismatches between reference and target systems. Omission of important predictors. Stochastic events in evaluation data.

## Concluding Remarks

Transferability is critical to scientific understanding. Better transferability might not equate to better decisions without proper uncertainty communication. Models built with thorough consideration of ecological processes should have greater chance of being transferable. The fastest way to enhance predictions is to use them as tools for learning. Rigorous documenting of failures to transfer is important.
