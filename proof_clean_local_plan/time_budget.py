#!/usr/bin/env python3
"""Hypothetical acquisition budgets; no field measurement is implied."""
from pathlib import Path
import csv,math
R=Path(__file__).resolve().parent;O=R/'outputs';O.mkdir(exist_ok=True)
area=20.0;useful=0.65;frame=0.15;move=3.0;setup=120.0;report=60.0
# All numbers below are transparent, editable assumptions, NOT measured specifications.
rows=[]
for freq in [2,3,6]:
    for footprint in [0.01,0.05,0.1,0.25,1.0]:
        n=math.ceil(area/(footprint*useful))
        sample_frames=freq*2*4
        reference_frames=sample_frames  # conservative: a new matched reference per view
        computational_per_view=0.1  # assumption, not this machine's test latency
        seconds=setup+report+n*((sample_frames+reference_frames)*frame+move+computational_per_view)
        rows.append(dict(evidence_type='ASSUMPTION_ONLY',target_surface_area_m2=area,
                  assumed_nominal_view_area_m2=footprint,assumed_useful_fraction=useful,
                  views=n,frequencies=freq,sample_frames_per_view=sample_frames,
                  reference_frames_per_view=reference_frames,assumed_seconds_per_frame=frame,
                  assumed_move_seconds=move,assumed_compute_seconds_per_view=computational_per_view,
                  hypothetical_total_minutes=round(seconds/60,3),under_30_minutes_hypothetically=seconds<1800))
with (O/'time_budget.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(O/'time_budget_note.md').write_text('''# Hypothetical field-time budget

Every number in this table is an assumption, not a demonstrated capability. Target area is the **sum of target surface areas**, not room floor area. Useful field of view must be measured with real geometry, illumination, resolution and obstructions; a laptop screen has not been shown to illuminate these listed footprints adequately.

Formula: views = ceil(target_area / (nominal_view_area * useful_fraction)). Total time = setup + reporting + views * (sample and reference acquisition + repositioning + computing). Include new references conservatively. Reusing an archived reference may reduce time but needs matched geometry and trustworthy reference provenance.

An assumed budget below 30 minutes does not validate field feasibility. Invisible surfaces remain unassessed; moving an instrument across a room is not the same as covering all relevant surfaces. A physical experiment is needed to determine footprint, useful fraction, exposure, synchronization, repositioning and rescan time. A quality-check or acquisition failure adds time or yields UNKNOWN. No hardware price or sensitivity is assumed here.
''',encoding='utf-8')
print('Hypothetical budget written to outputs/time_budget.csv and time_budget_note.md')
