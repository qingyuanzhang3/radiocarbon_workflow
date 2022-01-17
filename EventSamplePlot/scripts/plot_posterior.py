import matplotlib.pyplot as plt
import numpy as np
from ticktack import fitting

chains = []
for i in range(len(snakemake.input)):
    chain = np.load(snakemake.input[i])
    chains.append(chain)
if chains[-1].shape[1] == 4:
    labels = ["start date (yr)", "duration (yr)", "phi (yr)", "spike production (cm$^2$ yr/s)"]
else:
    labels = ["start date (yr)", "duration (yr)", "phi (yr)", "spike production (cm$^2$ yr/s)", "solar amplitude (cm$^2$/s)"]
cf = fitting.CarbonFitter()
fig = cf.plot_multiple_chains(chains, chain.shape[1] * 2,
                        params_names=labels,
                        labels = snakemake.params.cbm_model
                        )
plt.suptitle(snakemake.params.event, fontsize=25)
fig.savefig(snakemake.output[0])