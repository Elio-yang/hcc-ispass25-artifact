#!/usr/bin/python3
import sys
sys.path.append('..')
from common import *

benchname = "sum"

def draw(output_dir):
    plt.rcParams["figure.autolayout"] = True
    file1 = output_dir + benchname+'-base-memcpy_sum.csv'
    file2 = output_dir + benchname+'-cc-memcpy_sum.csv'
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    interest_cols = ["App", "mode", "h2d_time", "d2h_time", "d2d_time", "src_pin_cnt","src_page_cnt","src_dev_cnt","src_man_cnt"]
    df1 = df1[interest_cols]
    df2 = df2[interest_cols]

    # all app name to lower case
    df1["App"] = df1["App"].str.lower()
    df2["App"] = df2["App"].str.lower()

    # time is ns in csv, convert to us
    df1["h2d_time"] = df1["h2d_time"] / 1000
    df1["d2h_time"] = df1["d2h_time"] / 1000
    df1["d2d_time"] = df1["d2d_time"] / 1000
    df1["sum"] = df1["h2d_time"] + df1["d2h_time"] + df1["d2d_time"]


    df2["h2d_time"] = df2["h2d_time"] / 1000
    df2["d2h_time"] = df2["d2h_time"] / 1000
    df2["d2d_time"] = df2["d2d_time"] / 1000
    df2["sum"] = df2["h2d_time"] + df2["d2h_time"] + df2["d2d_time"]

    # normalize the time
    df2["norm_sum"] = df2["sum"] / df1["sum"]
    # calculate geometric mean of the normalized time
    max_value = df2["norm_sum"].max()
    gmean_value = gmean(df2["norm_sum"])
    print("min of normalized time: ", df2["norm_sum"].min())
    print("max of normalized time: ", max_value)
    print("gmean of normalized time: ", gmean_value)
    print(df2[["App","norm_sum"]])

    colors = ['#1b9e77', '#d95f02', '#7570b3']
    colors = ['#f46036', '#2e294e', '#0496ff']

    ax = df1.plot(x="App", y=["h2d_time", "d2h_time", "d2d_time"], 
            kind="bar", 
            stacked=True,
            position=1,
            edgecolor='white',
            width=0.45,
            color=colors,
            alpha=default_alpha-0.2,
            label=['Base H2D', 'Base D2H', 'Base D2D'],
            figsize=(12, 3.5)) 
    
    df2.plot(x="App", 
        y=["h2d_time", "d2h_time", "d2d_time"], 
        kind="bar", 
        stacked=True,
        ax=ax,
        position=0,
        width=0.45,
        hatch='///',
        edgecolor='white',
        # colormap='rainbow',
        color=colors,
        alpha=default_alpha-0.2,
        label=['CC H2D', 'CC D2H', 'CC D2D']) 



    ax.set_xlim(-1,len(df1["App"]))
    ax.set_ylim(1, 1500000)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # ax.set_title("Memcpy Time")
    
    ax.set_yscale('log')
    major_ticks = [1, 1000, 1000000]
    ax.set_yticks(major_ticks)
    # Set major tick labels
    ax.yaxis.set_major_locator(ticker.FixedLocator(major_ticks))
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto', numticks=10))



    ax.tick_params(axis='y', which='major', labelsize=10)
    ax.tick_params(axis='y', which='minor', labelsize=10)



    ax.set_ylabel("Time (us)", fontsize=12)
    ax.set_xlabel("")
    plt.legend(bbox_to_anchor=(0.5, 1.25), loc='upper center', ncol=6, fontsize=12)
    plt.tight_layout()
    output_dir = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    plt.savefig(output_dir +"fig-"+benchname+'-memcpy_sum.pdf', format='pdf')



if __name__ == "__main__":
    draw("/Users/yangyang/Desktop/ispass_25_artifact/fig4/")