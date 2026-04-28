# Species Distribution Models: Ecological Explanation and Prediction Across Space and Time

**Authors:** Jane Elith, John R. Leathwick
**Journal:** Annual Review of Ecology, Evolution, and Systematics, 40, 677–697
**Year:** 2009
**DOI:** 10.1146/annurev.ecolsys.110308.120159

## Abstract

Species distribution models (SDMs) are numerical tools combining observations of species occurrence or abundance with environmental estimates. Used across terrestrial, freshwater, and marine realms for ecological and evolutionary insights and distribution prediction. Model realism and robustness influenced by predictor selection, modeling method, scale considerations, environmental-geographic interplay, and extrapolation extent. Current linkages between SDM practice and ecological theory are often weak. Remaining challenges: presence-only data methods, model selection and evaluation, biotic interactions, and model uncertainty.

## Key Topics

### Conceptual Underpinnings
SDMs combine ecological/natural history traditions with statistics and IT. Roots in early studies describing biological patterns in relation to gradients (Grinnell 1904). Individualistic species responses to environment support modeling individual species rather than communities. Modern SDMs emerged when field-based ecology (GLMs) converged with GIS and spatial data technologies.

### Scale
No single natural scale for ecological patterns. Climate dominates at global scale; topography and rock type at meso/toposcales. Appropriate scale dictated by study goals, system, and data. Little consensus on handling scale disparities in SDMs despite long-standing concepts.

### Geographic vs. Environmental Space
Critical distinction. SDMs with solely environmental predictors model variation in environmental space and are ignorant of geographic proximity. Spatial autocorrelation in predictions reflects autocorrelation of environment. Residual geographic patterning indicates missing predictors, model misspecification, or geographic factors (dispersal, biotic interactions).

### Explanation vs. Prediction
Early studies sought ecological insight; recent focus shifted to prediction. Two forms of prediction: (1) model-based interpolation to unsampled sites (usually reliable), (2) extrapolation to new geographic domains/climates (inherently risky — violates SDM assumptions).

### Functionally Relevant Predictors
Strong argument for using ecologically relevant predictors rather than convenient proxies. Distal predictors (elevation, depth) are indirect; proximal predictors (temperature, rainfall, water balance) are more functionally relevant. Even for prediction-only aims, relevant predictors improve results and are critical for extrapolation.

### Modeling Methods
- Envelopes and distance measures (BIOCLIM, Mahalanobis distance)
- Regression: GLMs, GAMs
- Machine learning: ANNs, boosted regression trees, random forests, GARP, MaxEnt, SVMs
- Machine learning methods can exceed conventional techniques in predictive performance
- Bayesian approaches available but under-utilized due to mathematical complexity

### Presence-Only Data
Museum records, radiotelemetry data. Methods: envelopes, GARP, ENFA, MaxEnt, regression with pseudoabsences. Debate about value of presence-only vs. presence-absence data. Presence-absence data conveys information about surveyed locations and prevalence.

### Model Evaluation
Diverse opinions on important properties and testing approaches. Common statistics: kappa, AUC, correlation coefficients. Need for comprehensive evaluation toolbox. Machine learning and weather-forecasting communities have expertise in predictive performance testing.

### Uncertainty
Results from data deficiencies and model specification errors. Model uncertainty received most attention (model averaging, consensus). Data errors include biases in species records and predictors. Often ignored despite importance.

## Summary Points
1. Modern SDMs represent convergence of site-based ecology with GIS/spatial data
2. Species distributions reflect interplay of geographic and environmental processes
3. Prediction: interpolation (reliable) vs. extrapolation (risky — requires special care)
4. Stronger links between ecological theory and SDM practice needed

## Future Issues
1. Uncertainty characterization and reduction
2. Expanded model selection/evaluation from statistics, weather forecasting, machine learning
3. Better methods for presence-only data biases and evaluation
4. Development-implementation-evaluation cycles for ecological insights
5. Modeling biotic interactions and ecological processes
6. Assessing SDM fitness for extrapolation purposes
