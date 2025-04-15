import sys
sys.path.append('..')
from common import *

rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/fig11/"
kern_sum_dir = root_dir + "size-csv/"
benchname = "uench"


def draw_single():
    file1    = rootpath+"nor-launch-1024-1024-1000-1000-3foo_cuda_kern_exec_trace.csv"
    file2    = rootpath+"cc-launch-1024-1024-1000-1000-3foo_cuda_kern_exec_trace.csv"
    
    df = pd.read_csv(file1)
    intrest_cols = ["API Dur (ns)"]
    df = df[intrest_cols].reset_index()
    df["us"] = df["API Dur (ns)"] / 1000

    df2 = pd.read_csv(file2)
    intrest_cols = ["API Dur (ns)"]
    df2 = df2[intrest_cols].reset_index()
    df2["us"] = df2["API Dur (ns)"] / 1000

    ax = df.plot.scatter(x="index", y="us", alpha=0.7, color='royalblue',s=10, label='Base', figsize=(2.3, 2))
    df2.plot.scatter(x="index", y="us", ax=ax, alpha=0.7, color='teal', s=10, label='CC')
    

    highlight_indices = [0, 100]
    highlight_y1 = df.loc[df["index"].isin(highlight_indices), "us"]
    highlight_y2 = df2.loc[df2["index"].isin(highlight_indices), "us"]

    ax.scatter(highlight_indices, highlight_y1, color='blue', alpha=0.1, s=70)
    ax.scatter(highlight_indices, highlight_y2, color='green', alpha=0.1,s=70)
    xticks = [0, 100, 200, 300, 400, 500]
    xtick_labels = [f"{x}" for x in xticks]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, fontsize=8)
    
    ax.set_yscale('log')
    major_ticks = [1, 10000, 10000000]
    ax.set_yticks(major_ticks)
    ax.yaxis.set_major_locator(ticker.FixedLocator(major_ticks))

    ax.yaxis.set_major_formatter(ticker.LogFormatterSciNotation(base=10.0))

    ax.yaxis.set_minor_locator(ticker.NullLocator())

    ax.tick_params(axis='y', which='major', labelsize=8)
    ax.tick_params(axis='y', which='minor', labelsize=8)

    ax.set_xlabel("Launch index", fontsize=8)
    ax.set_ylabel("Time (us)", fontsize=8)
    ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.3),ncol=2)
    plt.tight_layout()
    # save path 
    output_dir = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    plt.savefig(output_dir +"fig-foo3.pdf", format='pdf', dpi = 900)

if __name__ == "__main__":
    draw_single()