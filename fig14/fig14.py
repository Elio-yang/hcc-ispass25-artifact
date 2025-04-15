import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.colors import LogNorm

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 5
 
file_path = "./medians_per_run.tsv"
df = pd.read_csv(file_path, sep='\t')
 
metric = 'thruput'
 
baseline_condition = (df['Model'] == 'nonquant') & (df['CC_mode'] == 'off') & (df['Backend'] == 'hf')
baseline_df = df[baseline_condition]
baseline_pivot = baseline_df.pivot_table(
    index='batch_size',
    columns='input_length',
    values=metric,
    aggfunc='median'
)
 
models = df['Model'].unique()
cc_modes = df['CC_mode'].unique()
 
global_min = np.inf
global_max = -np.inf
 
for model in models:
    for cc_mode in cc_modes:
        subset = df[(df['Model'] == model) &
                    (df['CC_mode'] == cc_mode) &
                    (df['Backend'] == 'vllm')]
        if not subset.empty:
            pivot = subset.pivot_table(
                index='batch_size',
                columns='input_length',
                values=metric
            )
            local_min = pivot.min().min()
            local_max = pivot.max().max()
            global_min = min(global_min, local_min)
            global_max = max(global_max, local_max)
 
print(f"Global min: {global_min}, Global max: {global_max}")


n_subplots = 0
for model in models:
    for cc_mode in cc_modes:
        subset = df[(df['Model'] == model) &
                    (df['CC_mode'] == cc_mode) &
                    (df['Backend'] == 'vllm')]
        if not subset.empty:
            n_subplots += 1
 
n_cols = int(np.ceil(np.sqrt(n_subplots)))
n_rows = int(np.ceil(n_subplots / n_cols))
fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 3, n_rows * 3), sharex=False, sharey=False)
axes = axes.flatten()
subplot_idx = 0
 
for model in models:
    for cc_mode in cc_modes:
        subset = df[(df['Model'] == model) &
                    (df['CC_mode'] == cc_mode) &
                    (df['Backend'] == 'vllm')]
        if not subset.empty:
            pivot = subset.pivot_table(
                index='batch_size',
                columns='input_length',
                values=metric
            )
            ax = axes[subplot_idx]
            im = ax.imshow(pivot.to_numpy(), aspect='auto', cmap=plt.cm.Blues, norm=LogNorm(vmin=global_min, vmax=global_max))
            data_array = pivot.to_numpy()
            for i in range(data_array.shape[0]):
                for j in range(data_array.shape[1]):
                    value = data_array[i, j]
                    rgba = im.cmap(im.norm(value))
                    brightness = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
                    text_color = 'white' if brightness < 0.5 else 'black'
                    ax.text(j, i, f'{value:.1f}', ha='center', va='center', color=text_color, fontsize=11)
            if model == "nonquant":
                    ax.set_title(f"BF16 | CC-{cc_mode} | vllm", fontsize=12)
            else:
                    ax.set_title(f" AWQ | CC-{cc_mode} | vllm", fontsize=12)
            ax.set_xticks(range(pivot.shape[1]))
            ax.set_xticklabels(pivot.columns, fontsize=11, ha='right')
            ax.set_yticks(range(pivot.shape[0]))
            ax.set_yticklabels(pivot.index, fontsize=11)
            subplot_idx += 1
 
for i in range(subplot_idx, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout(rect=[0, 0, 1, 0.95])

filename = f"/Users/yangyang/Desktop/ispass_25_artifact/figure/fig-vllm_heatmap_{metric}.pdf"
plt.savefig(filename, format='pdf', dpi=900)
plt.close()