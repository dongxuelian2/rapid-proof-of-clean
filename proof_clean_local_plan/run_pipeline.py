#!/usr/bin/env python3
"""Offline, CPU-only synthetic feasibility pipeline. Never submits anything."""
from __future__ import annotations
import argparse, csv, datetime, hashlib, io, json, platform, sys, time, unittest
from pathlib import Path
import numpy as np
from src.core import infer,demodulate,UNKNOWN,PASS,FLAG
from src.simulation import make_scene,CONDITIONS,STRESSES
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'

def write_json(path,obj):
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def doctor(cfg):
    OUT.mkdir(exist_ok=True)
    data={'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),
          'processor':platform.processor(),'config_sha256':sha(ROOT/'config.json'),
          'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'evidence_type':cfg['evidence_type'],'gpu_required':False,'network_required':False,
          'code_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'src').glob('*.py'))}}
    write_json(OUT/'environment.json',data)
    print('Environment recorded; no GPU, account, paid API or network used.')

def tests():
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    OUT.mkdir(exist_ok=True)
    (OUT/'tests.txt').write_text(stream.getvalue(),encoding='utf-8')
    write_json(OUT/'test_results.json',dict(tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful()))
    print(stream.getvalue())
    if not result.wasSuccessful(): raise RuntimeError('Tests failed; stop and inspect outputs/tests.txt')

def thresholds(cfg):
    # Independent calibration scenes; no test labels or test frames are used.
    rng=np.random.default_rng(cfg['seed']+101)
    dc=[]; single=[]
    for _ in range(20):
        r,s,_,vis,_=make_scene(cfg,rng,'clean')
        mr=demodulate(r); ms=demodulate(s)
        dc.extend(np.abs(s[:,:,0:4].mean(axis=(0,1,2))-r.mean(axis=(0,1,2))).ravel())
        single.extend(np.abs(np.log(np.maximum(ms[:,-1],1e-9)/np.maximum(mr[:,-1],1e-9))).max(axis=0).ravel())
    return dict(dc=float(np.quantile(dc,.99)),single=float(np.quantile(single,.99)),
                note='Empirical calibration only. Baselines use separate clean calibration scenes; no statistical guarantee claimed.')

def benchmark(cfg,stress=False,small=False):
    OUT.mkdir(exist_ok=True)
    cal=thresholds(cfg);write_json(OUT/'baseline_calibration.json',cal)
    rng=np.random.default_rng(cfg['seed']+(303 if stress else 202))
    kinds=STRESSES if stress else CONDITIONS
    n=2 if small else (4 if stress else cfg['scenes_per_condition'])
    rows=[]; th=cfg['proxy_threshold_pixel2']
    start=time.perf_counter()
    for kind in kinds:
        for sid in range(n):
            r,s,q,visible,meta=make_scene(cfg,rng,kind)
            t=time.perf_counter();z=infer(r,s,cfg,visible);dur=time.perf_counter()-t
            mr=demodulate(r);ms=demodulate(s)
            dc=np.abs(s.mean(axis=(0,1,2))-r.mean(axis=(0,1,2)))
            ss=np.abs(np.log(np.maximum(ms[:,-1],1e-9)/np.maximum(mr[:,-1],1e-9))).max(axis=0)
            methods={'uniform_DC':np.where(dc>cal['dc'],FLAG,PASS),
                     'single_frequency_modulation':np.where(ss>cal['single'],FLAG,PASS),
                     'multi_frequency_point_estimate':np.where(z['ols']>=th,FLAG,PASS),
                     'bounded_interval':z['status']}
            if not stress:
                for label,idx in [('interval_two_frequencies',[0,5]),('interval_three_frequencies',[0,3,5])]:
                    methods[label]=infer(r,s,cfg,visible,indices=idx)['status']
            positive=q.max(axis=0)>=th
            trueclean=(q==0).all(axis=0)
            for method,status in methods.items():
                # All methods receive the same externally supplied visibility mask.
                status=np.where(visible,status,UNKNOWN)
                p=int(positive.sum());c=int(trueclean.sum())
                rows.append(dict(condition=kind,scene_id=sid,method=method,pixels=int(status.size),
                                 proxy_positive_pixels=p,exact_zero_proxy_pixels=c,
                                 proxy_positive_called_pass=int(((status==PASS)&positive).sum()),
                                 proxy_positive_flagged=int(((status==FLAG)&positive).sum()),
                                 proxy_positive_unknown=int(((status==UNKNOWN)&positive).sum()),
                                 exact_zero_proxy_called_pass=int(((status==PASS)&trueclean).sum()),
                                 exact_zero_proxy_flagged=int(((status==FLAG)&trueclean).sum()),
                                 unknown_pixels=int((status==UNKNOWN).sum()),pass_pixels=int((status==PASS).sum()),
                                 flag_pixels=int((status==FLAG).sum()),
                                 scope_positive_pass_fraction=float(((status==PASS)&positive).sum()/p) if p else '',
                                 zero_proxy_pass_fraction=float(((status==PASS)&trueclean).sum()/c) if c else '',
                                 unknown_fraction=float((status==UNKNOWN).mean()),
                                 bounded_inference_seconds=dur if method=='bounded_interval' else '',
                                 evidence_type='SYNTHETIC',
                                 assumed_physical_contamination_in_stress=meta['physical_label_simulated_only']))
            if kind=='patchy' and sid==0:
                np.savez_compressed(OUT/'example_map.npz',status=z['status'],q_truth=q,
                                    q_lower=z['lower'],q_upper=z['upper'],visible=visible)
    name='stress' if stress else ('smoke' if small else 'benchmark')
    with (OUT/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write_json(OUT/(name+'_run.json'),dict(scenes=n*len(kinds),elapsed_seconds=time.perf_counter()-start,
               seed=cfg['seed']+(303 if stress else 202),image_size=cfg['image_size'],
               note='Measured only on the machine running this file; not field acquisition time.'))
    print(f'{name}: {n*len(kinds)} synthetic scenes -> outputs/{name}.csv')

def aggregate(path):
    with path.open(encoding='utf-8') as f: return list(csv.DictReader(f))

def report(cfg):
    for p in ['benchmark.csv','stress.csv','test_results.json','environment.json']:
        if not (OUT/p).exists(): raise FileNotFoundError('Run missing stage first: '+p)
    rows=aggregate(OUT/'benchmark.csv'); stress=aggregate(OUT/'stress.csv')
    summaries=[]
    for method in dict.fromkeys(r['method'] for r in rows):
        sub=[r for r in rows if r['method']==method]
        def total(k):return sum(int(r[k]) for r in sub)
        pos=total('proxy_positive_pixels');clean=total('exact_zero_proxy_pixels');pix=total('pixels')
        scene_rates=[float(r['scope_positive_pass_fraction']) for r in sub if r['scope_positive_pass_fraction']!='']
        summaries.append(dict(method=method,proxy_positive_called_pass=total('proxy_positive_called_pass'),
                  proxy_positive_pixels=pos,false_pass_fraction=total('proxy_positive_called_pass')/pos,
                  zero_proxy_pass_fraction=total('exact_zero_proxy_called_pass')/clean,
                  unknown_fraction=total('unknown_pixels')/pix,
                  proxy_positive_flag_fraction=total('proxy_positive_flagged')/pos,
                  worst_scene_false_pass_fraction=max(scene_rates),
                  note='Pixel ratios are descriptive, not independent-sample confidence estimates.'))
    limits=[]
    for kind in STRESSES:
        sub=[r for r in stress if r['condition']==kind and r['method']=='bounded_interval']
        p=sum(int(r['pixels']) for r in sub)
        limits.append(dict(condition=kind,pass_fraction=sum(int(r['pass_pixels']) for r in sub)/p,
                          unknown_fraction=sum(int(r['unknown_pixels']) for r in sub)/p,
                          flag_fraction=sum(int(r['flag_pixels']) for r in sub)/p))
    result={'evidence_type':'SYNTHETIC_ONLY','physical_detection_validated':False,
            'novelty_established':False,'system_trl_certified':False,
            'metrics':summaries,'stress':limits,
            'config_sha256':sha(ROOT/'config.json')}
    write_json(OUT/'summary.json',result)
    text=['# Local synthetic feasibility report','',
    '**Evidence: synthetic model only. No oil, microorganism, professional room, camera or screen has been experimentally validated by this run.**','',
    '## Definitions','',
    'The proxy q is an excess Gaussian reflection-transfer blur variance in screen-coordinate pixels squared. It is not film thickness, CFU, protein mass, pathogen concentration, or a cleanliness standard. PASS is restricted to this proxy, the supplied reference and the assumed model.','',
    '## Benchmark','',
    '| Method | Proxy-positive called PASS | Zero-proxy PASS | UNKNOWN | Proxy-positive FLAG |',
    '|---|---:|---:|---:|---:|']
    for m in summaries:
        text.append(f"| {m['method']} | {m['false_pass_fraction']:.4%} | {m['zero_proxy_pass_fraction']:.2%} | {m['unknown_fraction']:.2%} | {m['proxy_positive_flag_fraction']:.2%} |")
    text +=['','These are descriptive synthetic pixel ratios; scenes share nuisance parameters, so pixels are not independent experimental samples. A zero count is not proof of zero real-world error. The bounded-error statement is an algebraic, model-conditional result.','',
             '## Stress tests and failure modes','',
             '| Condition | PASS | UNKNOWN | FLAG |','|---|---:|---:|---:|']
    for s in limits:text.append(f"| {s['condition']} | {s['pass_fraction']:.2%} | {s['unknown_fraction']:.2%} | {s['flag_fraction']:.2%} |")
    text +=['','The uniform-absorber, optically-invisible-residue and dirty-reference cases may PASS even though the scene construction labels physical residue present. This is a limitation of the sensing model or reference, not a success. A scratch-like response can FLAG a clean but damaged surface.','',
    '## Interpretation and next evidence required','',
    'This prototype checks demodulation, error propagation, feasible-set inference, abstention and synthetic failure cases. It does not establish that actual residues obey the Gaussian model, that the reference is clean, that a room can be covered within 30 minutes, that equipment costs are acceptable, or that the proposed combination is novel. These require human assessment and physical/source evidence.','',
    'The uniform-DC baseline is intentionally weak for this response model because the primary modeled effect changes modulation rather than mean intensity. It is a sanity baseline, not evidence of superiority over all conventional optical inspection.','',
    'No autonomous submission is performed. Human-authored contribution, verified sources and review of the current challenge agreement are required before any proposal.']
    (OUT/'report.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    print('Report -> outputs/report.md; all claims remain synthetic/model-conditional.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['doctor','tests','smoke','benchmark','stress','report','all'])
    args=parser.parse_args(); cfg=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
    if args.stage=='doctor':doctor(cfg)
    elif args.stage=='tests':tests()
    elif args.stage=='smoke':benchmark(cfg,small=True)
    elif args.stage=='benchmark':benchmark(cfg)
    elif args.stage=='stress':benchmark(cfg,stress=True)
    elif args.stage=='report':report(cfg)
    else:
        doctor(cfg);tests();benchmark(cfg,small=True);benchmark(cfg);benchmark(cfg,stress=True);report(cfg)

if __name__=='__main__':main()
