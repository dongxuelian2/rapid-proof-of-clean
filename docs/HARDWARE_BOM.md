# Hardware bill of materials

Ranges are rough 2026 USD planning assumptions, excluding tax, integration and
certification. They are not quotations. No component has been purchased or tested.

## Minimal prototype

This tier answers “is a physical optical response observable?” It may not satisfy
the retained v1 12-bit/high-SNR controlled-state assumptions.

| Item | Function / approximate specification | Cost range | Why needed | Commodity? | Validation status |
| --- | --- | ---: | --- | --- | --- |
| Existing RAW camera or phone | manual exposure; lossless/RAW preferred | $0–1,000 | record reflected patterns | yes | TO VALIDATE linearity/bit depth |
| Monitor/tablet/projector | show phase-stepped sinusoidal patterns; ≥60 Hz desirable | $100–500 | active illumination | yes | TO VALIDATE gamma/flicker |
| Tripod + printed rigid fixture | fixed camera/display/coupon pose | $30–150 | reduce geometry variation | yes | NOT BUILT |
| Polarizer sheets, optional | exploratory glare-state control | $20–100 | test measured incremental contrast only | yes | candidate, not retained evidence |
| Calibration/clean coupons | material-matched references and fiducials | $20–100 | qualify reference and pose | yes/custom mix | NOT PREPARED |
| Hood/shroud | suppress ambient light | $20–100 | stabilize illumination | yes/custom | NOT BUILT |
| Existing laptop | local acquisition/processing | $0 | run pipeline | yes | software runs; camera interface absent |
| **Indicative total** | excluding existing camera/compute | **$170–950** | concept experiment only | — | ASSUMED |

## Practical field prototype

| Item | Function / approximate specification | Cost range | Why needed | Commodity? | Validation status |
| --- | --- | ---: | --- | --- | --- |
| Industrial camera + lens | global shutter, external trigger, ≥12-bit RAW, suitable FOV | $500–2,500 | controlled high-SNR acquisition | yes | TO SPECIFY/QUOTE |
| Compact projector/display | triggerable or synchronized; stable brightness; 60–120 Hz | $500–2,000 | repeatable patterns and timing | yes | TO SPECIFY/QUOTE |
| Rigid cleanable frame | guarded geometry, fiducials, working-distance stops | $300–1,500 | make controlled-state bound plausible | custom from commodity parts | NOT DESIGNED |
| Filters/polarization | matched optics where coupon data supports them | $100–500 | glare control, not automatic feature expansion | yes | OPTIONAL / TO VALIDATE |
| Reference cassette | keyed material coupons, IDs and replaceable protection | $100–500 | reference provenance/logistics | custom | NOT DESIGNED |
| Mini-PC/tablet | local processing, ≥16 GB RAM, storage and UI | $400–1,200 | field computation/reporting | yes | TO BENCHMARK |
| Enclosure/power/case | cleanable housing, battery, cables, transport | $200–1,000 | field deployment and safety | commodity/custom | TO DESIGN |
| **Indicative total** | before engineering/certification | **$2,100–9,200** | field concept | — | ASSUMED |

Reference stability, camera/projector synchronization and mapping, surface-safe
operation, cleanability, electrical safety, field of view and acquisition time are
gating tests. The architecture does not inherently require a wet laboratory, but
the current evidence does not establish field-grade affordability or performance.
