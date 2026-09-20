import unittest
import numpy as np
from src.core import demodulate,slope_bounds,infer,PASS,UNKNOWN
from src.simulation import make_scene

class CoreTests(unittest.TestCase):
    def setUp(self):
        import json
        from pathlib import Path
        self.cfg=json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        self.cfg['image_size']=8

    def test_demodulation_exact(self):
        p=np.linspace(-3,3,64).reshape(8,8)
        arr=np.array([0.5+0.23*np.cos(p+k*np.pi/2) for k in range(4)])
        np.testing.assert_allclose(demodulate(arr),0.23,atol=1e-14)

    def test_amplitude_error_bound(self):
        rng=np.random.default_rng(11); eps=0.005
        p=rng.uniform(-np.pi,np.pi,(32,32))
        ideal=np.array([0.5+0.23*np.cos(p+k*np.pi/2) for k in range(4)])
        for _ in range(20):
            noise=rng.uniform(-eps,eps,ideal.shape)
            self.assertLessEqual(float(np.abs(demodulate(ideal+noise)-0.23).max()),np.sqrt(2)*eps+1e-12)

    def test_slope_interval(self):
        x=np.array([0.01,0.05,0.2,0.8]); a=0.17;t=0.63
        z=(a+x*t)[:,None,None]
        lo,hi=slope_bounds(x,z-0.01,z+0.01)
        self.assertTrue((lo<=t).all() and (hi>=t).all())
        lo2,hi2=slope_bounds(x,z,z)
        np.testing.assert_allclose(lo2,t,atol=1e-12)
        np.testing.assert_allclose(hi2,t,atol=1e-12)

    def test_interval_contains_true_proxy(self):
        rng=np.random.default_rng(22)
        for kind in ['clean','subthreshold','boundary','strong','patchy','anisotropic']:
            for _ in range(5):
                r,s,q,vis,_=make_scene(self.cfg,rng,kind)
                z=infer(r,s,self.cfg,vis)
                good=z['valid'][None,:,:]
                self.assertTrue(np.all((q>=z['lower']-1e-10)|~good))
                self.assertTrue(np.all((q<=z['upper']+1e-10)|~good))
                positive=q.max(axis=0)>=self.cfg['proxy_threshold_pixel2']
                self.assertFalse(np.any((z['status']==PASS)&positive))

    def test_hidden_is_unknown(self):
        r,s,q,vis,_=make_scene(self.cfg,np.random.default_rng(3),'occluded')
        z=infer(r,s,self.cfg,vis)
        self.assertTrue((z['status'][~vis]==UNKNOWN).all())

    def test_more_frequencies_cannot_expand_exact_feasible_set(self):
        r,s,q,vis,_=make_scene(self.cfg,np.random.default_rng(4),'clean')
        few=infer(r,s,self.cfg,vis,indices=[0,5]); full=infer(r,s,self.cfg,vis)
        good=few['valid']&full['valid']
        self.assertTrue((full['lower'][:,good]>=few['lower'][:,good]-1e-10).all())
        self.assertTrue((full['upper'][:,good]<=few['upper'][:,good]+1e-10).all())

    def test_gaussian_kernel_frequency_response(self):
        # Independent numerical spatial-kernel check of the chosen approximation.
        n=256; f=32/n; sigma=1.1
        k=np.arange(-8,9); kernel=np.exp(-0.5*(k/sigma)**2);kernel/=kernel.sum()
        empirical=np.sum(kernel*np.cos(2*np.pi*f*k))
        theoretical=np.exp(-2*np.pi**2*sigma**2*f*f)
        self.assertLess(abs(empirical-theoretical),5e-4)

    def test_no_nan(self):
        for kind in ['low_signal','clipped','phase_motion']:
            r,s,q,vis,_=make_scene(self.cfg,np.random.default_rng(7),kind)
            z=infer(r,s,self.cfg,vis)
            self.assertTrue(np.isfinite(z['lower']).all())
            self.assertTrue(np.isfinite(z['upper']).all())

if __name__=='__main__': unittest.main()
