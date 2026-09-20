"""Synthetic generator. Parameters are assumptions, not published LOD values."""
from __future__ import annotations
import numpy as np

CONDITIONS=['clean','subthreshold','boundary','strong','patchy','anisotropic']
STRESSES=['low_signal','occluded','clipped','noise_bound_violated',
          'defocus_bound_violated','dirty_reference','uniform_absorber',
          'optically_invisible_residue','scratch_like_response','phase_motion',
          'frequency_dependent_gain','negative_blur_cancellation']

def make_scene(cfg:dict,rng:np.random.Generator,kind:str):
    h=w=cfg['image_size']; shape=(h,w)
    q=np.zeros((2,h,w))
    th=cfg['proxy_threshold_pixel2']
    if kind=='subthreshold': q[:]=0.2
    elif kind=='boundary': q[:]=th
    elif kind=='strong': q[:]=1.2
    elif kind=='patchy':
        q[:,h//4:3*h//4,w//4:3*w//4]=1.2
    elif kind=='anisotropic': q[0]=1.2
    elif kind in ('dirty_reference','scratch_like_response'): q[:]=1.2
    elif kind=='negative_blur_cancellation': q[:]=0.6
    elif kind not in CONDITIONS+STRESSES: raise ValueError('Unknown condition: '+kind)
    bmax=cfg['clean_variation_bound_pixel2']
    # Shared per-scene variations: pixels must NOT be treated as independent trials.
    b=rng.uniform(-bmax,bmax,size=(2,1,1))*np.ones((2,h,w))
    if kind=='defocus_bound_violated': b[:]=0.8
    if kind=='negative_blur_cancellation': b[:]=-0.6
    qref=np.zeros_like(q)
    if kind=='dirty_reference': qref=q.copy(); b[:]=0
    v=cfg['reference_blur_variance_pixel2']
    gr=float(rng.uniform(0.85,1.15)); gs=float(rng.uniform(0.85,1.15))
    if kind=='uniform_absorber': gs*=0.65
    if kind=='low_signal': gs=0.01
    f=np.asarray(cfg['frequencies_cycles_per_screen'],float)/cfg['screen_coordinate_width']
    xx,yy=np.meshgrid(np.linspace(0,cfg['screen_coordinate_width'],w,endpoint=False),
                      np.linspace(0,cfg['screen_coordinate_width'],h,endpoint=False))
    ref=np.empty((2,len(f),4,h,w)); sam=np.empty_like(ref)
    noise=cfg['additive_noise_bound']
    noise_actual=0.03 if kind=='noise_bound_violated' else noise
    levels=cfg['quantization_levels']
    offset=0.9 if kind=='clipped' else 0.5
    phase0=rng.uniform(-np.pi,np.pi,size=shape)
    for o,coord in enumerate((xx,yy)):
        for j,fj in enumerate(f):
            coef=2*np.pi**2*fj*fj
            mr=0.30*gr*np.exp(-coef*(v+qref[o]))
            ms=0.30*gs*np.exp(-coef*(v+b[o]+q[o]))
            if kind=='frequency_dependent_gain': ms*=np.exp(-coef*0.8)
            for k in range(4):
                phase=2*np.pi*fj*coord+phase0+k*np.pi/2
                ir=0.5+mr*np.cos(phase)
                motion=0.35*k if kind=='phase_motion' else 0.0
                it=offset+ms*np.cos(phase+motion)
                ir +=rng.uniform(-noise,noise,size=shape)
                it +=rng.uniform(-noise_actual,noise_actual,size=shape)
                ref[o,j,k]=np.round(np.clip(ir,0,1)*(levels-1))/(levels-1)
                sam[o,j,k]=np.round(np.clip(it,0,1)*(levels-1))/(levels-1)
    visible=np.ones(shape,dtype=bool)
    if kind=='occluded': visible[:,:w//2]=False
    contaminated_by_construction=kind in ('uniform_absorber','optically_invisible_residue','dirty_reference')
    meta=dict(kind=kind,evidence_type='SYNTHETIC',
              physical_label_simulated_only=contaminated_by_construction,
              proxy_definition='max directional excess blur variance >= threshold',
              material_identity='NONE; abstract response model',
              model_assumptions_expected_to_hold=kind in CONDITIONS+['low_signal','occluded'])
    return ref,sam,q,visible,meta
