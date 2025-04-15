#!/usr/bin/python3
import sys
sys.path.append('..')
from common import *



benchname = "sum"

def draw(csv_path):
    plt.rcParams["figure.autolayout"] = True

    file1 = csv_path + benchname+'-base-queue_sum.csv'
    file2 = csv_path + benchname+'-cc-queue_sum.csv'
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    interest_cols = ["App", "mode","launch_queue_dur", "kern_launch_dur", "queue_dur", "average_launch_dur","average_queue_dur"]
    df1 = df1[interest_cols].reset_index(drop=True)
    df2 = df2[interest_cols].reset_index(drop=True)

    df1 = df1[1:]
    df2 = df2[1:]

    df1["App"] = df1["App"].str.lower()
    df2["App"] = df2["App"].str.lower()

    for df in [df1, df2]:
        df["launch_queue_dur"]= df["launch_queue_dur"] / 1000
        df["kern_launch_dur"]= df["kern_launch_dur"] / 1000
        df["queue_dur"]= df["queue_dur"] / 1000
        df["average_launch_dur"]= df["average_launch_dur"] / 1000
        df["average_queue_dur"]= df["average_queue_dur"] / 1000
    

    df2["norm_launch_queue_dur"] = df2["launch_queue_dur"] / df1["launch_queue_dur"]
    df1["norm_launch_queue_dur"] = df1["launch_queue_dur"] / df1["launch_queue_dur"]
    max_launch_queue_dur_norm = df2["norm_launch_queue_dur"].max()
    min_launch_queue_dur_norm = df2["norm_launch_queue_dur"].min()
    gmean1 = gmean(df2["norm_launch_queue_dur"])

    df2["norm_kern_launch_dur"] = df2["kern_launch_dur"] / df1["kern_launch_dur"]
    df1["norm_kern_launch_dur"] = df1["kern_launch_dur"] / df1["kern_launch_dur"]
    max_kern_launch_dur_norm = df2["norm_kern_launch_dur"].max()
    min_kern_launch_dur_norm = df2["norm_kern_launch_dur"].min()
    gmean2 = gmean(df2["norm_kern_launch_dur"])

    df2["norm_queue_dur"] = df2["queue_dur"] / df1["queue_dur"]
    df1["norm_queue_dur"] = df1["queue_dur"] / df1["queue_dur"]

    max_queue_dur_norm = df2["norm_queue_dur"].max()
    min_queue_dur_norm = df2["norm_queue_dur"].min()
    gmean3 = gmean(df2["norm_queue_dur"])

    print("max of normalized launch_queue_dur increase: ", max_launch_queue_dur_norm)
    print("min of normalized launch_queue_dur increase: ", min_launch_queue_dur_norm)
    print("gmean of normalized launch_queue_dur increase: ", gmean1)

    print("max of normalized kern_launch_dur increase: ", max_kern_launch_dur_norm)
    print("min of normalized kern_launch_dur increase: ", min_kern_launch_dur_norm)
    print("gmean of normalized kern_launch_dur increase: ", gmean2)

    print("max of normalized kern_queue_dur increase: ", max_queue_dur_norm)
    print("min of normalized kern_queue_dur increase: ", min_queue_dur_norm)
    print("gmean of normalized kern_queue_dur increase: ", gmean3)


    print(df2[["App","norm_queue_dur","norm_kern_launch_dur","norm_launch_queue_dur"]])


    colors = ['#f46036', '#064789', '#9381ff']

    fig, axes = plt.subplots(3, 1, figsize=(8.5, 5.5), sharex=True)

    df1.plot(
        x="App", y="norm_kern_launch_dur", kind="bar",
        ax=axes[0], position=1, width=0.4, edgecolor='white',
        color=colors[0], alpha=default_alpha-0.2, label='Base KLO'
    )
    df2.plot(
        x="App", y="norm_kern_launch_dur", kind="bar",
        ax=axes[0], position=0, width=0.4, hatch='///',
        edgecolor='white', color=colors[0], alpha=default_alpha-0.2, label='CC KLO'
    )
    axes[0].legend(loc="upper right",bbox_to_anchor=(0.8,1))

    df1.plot(
        x="App", y="norm_launch_queue_dur", kind="bar",
        ax=axes[1], position=1, width=0.4, edgecolor='white',
        color=colors[1], alpha=default_alpha-0.2, label='Base LQT'
    )
    df2.plot(
        x="App", y="norm_launch_queue_dur", kind="bar",
        ax=axes[1], position=0, width=0.4, hatch='///',
        edgecolor='white', color=colors[1], alpha=default_alpha-0.2, label='CC LQT'
    )
    axes[1].legend(loc="upper right",bbox_to_anchor=(0.8,1))

    df1.plot(
        x="App", y="norm_queue_dur", kind="bar",
        ax=axes[2], position=1, width=0.4, edgecolor='white',
        color=colors[2], alpha=default_alpha-0.2, label='Base KQT'
    )
    df2.plot(
        x="App", y="norm_queue_dur", kind="bar",
        ax=axes[2], position=0, width=0.4, hatch='///',
        edgecolor='white', color=colors[2], alpha=default_alpha-0.2, label='CC KQT'
    )

    for ax in axes:
        ax.set_xlim(-0.5,len(df1["App"])-0.4)
    axes[2].legend(loc="upper right",bbox_to_anchor=(0.8,1))
    axes[0].set_ylim(0,6)
    axes[1].set_ylim(0,4)
    axes[2].set_ylim(0,20)

    plt.xlabel("")
    
    labels = ['(a)', '(b)', '(c)']
    for i, a in enumerate(axes):
        a.text(
            0.07, 0.9,
            labels[i],  
            transform=a.transAxes, 
            color = 'black',
            fontsize=12,  # Font size
            fontweight='bold',  # Bold font
            ha='right',  
            va='top'    
    )
    plt.tight_layout()
    csv_path = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    plt.savefig(csv_path +"fig-"+benchname+'-queue_brk.pdf', format='pdf')

if __name__ == "__main__":

    draw("/Users/yangyang/Desktop/ispass_25_artifact/fig6/")