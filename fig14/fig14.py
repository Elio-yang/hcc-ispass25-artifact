import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.colors import LogNorm

# Set some matplotlib font properties
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 5
 
# Read the TSV data file
file_path = "./medians_per_run.tsv"
df = pd.read_csv(file_path, sep='\t')
 
# Define the metric to plot
metric = 'real'
 
# (Optional) Compute the baseline pivot table for reference,
# although it is not used for independent color scaling.
baseline_condition = (df['Model'] == 'nonquant') & (df['CC_mode'] == 'off') & (df['Backend'] == 'hf')
baseline_df = df[baseline_condition]
baseline_pivot = baseline_df.pivot_table(
    index='batch_size',
    columns='input_length',
    values=metric,
    aggfunc='median'
)
 
# We'll only consider subplots for combinations of Model and CC_mode for backend 'vllm'
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


# Count how many subplots are needed
n_subplots = 0
for model in models:
    for cc_mode in cc_modes:
        subset = df[(df['Model'] == model) &
                    (df['CC_mode'] == cc_mode) &
                    (df['Backend'] == 'vllm')]
        if not subset.empty:
            n_subplots += 1
 
# Arrange subplots in a grid (do not share x or y axes so each can be independently scaled)
n_cols = int(np.ceil(np.sqrt(n_subplots)))
n_rows = int(np.ceil(n_subplots / n_cols))
fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 3, n_rows * 3), sharex=False, sharey=False)
axes = axes.flatten()
subplot_idx = 0
 

pivot_dic = {}

# Loop over unique Model and CC_mode (for backend 'vllm') and plot each pivot table independently
for model in models:
    for cc_mode in cc_modes:
        subset = df[(df['Model'] == model) &
                    (df['CC_mode'] == cc_mode) &
                    (df['Backend'] == 'vllm')]
        if not subset.empty:
            # Create a pivot table with Batch Size as rows and Input Length as columns
            old_pivot = subset.pivot_table(
                index='batch_size',
                columns='input_length',
                values=metric
            )
            print(cc_mode)
            print(model)
            key=cc_mode+"-"+model
            print(key)
            pivot = (old_pivot)/baseline_pivot
            print(pivot)

            pivot_dic[key]=pivot
            
            ax = axes[subplot_idx]
            # Use imshow with the lighter colormap "YlGnBu".
            # No vmin/vmax is set, so each subplot normalizes its own data#
            im = ax.imshow(pivot.to_numpy(), aspect='auto', cmap=plt.cm.Blues)
            data_array = pivot.to_numpy()
            # Add annotations for each cell
            for i in range(data_array.shape[0]):
                for j in range(data_array.shape[1]):
                    value = data_array[i, j]
                    # Get RGBA color from the colormap corresponding to this value
                    rgba = im.cmap(im.norm(value))
                    # Compute perceived brightness: standard formula (values are 0-1)
                    brightness = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
                    # Choose white text if the background is dark, black if light
                    text_color = 'white' if brightness < 0.5 else 'black'
                    ax.text(j, i, f'{value:.1f}', ha='center', va='center', color=text_color, fontsize=11)
            # Title reflecting current conditions
            if model == "nonquant":
                    ax.set_title(f"BF16 | CC-{cc_mode} | vllm", fontsize=12)
            else:
                    ax.set_title(f" AWQ | CC-{cc_mode} | vllm", fontsize=12)
            # Set tick positions and labels based on pivot table index and columns
            ax.set_xticks(range(pivot.shape[1]))
            if subplot_idx == 2 or subplot_idx == 3:
                ax.set_xlabel("Sequence Length", fontsize=11)
            if subplot_idx == 0 or subplot_idx == 2:
                ax.set_ylabel("Batch Size", fontsize=11)
            ax.set_xticklabels(pivot.columns, fontsize=11, ha='right')
            ax.set_yticks(range(pivot.shape[0]))
            ax.set_yticklabels(pivot.index, fontsize=11)
            # Optionally add an individual colorbar for this subplot
            # cbar = fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.05, pad=0.05)
            # cbar.ax.tick_params(labelsize=6)
            subplot_idx += 1
 
# Remove any extra axes if the grid has more slots than needed
for i in range(subplot_idx, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout(rect=[0, 0, 1, 0.95])
 
# Create a directory for the metric if it does not exist, then save the figure
if not os.path.exists(metric):
    os.makedirs(metric)

filename = f"/Users/yangyang/Desktop/ispass_25_artifact/figure/fig-vllm_heatmap_{metric}.pdf"
plt.savefig(filename, format='pdf', dpi=900)
plt.close()