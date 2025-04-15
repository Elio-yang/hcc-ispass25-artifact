#!/usr/bin/python3
import sys
sys.path.append('..')
from common import *


def draw(csv_dir):
    plt.rcParams["figure.autolayout"] = True
    file1 = csv_dir + 'base-alloc.csv'
    file2 = csv_dir + 'cc-alloc.csv'
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    interest_cols = ['App', 'mode', "hmalloc", "gmalloc","free", "all"]
    int_cols = ['App',"all"]
    df1 = df1[interest_cols]
    df2 = df2[interest_cols]
    dfs1 = df1[int_cols]
    dfs2 = df2[int_cols]



    dfs2["sd"] = dfs2["all"] / dfs1["all"]
    gmean_sd = gmean(dfs2["sd"])
    print("gmean_sd: ", gmean_sd)

    dfs1h = df1[df1["hmalloc"] != 0].copy()
    dfs2h = df2[df2["hmalloc"] != 0].copy()

    dfs2h["host"] = dfs2h["hmalloc"] / dfs1h["hmalloc"]
    gmean_host = gmean(dfs2h["host"])
    print("gmean_host: ", gmean_host)

    dfs2h["dev"] = dfs2h["gmalloc"] / dfs1h["gmalloc"]
    gmean_dev = gmean(dfs2h["dev"])
    print("gmean_dev: ", gmean_dev)

    dfs2h["free"] = dfs2h["free"] / dfs1h["free"]
    gmean_free = gmean(dfs2h["free"])
    print("gmean_free: ", gmean_free)





    df1["App"] = df1["App"].str.lower()
    df2["App"] = df2["App"].str.lower()
    

    for dfs in [df1, df2]:
        for col in ["hmalloc", "gmalloc","free", "all"]:
            dfs[col] = dfs[col] / 1000
    colors = ['#f46036', '#2e294e', '#0496ff']

    ax = df1.plot(x="App", y=["hmalloc", "gmalloc","free"], 
            kind="bar", 
            stacked=True,
            position=1,
            edgecolor='white',
            width=0.45,
            color=colors,
            alpha=default_alpha-0.2,
            label=['Base Hmalloc', 'Base Dmalloc', 'Base Free'],
            figsize=(12, 3.5)) 
    
    df2.plot(x="App", 
        y=["hmalloc", "gmalloc","free"], 
        kind="bar", 
        stacked=True,
        ax=ax,
        position=0,
        width=0.45,
        hatch='///',
        edgecolor='white',
        color=colors,
        alpha=default_alpha-0.2,
        label=['CC Hmalloc', 'CC Dmalloc', 'CC Free']) 



    ax.set_xlim(-1,len(df1["App"]))
    # set ylim
    ax.set_ylim(100, 10000000)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    ax.set_yscale('log')
    major_ticks = [100, 1000, 10000, 100000,1000000, 10000000]
    ax.set_yticks(major_ticks)
    ax.yaxis.set_major_locator(ticker.FixedLocator(major_ticks))
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto', numticks=10))

    ax.tick_params(axis='y', which='major', labelsize=12)
    ax.tick_params(axis='y', which='minor', labelsize=12)

    ax.set_ylabel("Time (us)", fontsize=12)
    ax.set_xlabel("")

    plt.legend(bbox_to_anchor=(0.5, 1.3), loc='upper center', ncol=6, fontsize=12)

    plt.tight_layout()
    csv_dir = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    plt.savefig(csv_dir +"fig-alloc.pdf", format='pdf')

    pass


if __name__ == "__main__":
    draw("/Users/yangyang/Desktop/ispass_25_artifact/fig5/")