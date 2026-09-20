# Final system architecture

## Objective and decision unit

The candidate screens visible target-surface patches for changes in reflected
structured-light transfer relative to a controlled reference ensemble. Its
decision unit is a registered surface pixel/patch, not a room and not a microbe.
The output is `PASS`, `FLAG`, or `UNKNOWN`; `UNKNOWN` requires remeasurement or an
orthogonal test.

## Inputs

- three clean/reference observations for the declared material class;
- active illumination states: two orientations, six frequencies and four phases;
- primary and controlled measurement geometry plus pose/exposure metadata;
- test-surface frames, visibility mask and frame-completeness record.

## Core stages

1. qualify the reference ensemble and expose disagreement;
2. acquire structured active measurements in primary and controlled states;
3. validate registration, signal, saturation, closure and normalization bounds;
4. run bounded transfer inference and the gain guard;
5. remeasure invalid/ambiguous views under controlled geometry;
6. fuse to PASS, FLAG or UNKNOWN and write the coverage/action log.

## Acquisition

1. Prepare three dated, majority-clean reference captures for each material class.
2. Project two orientations × six spatial frequencies × four phase steps.
3. Capture a primary state and a registered, higher-SNR controlled-geometry state:
   96 live sample frames per field of view.
4. Log pose, exposure, saturation, visible mask, reference IDs and coverage.

The camera, display/projector and target are rigidly constrained for the second
state. This is a design requirement, not a demonstrated capability.

## Inference and confidence

- Four-phase demodulation estimates modulation amplitude.
- The model fits `log(M_ref/M_sample)=a+x(b+q)` where `q` is an equivalent
  Gaussian transfer-blur variance and `b` is bounded clean geometry variation.
- Deterministic error bounds propagate quantization and declared additive error.
- A 2-of-3 self-consistency rule selects the reference neighborhood.
- A bounded absolute log-gain guard detects modeled uniform attenuation.
- Any state `FLAG` wins; `PASS` requires both states to pass; all other cases are
  `UNKNOWN`.

Confidence is not a learned probability. It consists of reference-consensus
fraction, validity masks, interval separation, and coverage metadata.

## Failure containment

Low modulation, clipping, occlusion, closure failure, missing frames, inconsistent
references, or bounds violations must abstain. Common-mode dirty references,
optically invisible residue, and unmodeled material response remain major hazards.
No algorithmic confidence can recover a signal that the retained optics do not
observe.

## Remeasurement loop

`UNKNOWN` routes to: correct framing/exposure → reacquire primary and controlled
states → replace/verify references if inconsistency persists → use ATP, chemistry,
protein assay or microbiology when the decision requires biological or chemical
specificity. `FLAG` routes to reclean and repeat; persistent flags are escalated.

## Outputs

- `PASS`: no detectable deviation within the validated observable optical class
  and measurement bounds in both states; never “sterile” or “microorganism-free”;
- `FLAG`: an accepted observation exceeds the optical proxy envelope; cause unknown;
- `UNKNOWN`: bounds, observability, references, registration, frames or coverage
  are insufficient for either conclusion.

## Evidence boundary

The implemented architecture and synthetic behavior are reproducible. Hardware
timing, surface compatibility, residue sensitivity, field error rates and
operator performance are not measured.
