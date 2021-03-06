import numpy as np
import os
import ticktack
from ticktack import fitting
import pandas as pd

file_names = [f for f in os.listdir(snakemake.input[0]) if os.path.isfile(os.path.join(snakemake.input[0], f))]
start, end = np.inf, -np.inf
cbm = ticktack.load_presaved_model('Guttler15', production_rate_units = 'atoms/cm^2/s')
sf = fitting.SingleFitter(cbm, cbm_model='Guttler15')
for file in file_names:
    sf.load_data(snakemake.input[0] + "/" + file)
    if sf.start < start:
        start = sf.start
    if sf.end > end:
        end = sf.end


offset = 0
time_sampling = np.arange(start, end+1)
counter = np.zeros(time_sampling.size)
dc14_data = np.zeros(time_sampling.size)
dc14_data_error = np.zeros(time_sampling.size)
for file in file_names:
    offset += sf.offset
    sf.load_data(snakemake.input[0] + "/" + file)
    idx = np.in1d(time_sampling, sf.time_data)
    dc14_data[idx] += sf.d14c_data - sf.offset
    dc14_data_error[idx] += sf.d14c_data_error**2
    counter[idx] += 1

offset = offset / len(file_names)
nonzero_entries = counter > 0

arr = np.zeros((counter.size, 3))[nonzero_entries]
arr[:, 0] = time_sampling[nonzero_entries]
arr[:, 1] = (dc14_data[nonzero_entries] / counter[nonzero_entries]) + offset
arr[:, 2] = (np.sqrt(dc14_data_error[nonzero_entries]) / counter[nonzero_entries])
df = pd.DataFrame(arr, columns=['year', 'd14c', 'sig_d14c'])
df.to_csv(snakemake.output[0], index=False)
