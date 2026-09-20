# Physical evidence matrix

Updated 2026-09-20. This is a literature-grounded feasibility map, not a claim
that the project has measured any residue. No project hardware experiment or
calibration dataset exists. “Direct” below means the cited work measured a
related residue/material/observable; it does not transfer a limit of detection
to this architecture.

## Decision summary

The literature narrows, but does not remove, the major physical assumption.
Real contamination can change specular return, polarization, wavelength ratios,
scatter/haze, and thin-film interference. The strongest quantitative support for
the proposed v2 diversity channel is on stainless steel: a 469/895-nm ratio
separated wet poultry residues diluted 1:100 from water/stainless background at
94.0% accuracy; 527/580-nm bands separated dry residues at up to 99.7% in that
study ([Cho et al.](https://www.sciencedirect.com/science/article/abs/pii/S0168169907000725),
S22). These are classification accuracies for that dataset, not concentration
or mass detection limits and not project performance.

The strongest negative evidence is equally important. On a polished stainless
substrate, visible scattering changed little below roughly 2 µm film thickness
and rose rapidly only beyond 2–3 µm for the tested molecular contaminant films
([NASA TN D-6585](https://ntrs.nasa.gov/citations/19720007973), S24). A clear,
smooth, sub-micron or index-matched film can therefore be weak in the v1
modulation/scatter observable even while it changes another optical state. A
residue exactly matching clean in every retained state remains impossible to
distinguish optically.

A second stainless-steel study used 400–1000 nm hyperspectral data for six
dilutions of spinach and potato juice and reported 0.94 validation accuracy for
both residue families. This supports spectral observability for those prepared
droplets, while also showing that reported classifier accuracy is not a mass LOD
or a guarantee under new finishes ([Aboonajmi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8122335/),
S41). A separate fluorescence system reported minimum detected blob diameters of
0.13 mm on stainless and 0.21 mm on plastic; that modality is outside the retained
elastic-reflectance architecture, but the material-dependent spatial boundary is
direct warning evidence for the new small-support failure class (S42).

## Residue × material × observable evidence

| Residue / morphology | Material | Measured or supported observable | Quantitative anchor | Evidence strength for this project | Consequence |
|---|---|---|---|---|---|
| Poultry feces, ingesta, blood, meat, fat, skin fluids; wet and dry | Stainless steel | Multispectral reflectance ratios | Wet 1:100 dilution: R895/R469, 94.0%; dry 1:100: 527/580 nm, 99.7% in the source dataset | Direct material/residue family; different optics and classifier | Wavelength diversity adds genuine information; it is not a threshold retune |
| Spinach and potato juice, six dilutions | Stainless steel | 400–1000 nm hyperspectral reflectance | CNN validation accuracy 0.94 for both residue families in the study | Direct surface/residue evidence; model and split are study-specific | Confirms spectral contrast can persist across dilution, not a transferable LOD |
| Beef, chicken, apple, mango, skim milk before/after detergent cleaning | 304 stainless steel | UV-visible illuminated area; strong residue/material/wavelength interaction | 365–490 nm tested; preferred bands differed by residue, and 490 nm often exposed surface structure rather than residue | Direct, but illumination includes fluorescence/visible response outside the retained purely elastic model | A single wavelength is fragile; material-conditioned bands are required |
| Same food residues | Fibre-reinforced plastic | UV-visible response | 365–490 nm; preferred band groups differed from stainless and aluminium | Adjacent to plastic/HDPE, not the same polymer/finish | Plastic cannot inherit a steel calibration; background structure can dominate |
| Peanut-butter soil from fouled detergent suspension | Stainless steel vs HDPE | Surface coverage, morphology, epifluorescence, FTIR/EDX; roughness and wettability | Detergent cases: stainless 3–21% coverage vs HDPE 0.3–1.3%; roughness and contact angle differed substantially | Direct residue deposition evidence; optical channel differs | Residue support and morphology are material-dependent; uniform-film simulation is inadequate |
| Spinach/olive-oil fluorescent blobs | Stainless steel vs plastic | UV/visible fluorescence imaging and segmentation | Reported minimum blob diameter 0.13 mm on steel vs 0.21 mm on plastic | Direct spatial/material evidence; different excitation/observable | Pixel support and background material change the detection boundary; no universal stain-size threshold |
| Latent fingerprint / sebum-like ridge residue | Plastic, stainless steel and other common objects | Specular reflection and polarization | Non-contact recovered images were reported comparable to existing methods in cases | Direct optical mechanism; no project LOD | Polarization can expose residue invisible to ordinary intensity, but only if it changes polarization |
| Transparent water | Industrial surfaces (conference samples) | Four-channel polarization under RGB dome illumination | Demonstrated as a route for transparent-liquid inspection; abstract gives no transferable error/LOD | Direct mechanism, incomplete quantitative evidence | Polarization is promising for water films, not guaranteed for all films |
| Crude and vegetable oil on water | Liquid background | Degree of linear polarization versus viewing geometry | Peak linear polarization 40–70% crude and 20–50% vegetable oil in the source study | Direct polarimetric contrast, but wrong substrate/application | Polarization can add information; its magnitude is strongly angle-dependent and cannot be transferred to solid coupons |
| Dust/soiling | Glass mirror | Specular reflectance and area distribution | 22-day soiling: mean reflectance 52.3% vs 95.2% cleaned at 656 nm, 15°, 12.5 mrad; 91.4% vs 0.001% of area below 70% | Direct and quantitative, but outdoor dust is easier than molecular film | Particles/rough deposits should be among the easiest classes for active reflectance |
| Airborne soiling | Glass | Total reflectance, transmittance and diffuse transmittance/haze | Study correlates modern-glass soiling with optical and chemical measures | Direct material; environment differs | Reflection plus haze/transmission can reveal particles, but transmission is not always accessible |
| Water, silicone oil, aromatic/aliphatic hydrocarbon films | Reflective stainless steel at cryogenic temperature | Visible scatter, reflectance and IR emissivity vs film thickness | Visible scatter little changed below ~2 µm; rapid rise beyond 2–3 µm over 0–20 µm films | Direct substrate/film/scatter evidence; temperature and surface differ | Thin clear films are a hard v1 case; scattering alone cannot support broad sensitivity claims |
| Crude-oil smear | Glass | Reflectance suppression by thin-film interference | Qualitative measured suppression; no project-band LOD | Direct mechanism | A clear film can decrease or increase reflectance depending on thickness, angle and wavelength; sign-only rules fail |
| Optically thin contamination | Transparent surfaces / glass | BRDF/BTDF from interface, optical thickness and scattering | Analytic radiative-transfer model demonstrated against rendered/photographic cases | Mechanistic adjacent evidence | A joint interface + film + scattering model is more credible than a blur-only proxy |
| Particulate contamination | Optical surfaces | BRDF as function of particle size, shape and areal density | Calculated BRDF agreed with measurements within uncertainty for most tested angles | Direct mechanism, different cleanliness use case | Multi-angle scatter is informative for particles and crystals |
| Clean/soiled ware controls | Glass and ceramic tile | Material-specific luminosity under controlled illumination | Patent teaches clean/soiled control wares and ware-type-specific settings; no independent performance dataset | Prior-art/engineering evidence, not scientific validation | Ceramic is currently the weakest evidence row; it needs dedicated coupon measurements |
| Detergent crystals / mineral scale | Glass, steel, plastic, glazed ceramic | Expected scatter, depolarization and spectral albedo | No sufficiently matched quantitative source located | Mechanistic inference only | Do not claim a detection limit; coupon testing is mandatory |
| Smooth index-matched or response-matched residue | Any | None within retained states by construction | Identical observation distributions imply zero discriminative information | Information-theoretic boundary | Must remain PASS/UNKNOWN indistinguishable from clean unless another responsive state is added |

## Material interpretation

- **Stainless steel:** strongest evidence base, but highly specular response makes
  water, pose and illumination confounders. Organic spectral ratios, polarization
  and multi-angle observations have real support. Thin clear films remain hard.
- **Glass:** dust and optically thicker contamination strongly alter specular
  reflectance/haze; oil films can produce interference. Transparent, smooth films
  can be locally degenerate at one wavelength/angle, which motivates diversity.
- **Plastic / HDPE:** roughness, hydrophobicity, autofluorescence and molding
  texture vary widely. The 2026 soil study found different coverage and morphology
  from steel, so a material-specific clean reference is necessary but not
  sufficient.
- **Glazed ceramic:** Fresnel behavior is plausible and cleaning-specific optical
  control precedent exists, but the search found little quantitative native-
  residue evidence matching this architecture. It remains a physical-validation
  priority rather than a supported generalization.

## Easiest and hardest expected classes

Expected easiest, conditional on the literature and model: optically thick
particles/dust, detergent crystals or dried deposits that add scatter; absorbing
or spectrally structured organic smears; and ridge/film residues that measurably
alter polarization or specular return.

Expected hardest: sub-micron clear films with little scatter; water or oil near a
single-state reflectance degeneracy; small stains near the registration/point-
spread boundary; residue on strongly textured plastic; and any residue whose
BRDF/spectrum/polarization matches the clean surface over every measured state.

## Data that still do not exist

No source supplies the joint distribution needed for a defensible project LOD:
residue mass or thickness × stain size × material finish × wavelength × angle ×
polarization × structured-light modulation under field noise. The new simulator
therefore uses literature-supported mechanisms but assumption-driven parameters.
Its numbers cannot replace the coupon protocol.

## Key sources

- [Cho et al., multispectral poultry-residue reflectance](https://www.sciencedirect.com/science/article/abs/pii/S0168169907000725)
- [Jespersen et al., wavelength × food residue × surface study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4252410/)
- [Lin et al., polarization/specular latent-fingerprint imaging](https://opg.optica.org/josaa/abstract.cfm?uri=josaa-23-9-2137)
- [Fraunhofer, polarization imaging of transparent water contamination](https://publica.fraunhofer.de/entities/publication/074c8a49-cf5e-4ef9-901f-3eef59ee93dd)
- [NASA TN D-6585, contaminant film thickness vs scatter](https://ntrs.nasa.gov/citations/19720007973)
- [NREL, spatially resolved glass-mirror soiling reflectance](https://www.nrel.gov/docs/fy11osti/49164.pdf)
- [USGS, oil-smear thin-film interference on glass](https://www.usgs.gov/publications/measured-reflectance-suppressed-thin-film-interference-crude-oil-smeared-glass)
- [Dirty Glass BRDF/BTDF model](https://diglib.eg.org/items/2211d001-3ee3-4228-aa34-ccf479ef29ad)
- [Stainless/HDPE soil adsorption study](https://doi.org/10.1016/j.fbp.2026.03.023)
- [VNIR spinach/potato residue study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8122335/)
- [Handheld fluorescence system and material-dependent blob size](https://pmc.ncbi.nlm.nih.gov/articles/PMC8588002/)
- [Oil/water polarimetric discrimination](https://opg.optica.org/abstract.cfm?uri=hise-2015-HW2B.4)
