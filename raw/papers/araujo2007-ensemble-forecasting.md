# Ensemble forecasting of species distributions

**Authors:** Miguel B. Araújo, Mark New
**Journal:** Trends in Ecology and Evolution, Vol. 22, No. 1
**Year:** 2007
**DOI:** 10.1016/j.tree.2006.09.010

## Abstract

Concern over implications of climate change for biodiversity has led to the use of bioclimatic models to forecast the range shifts of species under future climate-change scenarios. Recent studies have demonstrated that projections by alternative models can be so variable as to compromise their usefulness for guiding policy decisions. Here, we advocate the use of multiple models within an ensemble forecasting framework and describe alternative approaches to the analysis of bioclimatic ensembles, including bounding box, consensus and probabilistic techniques. We argue that, although improved accuracy can be delivered through the traditional tasks of trying to build better models with improved data, more robust forecasts can also be achieved if ensemble forecasts are produced and analysed appropriately.

## Introduction

Attempts to predict climate change impacts on species distributions have often relied on the bioclimatic 'envelope' modelling approach, whereby empirical relationships between present-day distributions of species and climate variables are used to estimate distributions of species under future climate scenarios. For several (usually) pragmatic reasons, modelling typically involves selecting a favoured technique from a range of alternatives, and then justifying the choice by making reference to one or more published studies. However, despite claims of superiority for any given technique, independent evaluations of models have often been unable to demonstrate the pre-eminence of any single one.

Furthermore, studies have shown that projections by alternative models can be so variable as to compromise even the simplest assessment of whether species distributions should be expected to contract or expand for any given climate scenario. For example, Pearson and colleagues applied nine well documented bioclimatic modelling techniques to a standardised data set of four South African plant species and compared consistency in range predictions under current and future climates. Predicted distribution changes varied from a 92% loss to a 322% gain for one species and an equally wide variability in distribution change was predicted for the remaining species. Similarly divergent forecasts have been the rule in studies comparing alternative techniques to assess potential climate change-induced shifts in the distributions of European plants, amphibians and reptiles, and British breeding birds. These results challenge the common practice of relying on one single method to make forecasts of the responses of species to climate change scenarios or, if one accepted a more sceptical view, the usefulness of bioclimatic modelling in general for climate change impact studies.

Such variability in forecasts is not surprising given that bioclimate 'envelope' models are correlative and therefore sensitive to the data and the mathematical functions utilized to describe the distributions of species in relation to climate parameters. Process-based models that simulate bioclimate interactions from theoretical and experimental knowledge provide an alternative that is less dependent on empirical relationships; however, their implementation at the species level is difficult because of the complex processes and interactions that have to be represented; and variability in forecasts is also common.

A solution to intermodel variations that has been used in other fields is to utilize several models (herein termed 'ensembles') and use appropriate techniques to explore the resulting range of projections. Here, we argue that significant improvements on the robustness of a forecast can be achieved if an ensemble approach is used and the results analysed appropriately.

## Ensemble Forecasting

An ensemble, as introduced into statistical mechanics by J. Willard Gibbs in 1878, is an idealization consisting of a large (possibly infinite) number of copies of a system, considered all at once, each of which represents a possible state that the real system might be in at some specified time. A forecast ensemble is more narrowly defined as multiple simulations (copies) across more than one set of initial conditions (IC), model classes (MC), parameters (MP) and boundary conditions (BC). Each combination of IC, MC, MP and BC is one possible state of the system being forecasted.

The idea of ensemble forecasting dates back to 1969, when J.M. Bates and Nobel Prize winner in Economics C.W.J. Granger published their influential article 'The combination of forecasts'. Providing that individual forecasts contain some independent information, the authors observed that combined forecasts would yield lower mean error than any of the constituent individual forecasts. The idea had been formally developed by French mathematician P. Laplace in 1818: 'In combining the results of these two methods, one can obtain a result whose probability law of error will be more rapidly decreasing'. However it was not until the pioneering work of Bates and Granger that the idea of combining forecasts became established. Since then, hundreds of studies have been reviewed and applied to a variety of fields of research, including economics, management, systematics, biomedicine, meteorology and climatology. Surprisingly, these ideas have been slow to penetrate the ecological literature and it was only recently that ensemble forecasting was explicitly attempted in bioclimatic modelling of species distributions.

