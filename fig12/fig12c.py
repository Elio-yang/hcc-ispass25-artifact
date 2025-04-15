
#!/usr/bin/python3
import sys
# add .. in the path
sys.path.append("..")
from common import *

def reset_with_original_index(df):
    df = df.reset_index().rename(columns={'index': 'original_index'})
    df.reset_index(drop=False, inplace=True)
    return df

def draw():
    file = "/Users/yangyang/Desktop/ispass_25_artifact/fig11/results.csv"
    df = pd.read_csv(file)
    df_base = df[df["mode"] == "base"].reset_index(drop=True)
    df_cc = df[df["mode"] == "cc"].reset_index(drop=True)
    # print(df_base)
    # print(df_cc)


    df_base["nor_seq_time"] = df_base["seq"] / df_base["seq"]
    df_base["nor_pipe_time"] = df_base["pipe"] / df_base["seq"]
    df_cc["nor_seq_time"] = df_cc["seq"] / df_base["seq"]
    df_cc["nor_pipe_time"] = df_cc["pipe"] / df_base["seq"]

    sizes = df_base["size"].unique()
    times = df_base["time"].unique()
    streams = df_base["stream"].unique()

    df_base_512_1 = reset_with_original_index(df_base[(df_base["size"] == 512) & (df_base["time"] == 1)])
    df_base_512_100 = reset_with_original_index(df_base[(df_base["size"] == 512) & (df_base["time"] == 100)])
    df_cc_512_1 = reset_with_original_index(df_cc[(df_cc["size"] == 512) & (df_cc["time"] == 1)])
    df_cc_512_100 = reset_with_original_index(df_cc[(df_cc["size"] == 512) & (df_cc["time"] == 100)])

    df_base_1024_1 = reset_with_original_index(df_base[(df_base["size"] == 1024) & (df_base["time"] == 1)])
    df_base_1024_100 = reset_with_original_index(df_base[(df_base["size"] == 1024) & (df_base["time"] == 100)])
    df_cc_1024_1 = reset_with_original_index(df_cc[(df_cc["size"] == 1024) & (df_cc["time"] == 1)])
    df_cc_1024_100 = reset_with_original_index(df_cc[(df_cc["size"] == 1024) & (df_cc["time"] == 100)])


    datats = [(df_base_512_1, df_cc_512_1), (df_base_512_100, df_cc_512_100), (df_base_1024_1, df_cc_1024_1), (df_base_1024_100, df_cc_1024_100)]

    fig, ax = plt.subplots(2, 2, figsize=(4, 4))
    ax = ax.flatten()

   
    n = 2
    min_val = 0.3
    max_val = 0.9
    cmap = plt.get_cmap("RdPu")
    colors = [cmap(i) for i in np.linspace(min_val, max_val, n)]
    width = 0.4
    
    for i, (df_base, df_cc) in enumerate(datats):
        df_base.plot.scatter(
            x="index", 
            y="nor_pipe_time", 
            ax=ax[i], 
            color='royalblue',
            alpha = default_alpha, 
            s=25,
            label="Base")
        df_cc.plot.scatter(
            x="index", 
            y="nor_pipe_time", 
            ax=ax[i], 
            color='teal', 
            alpha = default_alpha,
            s=25,
            label="CC"
        )
        
        if i==0 or i == 2:
            ax[i].set_ylabel("Norm. Perf.", fontsize=12)
            if i == 2:
                ax[i].set_xlabel("Streams (2^i)", fontsize=12)
            else:
                ax[i].set_xlabel("")
        else:
            ax[i].set_ylabel("")
            # no x label
            ax[i].set_xlabel("")
        
        ax[i].set_xticks(range(0, len(streams))) 
        ax[i].set_xticklabels([0,1,2,3,4,5,6])
        ax[i].set_title(f"{df_base['size'].values[0]}MB | {df_base['time'].values[0]}ms", fontsize=12)


        ax[i].legend().remove()
        
        if i== 1 or i == 3:
            ticks = [1, 4, 6]
            ax[i].yaxis.tick_right()
            ax[i].yaxis.set_label_position("right")
        else:
            # 0, 5, 10, 15 y ticks
            ticks = [1, 10, 15]
        ax[i].set_yticks(ticks)
        # font size of ticks
        ax[i].tick_params(axis='both', which='major', labelsize=12)

        # draw y=1 line
        ax[i].axhline(y=1, color='grey', linestyle='--', linewidth=0.7)
    #wspace
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.tight_layout()
    outpath = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    plt.savefig(outpath + "fig-overlap.pdf", format='pdf', dpi=900)

if __name__ == "__main__":
    draw()