import pickle
import sys

import numpy as np

baseline_results_pkl = sys.argv[1]
with open(baseline_results_pkl, 'rb') as f:
    baseline_results = pickle.load(f)

firing_rates = baseline_results['firing_rates'][:]

firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))

with open('results/base_mean_sd.txt', 'w') as f:
    f.write(str(firing_rate_mean) + '\n')
    f.write(str(firing_rate_std) + '\n')
