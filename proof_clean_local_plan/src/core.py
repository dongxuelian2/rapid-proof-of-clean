"""Bounded-error optical-response intervals; NOT a physical hygiene detector.

q is extra Gaussian PSF variance in screen-coordinate pixels squared.
Every interval is conditional on the specified model and error bounds.
"""
from __future__ import annotations
import numpy as np

UNKNOWN, PASS, FLAG = 0, 1, 2

def demodulate(frames: np.ndarray) -> np.ndarray:
    """Input (...,4,H,W), output (...,H,W)."""
    if frames.ndim < 3 or frames.shape[-3] != 4:
        raise ValueError('Expected phase axis of size four at axis -3')
    return 0.5*np.hypot(frames[...,0,:,:]-frames[...,2,:,:],
                         frames[...,3,:,:]-frames[...,1,:,:])

def slope_bounds(x: np.ndarray, low: np.ndarray, high: np.ndarray):
    """Find all t for which some a obeys low_j <= a+x_j*t <= high_j.
    Frequency is axis zero. Pairwise interval intersection is exact here.
    """
    x=np.asarray(x,dtype=float)
    if low.shape != high.shape or low.shape[0] != len(x) or len(x)<2:
        raise ValueError('At least two frequencies and matching interval arrays are required')
    if not np.all(np.diff(x)>0):
        raise ValueError('x must be strictly increasing')
    lo=np.full(low.shape[1:],-np.inf)
    hi=np.full(low.shape[1:],np.inf)
    for j in range(len(x)):
        for k in range(j):
            dx=x[j]-x[k]
            lo=np.maximum(lo,(low[j]-high[k])/dx)
            hi=np.minimum(hi,(high[j]-low[k])/dx)
    return lo,hi

def infer(reference: np.ndarray, sample: np.ndarray, cfg: dict,
          visible: np.ndarray | None = None, indices=None) -> dict:
    """Frames have shape (2,F,4,H,W); orientations are treated separately.
    PASS: all feasible in-scope q values are below the proxy threshold.
    FLAG: some orientation has q lower bound above/equal the threshold.
    UNKNOWN: ambiguous, unobservable, saturated or outside the model.
    """
    if reference.shape!=sample.shape or reference.ndim!=5 or reference.shape[0]!=2:
        raise ValueError('reference/sample must both have shape (2,F,4,H,W)')
    if not np.isfinite(reference).all() or not np.isfinite(sample).all():
        raise ValueError('Non-finite input frames')
    f=np.array(cfg['frequencies_cycles_per_screen'],dtype=float)
    if indices is None: indices=list(range(len(f)))
    if len(indices)<2: raise ValueError('At least two frequencies required')
    ref=reference[:,indices]; sam=sample[:,indices]
    f=f[indices]/cfg['screen_coordinate_width']
    x=2*np.pi**2*f*f
    mref=demodulate(ref); msam=demodulate(sam)
    eps=cfg['additive_noise_bound']+0.5/(cfg['quantization_levels']-1)
    delta=np.sqrt(2)*eps
    tiny=np.finfo(float).tiny
    good=((mref>3*delta)&(msam>3*delta)).all(axis=(0,1))
    good &= ((ref>0)&(ref<1)&(sam>0)&(sam<1)).all(axis=(0,1,2))
    for fr in (ref,sam):
        closure=np.abs(fr[:,:,0]+fr[:,:,2]-fr[:,:,1]-fr[:,:,3])
        good &= (closure<=4*eps+1e-12).all(axis=(0,1))
    if visible is not None:
        if visible.shape!=good.shape: raise ValueError('Wrong visible mask shape')
        good &= visible.astype(bool)
    zlow=np.log(np.maximum(mref-delta,tiny)/np.maximum(msam+delta,tiny))
    zhigh=np.log(np.maximum(mref+delta,tiny)/np.maximum(msam-delta,tiny))
    b=cfg['clean_variation_bound_pixel2']
    qlo=[]; qhi=[]; estimate=[]
    xc=x-x.mean()
    for o in range(2):
        tl,th=slope_bounds(x,zlow[o],zhigh[o])
        qlo.append(np.maximum(0,tl-b)); qhi.append(th+b)
        good &= (tl<=th+1e-12)&(th+b>=0)
        z=np.log(np.maximum(mref[o],tiny)/np.maximum(msam[o],tiny))
        estimate.append(np.einsum('f,fhw->hw',xc,z)/np.sum(xc*xc))
    qlo=np.array(qlo); qhi=np.array(qhi); estimate=np.array(estimate)
    good &= (qlo<=qhi+1e-12).all(axis=0)
    th=cfg['proxy_threshold_pixel2']
    status=np.full(good.shape,UNKNOWN,dtype=np.uint8)
    status[good & (qhi<th).all(axis=0)]=PASS
    status[good & (qlo>=th).any(axis=0)]=FLAG
    return dict(status=status,lower=qlo,upper=qhi,valid=good,
                ols=np.maximum(0,estimate).max(axis=0),mref=mref,msam=msam)
