# Detection scope and non-goals

## Intended observable

The method attempts to detect material- and geometry-dependent changes in
structured-light modulation transfer on visible surface patches. It may respond
to scattering, blur, absorption, roughness, film, droplets, scratches, pose drift
or illumination change. The current scalar `q` is an abstract equivalent blur
proxy in screen-pixel².

## It does not directly detect

- bacteria, viruses, fungi, species, strains, viability, CFU, ATP, proteins,
  allergens, toxins, or a named chemical;
- sterility, disinfection, regulatory compliance, or clinical safety;
- invisible residue whose optical response is indistinguishable from clean;
- occluded, shadowed, highly curved, transparent/translucent, or inaccessible
  areas outside a validated material/pose envelope.

## Operational meaning

- `PASS`: the retained optical proxy is below its model threshold in both states,
  all validity checks pass, and the pixel was visible. It means neither hygienic
  nor microbiological clearance.
- `FLAG`: at least one retained state is inconsistent with the accepted clean
  transfer envelope. It does not identify the cause.
- `UNKNOWN`: the system cannot support either conclusion under its declared
  bounds. It is a safety output, not missing data to be silently discarded.

Material classes require separate references and acceptance envelopes. Claims may
only expand after coupon studies establish response, interference, repeatability,
false-clean rate, false-flag rate and coverage for a named surface/residue pair.