### Simulations for producing ensembles of forecasts

Ensembles of forecasts are produced by making multiple simulations across more than one set of IC, MC, MP and BC.

**Initial conditions:** The state of the real system (e.g. the distribution of species or factors that affect species) at the start of the simulation is often poorly known; it represents an incomplete realization of the real world. Small differences in IC will spawn different model trajectories (so-called 'chaos') around the system attractor(s). Models can be run with different ICs that are consistent with the available observations to explore the sensitivity of the predictions to IC uncertainty.

**Model classes:** Different MCs (e.g. polynomials and smoothing splines of different orders in general linear or additive models, nodes in classification and regression trees, hidden layers in neural nets, and various forms of process-based models) can all produce simulations that are consistent with available observations, and can be considered as competing and probably equally valid representations of the system of interest.

**Model parameters:** Statistical models typically have parameters that are estimated from the data. In classical statistics, the uncertainty in these parameters can be estimated. Multiple forecasts 'sampling' this parameter uncertainty are then possible. For process-based models, many important processes are parameterised, but the exact values of the parameters are unknown. Multiple simulations using different parameter values enable parameter uncertainty to be assessed.

**Boundary conditions:** Model forecasts are driven by an assumption about a change in BCs, defined broadly as predictors in a statistical model (e.g. climate variables). Typically, these BCs are uncertain, especially in the case of future anthropogenic pollution emissions. Alternative future BCs need to be explored, because the effect of differences between BCs in model predictions of species range shifts can be as large as differences between MCs.

## Combining Ensembles

Given an ensemble of model forecasts, how should they be analysed? The traditional approach consists of identifying the 'best' model from an ensemble of forecasts, where the best model is often judged to be one in which outputs match observed data as closely as possible. However, the ability to describe a given situation by calibration of MPs does not always coincide with the ability to represent adequately new observations using the existing calibration. This problem is particularly severe when predicted observations have a degree of spatial or temporal independence from the calibration set, which is the case for models projecting distributions of species under future climate scenarios.

Instead of picking the 'best' model from an ensemble, a more promising approach is to explore the resulting range of projections. For small ensemble sizes, two contrasting approaches are to use the ensemble to define a 'bounding box', or to generate a 'consensus' forecast. The appropriate approach is partly dependent on the question being asked, and the costs of being wrong. For medium to large ensemble sizes, raw data can be used to generate probability distribution functions (PDFs) for the forecast variable, but these will always be conditional on the sampling strategy across IC, MC, MP and BC.

### Bounding Box

The definition of a bounding box involves identification of the range in forecasts from the ensemble members. The approach is conservative in that it quantifies the range of forecasts, but makes no statement about the probability distribution or conditional probabilities of forecasts within the bounding box. It is acknowledged that the ensemble members are a subset of all possible IC–MC–MP–BC combinations and, therefore, only represent some limited projection of reality. Any averaging of ensemble member forecasts is considered to be unlikely to match the truth, and modellers do not attempt to estimate ensemble average or confidence limits for the average.

### Consensus Forecasting

In consensus forecasting, no assumption is made over the expected frequency distribution of the combined forecasts, but a measure of the central tendency (e.g. the mean or median) is calculated for the ensemble of forecasts. The rationale behind consensus forecasts is that, in averaging several models, the 'signal' that one is interested in emerges from the 'noise' associated with individual model errors and uncertainties. When combining forecasts for consensus, one can produce weighted and unweighted averages. Committee averaging takes a simple unweighted average of the predictions, essentially giving equal probability to each model. With Bayesian approaches, weights are proportional with the posterior probability of each model, which depend on how well the model fits the data and how many parameters are used. Stacking is one analogous procedure for estimating weights with least square regressions, but the idea is more general and can be used to obtain weights from measures of accuracy with any modelling technique. There is evidence from other disciplines that unweighted methods can yield cost-effective solutions, although this is only correct if model predictions are equally robust.

