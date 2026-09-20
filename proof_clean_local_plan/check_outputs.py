#!/usr/bin/env python3
"""Check numerical/file integrity. A pass is NOT permission or readiness to submit."""
from pathlib import Path
import csv,json,math,sys
R=Path(__file__).resolve().parent;O=R/'outputs'
required=['environment.json','test_results.json','benchmark.csv','benchmark_run.json',
          'stress.csv','stress_run.json','summary.json','report.md','example_map.npz']
errors=[]
for name in required:
    if not (O/name).is_file():errors.append('missing '+name)
if errors:
    print('\n'.join(errors));sys.exit(1)
summary=json.loads((O/'summary.json').read_text())
tests=json.loads((O/'test_results.json').read_text())
if not tests['passed'] or tests['tests_run']!=8:errors.append('Expected all eight default unit tests to pass')
for k in ['physical_detection_validated','novelty_established','system_trl_certified']:
    if summary.get(k) is not False:errors.append('Unsupported claim flag: '+k)
if summary.get('evidence_type')!='SYNTHETIC_ONLY':errors.append('Missing synthetic evidence label')
for fn in ['benchmark.csv','stress.csv']:
    with (O/fn).open() as f:rows=list(csv.DictReader(f))
    for i,r in enumerate(rows):
        counts=sum(int(r[k]) for k in ['unknown_pixels','pass_pixels','flag_pixels'])
        if counts!=int(r['pixels']):errors.append(f'{fn} row {i}: status counts inconsistent')
        p=sum(int(r[k]) for k in ['proxy_positive_called_pass','proxy_positive_flagged','proxy_positive_unknown'])
        if p!=int(r['proxy_positive_pixels']):errors.append(f'{fn} row {i}: positive counts inconsistent')
        if r['evidence_type']!='SYNTHETIC':errors.append(f'{fn} row {i}: missing label')
    expected=(6 if fn=='benchmark.csv' else 12)
    if len({r['condition'] for r in rows})!=expected:errors.append('Incomplete conditions: '+fn)
    if fn=='benchmark.csv':
        unsafe=sum(int(r['proxy_positive_called_pass']) for r in rows if r['method']=='bounded_interval')
        if unsafe:errors.append(f'Model-consistent benchmark has {unsafe} unsafe proxy passes; inspect error propagation')
        if len({r['method'] for r in rows})!=6:errors.append('Missing benchmark method')
result={'pipeline_integrity_passed':not errors,'errors':errors,
        'submission_readiness':'NOT_ESTABLISHED; human contribution, novelty, physical scope and agreement review required',
        'physical_validation':False,'experimental_system_trl3':False}
(O/'integrity_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:sys.exit(1)
