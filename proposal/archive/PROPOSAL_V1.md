# Proposal v1 — bounded active-reflectance screening

## Participation type, solution level and partnering

Participation type: **[PARTICIPANT TO COMPLETE]**. Solution level: TRL 2.
Partnering: yes, for representative surfaces, independent ground truth, optical
hardware engineering and professional-site validation.

## Problem and opportunity

Professional cleaning checks are often visual or based on a small number of
contact samples. We propose non-contact active-reflectance screening that maps
optical-transfer changes over visible target surfaces. The research contribution
is not the use of structured light alone; it is a conservative decision workflow
with multiple references, bounded inference, an UNKNOWN class, controlled repeat
measurement and coverage accounting.

## Solution overview

A camera observes phase-shifted patterns reflected from a surface. Six spatial
frequencies in two orientations are acquired in a primary and a rigidly controlled
state. Three clean reference captures are checked for self-consistency. The system
fits a bounded transfer-change proxy and reports PASS, FLAG or UNKNOWN. PASS
requires both states and all quality checks; any FLAG wins. UNKNOWN triggers a
reacquisition or orthogonal ATP/chemical/microbiology test.

## Scientific basis and feasibility

Four-step demodulation estimates pattern modulation. Under the toy model,
`log(Mref/Msample)=a+x(b+q)`, with bounded clean geometry `b` and nonnegative
transfer-change proxy `q`. Quantization and declared additive error are propagated
into intervals. Published structured-light modulation and deflectometry studies
support the general optical mechanism, but do not validate this implementation.

The repository freezes a baseline and runs deterministic adversarial scenes. The
retained v1 changes three modeled false-clean failures—one dirty reference,
frequency-independent attenuation and geometry cancellation—from PASS to FLAG,
while deliberately leaving an optically invisible construction as PASS. This is
synthetic-only evidence.

## Performance expectations and limitations

In the fixed synthetic failure suite, v0 passed all four positive constructions;
v1 flagged three and passed the deliberately invisible one. In the 72-scene toy
benchmark, v1 had 0% proxy-positive PASS, 100% zero-proxy PASS and 17.54% UNKNOWN.
Pixels are descriptive, not independent trials.

An assumption-driven timing model predicts 21.3 minutes for 12 m² of target
surfaces in a conservative profile and 36.7 minutes for 25 m². No hardware timing
has been measured. The method does not identify organisms, ATP, viability,
sterility or chemicals. It cannot see inaccessible areas or optically invisible
residue, and material-specific coupon validation is required.

## Relevant experience

**[PARTICIPANT TO COMPLETE WITH ONLY VERIFIABLE EXPERIENCE, FACILITIES AND ROLE.]**
The prepared work product includes reproducible Python inference, deterministic
tests, an assumption ledger, adversarial failure registry, coverage model and a
preregistered coupon-study design. Do not present AI-generated project artifacts
as the participant's personal credentials.

## Risks and mitigations

Major risks are absent optical contrast, common-mode dirty references, material
and BRDF variation, exposure/noise outside bounds, registration failure, occlusion,
false interpretation of PASS, timing, prior-art overlap and reference aging.
Mitigations include material-specific references, a three-reference cassette,
locked RAW exposure, strict UNKNOWN behavior, coverage masks, operator guidance,
orthogonal escalation and a blinded coupon protocol. Invisible residues remain a
fundamental limitation.

## Development and collaboration

Gate 1 builds and calibrates a bench rig and tests observability. Gate 2 executes
the preregistered blinded coupon study and locks supported material/residue strata.
Gate 3 measures operator coverage and timing in relevant sites. Gate 4 develops a
cleanable field prototype and multi-site study. A partner would provide domain
surfaces, ground truth, industrial design, safety review and site access.