In the simple case of committee methods where the median forecast is taken, the consensus will always be more accurate than at least half of the individual forecasts. This is true independently of the distribution of individual forecasts, or their position in relation to the truth. If the truth falls within the range encompassed by all forecasts, less than half of the individual forecasts will be superior to the median forecast; at worst, if the truth lies outside the forecast range, consensus will be better than 50% of the forecasts.

### Probabilistic Forecasting

Probabilistic forecasting can be considered the 'end game' of ensemble forecasting. We accept the fact that models are different from reality and that, in most cases, we have many possible candidate models that pass some criteria about their ability to represent key aspects of the real system that we are interested in. For a large ensemble across multiple ICs, MPs, MCs and BCs, the frequency distribution of forecasts approaches a probability distribution. New developments in climate modelling where many tens of thousands of simulations have produced initial results where frequency histograms are starting to resemble PDFs. However, even these large ensembles are only sparsely sampling the possible IC–MC–MP–BC combinations. Estimating a PDF from the frequency distributions requires some form of emulation of the forecast over unsampled combinations, and the resulting PDFs remain conditional.

## Ensembles in Practice

The idea of combining forecasts is particularly appealing for those who are not convinced that a single model is closest to the truth in all circumstances and who sympathise with the view that all models are flawed, but provide useful information. Yet ensemble forecasting should not be viewed as an alternative to the more traditional approach of trying to build better models with improved data. Combined forecasts, although emphasizing the 'signal' emerging from the noise associated with different model outputs, remain dependent on individual predictions; better individual forecasts will yield a better combined forecast.

Whether to use a synthetically combined forecast (consensus or probabilistic) or bounded forecasts depends in part upon the way in which the forecast will be used. Conservation planners need to take a long-term view and rely on forecasts to support conservation decisions. The costs of being wrong can be high. When planning for climate change, the consequences of acting upon a forecast yielding false positives (e.g. species ranges predicted to expand in fact contract) are that resources are not spent on the species most in need of conservation action. Alternatively, acting on the basis of false-negative information might lead to an investment of resources in species that are not threatened by climate change.

A recent study demonstrated the success of a simple implementation of consensus forecasting in reducing both false negative and positive errors in predictions of observed distribution shifts among British breeding birds. False negatives were reduced from an average of 50% error to 0% (lower quartile = 31% versus 0%; upper quartile = 69% versus 0%, respectively) and comparable reductions in false positives were obtained.

Some writers have criticized the use of any single forecast (combined from several models or single-model), as it can lead to a decision that, although appropriate for the forecast, imposes a rigidity that might have serious negative consequences if the forecast deviates significantly from truth. The use of bounded forecasts offers an approach that, although honest, might be challenging for decision makers; it enables us to say, with some confidence, what will not happen.

### Modelling techniques incorporating ensemble forecasting

| Approach | Procedure |
|----------|-----------|
| Artificial neural networks | Models are run several times and the mean prediction used. Alternatively, the best fitting model can be selected. |
| Bagging trees | Multiple boot-strapped regression trees are fitted without pruning and the mean prediction used. |
| Boosted additive trees | The boosting algorithm iteratively calls the regression-tree algorithm to construct an ensemble of trees. The regression trees are fitted sequentially on weighted versions of the data. Predictions are finally combined using a majority vote criterion. |
| GARP | A genetic algorithm evolves a set of rules that best predicts the distribution of species based on bootstrapped samples of available information. |
| Maximum entropy (MAXENT) | Algorithm estimates the distribution of a species by finding the probability distribution of maximum entropy subject to the constraint that the expected value of each of a set of features under this estimated distribution closely matches its empirical average. |
| Random forests | Similar to bagging trees but each tree is grown with a randomized subset of predictors. Several trees are grown and the predictions aggregated by averaging. |

## Conclusions and Recommendations

