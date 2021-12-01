from fitter import Fitter
from scipy import stats
import scipy.stats
import numpy as np


size = 30000
dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']
y = scipy.int_(np.round_(scipy.stats.vonmises.rvs(5,size=size)*47))

for dist_name in dist_names:
    dist = getattr(scipy.stats, dist_name)
    print(dist)
    params = dist.fit(y)
    print(params.mode())
