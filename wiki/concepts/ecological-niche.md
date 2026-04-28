---
title: "Ecological Niche"
created: 2026-04-28
updated: 2026-04-28
type: concept
sources:
  - peterson2011-niches-distributions.pdf
  - elith2009-sdm-review.pdf
  - thuiller2005-climate-change-plants.pdf
---

## Definition
The ecological niche describes the set of environmental conditions under which a species can maintain viable populations. The concept has multiple meanings depending on emphasis: the Grinnellian niche focuses on broad-scale environmental requirements (scenopoetic variables like climate and topography), while the Eltonian niche focuses on local-scale resource consumption and biotic interactions. Most species distribution modelling operates in the Grinnellian framework.

## Background
The niche concept traces to Grinnell (1917), who used it to describe the climatic and habitat requirements determining the California Thrasher's geographic range, and Elton (1927), who emphasised a species' functional role within a community. Hutchinson (1957) formalised the niche as an n-dimensional hypervolume of environmental variables within which a species can persist indefinitely, distinguishing the **fundamental niche** (all conditions permitting survival, absent competitors) from the **realized niche** (the subset actually occupied given biotic interactions). [[peterson2011-niches-distributions]] provides the most rigorous modern treatment, arguing that decades of confusion stem from mixing fundamentally different variable types (scenopoetic vs. dynamically linked) under a single label.

## How It Works
[[peterson2011-niches-distributions]] formalises two complementary niche types:

**Grinnellian niche** — defined in E-space (environmental space) using [[scenopoetic-variables]]: climate, topography, solar radiation — variables not dynamically modified by the species. At geographic scales, the Grinnellian niche determines where intrinsic growth rate r > 0. This is what correlative SDMs estimate.

**Eltonian niche** — defined in resource space using dynamically linked (bionomic) variables: consumed resources, prey densities, competitor abundances. Requires mechanistic consumer-resource models with zero-growth isoclines. Relevant at local scales where species interactions shape community composition.

The **[[bam-diagram]]** unifies these perspectives geographically:
- **A** (Abiotic): regions where scenopoetic conditions support r > 0 (Grinnellian niche projected to G-space)
- **B** (Biotic): regions where biotic interactions permit persistence
- **M** (Movement): regions accessible via dispersal
- **G_O = A ∩ B ∩ M**: the occupied distributional area (realized range)
- **G_I = A ∩ B ∩ M^C**: the invadable area (suitable but inaccessible)

The **[[fundamental-niche]]** may include environmental combinations not currently existing anywhere — non-analogue environments. The "existing fundamental niche" (or "potential niche") is the intersection of the fundamental niche with the available E-space.

The distinction between scenopoetic and bionomic variables is not biotic vs. abiotic, but whether the variable is modified by the species' population dynamics. Forest structure, for example, is biotic but may be scenopoetic for a bird species whose population does not alter the forest.

## Key Results From Sources
- **[[peterson2011-niches-distributions]]**: The Grinnellian and Eltonian niches require fundamentally different mathematical representations. Grinnellian niches are simple subsets of E-space; Eltonian niches require mechanistic models with zero-growth isoclines and impact vectors. The BAM framework provides a unified geographic representation. SDM and ENM are related but not equivalent: SDM estimates areas in G-space, ENM estimates niches in E-space.
- **[[elith2009-sdm-review]]**: The authors prefer the neutral term "SDM" over "ecological niche model" to avoid implying that correlative models directly estimate niches. Weak links between niche theory and modelling practice remain the key obstacle to progress. Proximal (mechanistically grounded) predictors better capture the niche than distal proxies.
- **[[thuiller2005-climate-change-plants]]**: The bioclimatic envelope approach assumes species' current climatic envelopes (an approximation of the Grinnellian niche) reflect environmental preferences retained under climate change — supported by evidence for evolutionary conservatism of niches across timescales.

## Open Problems
- Can the BAM framework be made quantitative — estimating the actual sizes and overlaps of A, B, and M empirically?
- How to incorporate Eltonian niche effects (biotic interactions) into geographic-scale correlative SDMs without requiring impractical local-scale data.
- Whether the Grinnellian/Eltonian distinction holds at intermediate spatial scales, or a continuum of niche types is more appropriate.
- The extent to which niche conservatism holds under rapid climate change — the assumption underlying all projection-based SDM applications.
- How non-analogue environments (combinations outside the existing E-space) should be handled in niche estimation and distribution projection.

## Related Concepts
- [[species-distribution-models]]
- [[grinnellian-niche]]
- [[eltonian-niche]]
- [[fundamental-niche]]
- [[bam-diagram]]
- [[scenopoetic-variables]]
- [[e-space-g-space]]
- [[biotic-interactions]]
- [[model-extrapolation]]
