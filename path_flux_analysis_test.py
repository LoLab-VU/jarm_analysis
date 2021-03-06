from tropical.discretize_path import DomPath
from tropical.examples.jnk3.jnk3_no_ask1 import model
import numpy as np
from pysb.simulator import ScipyOdeSimulator

param_values = np.array([p.value for p in model.parameters])
idx_pars_calibrate = [1, 5, 9, 11, 15, 17, 19, 23, 25, 27, 31, 35, 36, 37, 38, 39, 41, 43] #pydream3
rates_of_interest_mask = [i in idx_pars_calibrate for i, par in enumerate(model.parameters)]
pars = np.load('most_likely_par_100000.npy')
param_values[rates_of_interest_mask] = 10 ** pars
param_values[44] = 200
# param_values[44] = param_values[44] * 0.5
tspan = np.linspace(0, 60, 100)

# viz = ModelVisualization(model)
# data = viz.static_view(get_passengers=False)
sim = ScipyOdeSimulator(model, tspan, param_values=[param_values]).run()
# d = run_dompath_multi(model, sim, target='s27', depth=4, cpu_cores=2)
d = DomPath(model, sim, dom_om=0.5, target='s27', depth=5)
q, paths = d.get_path_signatures(cpu_cores=2)