Using ensemble forecasting has clear advantages over single-model forecasts. Different approaches to the analysis of the ensemble data have their own advantages and disadvantages, and their suitability will depend on the questions being asked. But if used appropriately, either individually, in combination, or in hybrid form, these approaches can enable more robust decision making in the face of uncertainty, and have much to offer to conservation planning.

Climatologists are now producing tens of thousands of simulations of future climates. Exploring these data will be necessary to provide comprehensive assessments of the possible impacts of climate change on biodiversity. The most comprehensive attempts to run ensembles of models of species distributions have spawned a limited number of combinations of MCs and BCs, yielding no more than 40 projections per species. Developments in bioclimate and climate modelling will rapidly force this number to increase to several thousands projections per species.

A serious limitation still includes the lack of appropriate software to run and combine large ensembles of models. If progress is to be made in the field of ensemble forecasting of species distributions, ecologists need to move fast, join efforts and abandon parochialism in software production. Open source platforms, such as that provided by the R project for statistical computing, might provide an adequate source of inspiration.

## References

1. Huntley, B. et al. (1995) Modelling present and potential future ranges of some European higher plants using climate response surfaces. J. Biogeogr. 22, 967–1001
2. Peterson, A.T. et al. (2002) Future projections for Mexican faunas under global climate change scenarios. Nature 416, 626–629
3. Thomas, C.D. et al. (2004) Extinction risk from climate change. Nature 427, 145–148
4. Thuiller, W. et al. (2005) Climate change threats plant diversity in Europe. Proc. Natl. Acad. Sci. U. S. A. 102, 8245–8250
5. Lehmann, A. et al. (2003) GRASP: generalized regression analysis and spatial prediction. Ecol. Model. 160, 165–183
6. Walker, P.A. and Cocks, K.D. (1991) HABITAT: a procedure for modelling a disjoint environmental envelope for a plant or animal species. Global Ecol. Biogeogr. Lett. 1, 108–118
7. Busby, J.R. (1986) A biogeographical analysis of Nothofagus cunninghamii (Hook.) Oerst. in southeastern Australia. Aust. J. Ecol. 11, 1–7
8. Carpenter, G. et al. (1993) DOMAIN: a flexible modelling procedure for mapping potential distributions of plants and animals. Biodiv. Conserv. 2, 667–680
9. Pearson, R.G. et al. (2002) SPECIES: a spatial evaluation of climate impact on the envelope of species. Ecol. Model. 154, 289–300
10. Stockwell, D.R.B. and Peters, D.P. (1999) The GARP modelling system: problems and solutions to automated spatial prediction. Int. J. Geogr. Inf. Syst. 13, 143–158
11. Olden, J.D. and Jackson, D.A. (2002) A comparison of statistical approaches for modelling fish species distributions. Freshw. Biol. 47, 1976–1995
12. Segurado, P. and Araújo, M.B. (2004) An evaluation of methods for modelling species distributions. J. Biogeogr. 31, 1555–1568
13. Elith, J. et al. (2006) Novel methods improve predictions of species' distributions from occurrence data. Ecography 29, 129–151
14. Pearson, R.G. et al. (2006) Model-based uncertainty in species' range prediction. J. Biogeogr. 33, 1704–1711
15. Thuiller, W. et al. (2004) Uncertainty in predictions of extinction risk. Nature 430, 10.1038/nature02716
16. Araújo, M.B. et al. (2006) Climate warming and the decline of amphibians and reptiles in Europe. J. Biogeogr. 33, 1712–1728
17. Araújo, M.B. et al. (2005) Reducing uncertainty in projections of extinction risk from climate change. Glob. Ecol. Biogeogr. 14, 529–538
18. Cramer, W. et al. (2001) Global response of terrestrial ecosystem structure and function to CO2 and climate change: results from six dynamic global vegetation models. Glob. Change Biol. 7, 357–373
19. Bates, J.M. and Granger, C.W. (1969) The combination of forecasts. Operat. Res. Quart. 20, 451–468
20. Laplace, P.S. (1818) Deuxième supplément à la Théorie Analytique des Probabilités, Courcier
21. Clemen, R.T. (1989) Combining forecasts: a review and annotated bibliography. Int. J. Forecast. 5, 559–583
22. Palm, F.C. and Zellner, A. (1992) To combine or not combine? Issues of combining forecasts. J. Forecast. 11, 687–701
23. Cheung, K.K.W. (2001) A review of ensemble forecasting techniques with a focus on tropical cyclone forecasting. Meteorol. Appl. 8, 315–332
24. Gregory, A.W. et al. (2001) Testing for forecast consensus. J. Bus. Econ. Stat. 19, 34–43
25. Makridakis, S. and Winkler, R.L. (1983) Averages of forecasts: some empirical results. Manage. Sci. 29, 987–996
26. Miyamoto, M.M. (1985) Consensus cladograms and general classifications. Cladistics 1, 186–189
27. Nilsson, J. et al. (2000) Consensus predictions of membrane protein topology. FEBS Lett. 486, 267–269
28. Sanders, F. (1963) On subjective probability forecasting. J. Appl. Meteorol. 2, 191–201
29. Benestad, R.E. (2004) Tentative probabilistic temperature scenarios for northern Europe. Tellus 56A, 89–101
30. Thuiller, W. (2004) Patterns and uncertainties of species' range shifts under climate change. Glob. Change Biol. 10, 2220–2227
31. Thuiller, W. (2003) BIOMOD: optimising predictions of species distributions and projecting potential future shifts under global change. Glob. Change Biol. 9, 1353–1362
32. Araújo, M.B. et al. (2005) Validation of species-climate impact models under climate change. Glob. Change Biol. 11, 1504–1513
33. Randin, C.F. et al. (2006) Are niche-based species distribution models transferable in space? J. Biogeogr. 33, 1689–1703
34. Araújo, M.B. et al. (2005) Downscaling European species atlas distributions to a finer resolution: implications for conservation planning. Glob. Ecol. Biogeogr. 14, 17–30
35. Prasad, A.M. et al. (2006) Newer classification and regression tree techniques: bagging and random forests for ecological prediction. Ecosystems 9, 181–199
36. Hastie, T. et al. (2001) The Elements of Statistical Learning: Data Mining, Inference and Prediction, Springer
37. McNees, S.K. (1992) The uses and abuses of "consensus" forecasts. J. Forecast. 11, 703–710
38. Stainforth, D.A. et al. (2004) climateprediction.net: a global community for research in climate physics.
39. Allen, M. (1999) Do-it-yourself climate prediction. Nature 401, 642
40. Allen, M.R. and Stainforth, D.A. (2002) Towards objective probabilistic climate forecasting. Nature 419, 228
41. Stainforth, D.A. et al. (2005) Uncertainty in predictions of the climate response to rising levels of greenhouse gases. Nature 433, 403–406
42. Smith, L.A. (2002) What might we learn from climate forecasts? Proc. Natl. Acad. Sci. U. S. A. 99, 2487–2492
43. Allen, M. et al. (2002) Model error in weather and climate forecasting.
44. Frame, D.J. et al. (2005) Constraining climate forecasts: the role of prior assumptions. Geophys. Res. Lett. 32, art. no.-L09702
45. Dessai, S. and Hulme, M. (2004) Does climate adaptation policy need probabilities? Climate Policy 4, 107–128
46. Winkler, R.L. (1989) Combining forecasts: a philosophical basis and some current issues. Int. J. Forecast. 5, 605–609
47. Box, G.E.P. (1979) Some problems of statistics and everyday life. JAMA 74, 1–4
48. Araújo, M.B. et al. (2004) Would climate change drive species out of reserves? An assessment of existing reserve selection methods. Glob. Change Biol. 10, 1618–1626
49. Pressey, R.L. and Cowling, R.M. (2001) Reserve selection algorithms and the real world. Conserv. Biol. 15, 275–277
50. Phillips, S.J. et al. (2006) Maximum entropy modeling of species geographic distributions. Ecol. Model. 190, 231–259
