#!/usr/bin/python3
import sys
sys.path.append('..')
from common import *


rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/fig4/"
kern_sum_dir = rootpath + "uvmbench-nsys_results/example_csv/"
benchname = "sum"

#nograph
def draw_ng():
    plt.rcParams["figure.autolayout"] = True
    file = "/Users/yangyang/Desktop/ispass_25_artifact/fig9/" + benchname+'-kern_sum_nog.csv'
    df = pd.read_csv(file)
    interested_cols = ['App','nor-nor', 'cc-nor', 'nor-uvm', 'cc-uvm']
    df = df[interested_cols]
    df['nor-nor'] = df['nor-nor'] / 1_000
    df['cc-nor'] = df['cc-nor'] / 1_000
    df['nor-uvm'] = df['nor-uvm'] / 1_000
    df['cc-uvm'] = df['cc-uvm'] / 1_000
    df['App'] = df['App'].str.lower()

    df['normal'] = df['cc-nor'] / df['nor-nor']
    gmean_value = gmean(df["normal"])
    print("gmean: ", gmean_value)


    df["nor2"] = df["nor-uvm"] / df["nor-nor"]
    df["nor3"] = df["cc-uvm"] / df["nor-nor"]

    non_zero_nor2 = df[df["nor2"] != 0]
    gmean2 = gmean(non_zero_nor2["nor2"])
    non_zero_nor3 = df[df["nor3"] != 0]
    max3 = non_zero_nor3["nor3"].max()
    min3 = non_zero_nor3["nor3"].min()
    print(non_zero_nor3)
    gmean3 = gmean(non_zero_nor3["nor3"])
    print("gmean2: ", gmean2)
    print("gmean3: ", gmean3)
    print("max3: ", max3)
    print("min3: ", min3)

    gmeans = [gmean_value, gmean2, gmean3]

    gmean_row = pd.DataFrame([{'App': 'GMEAN', 'normal': gmeans[0], 'nor2': gmeans[1], 'nor3': gmeans[2]}])
    df = pd.concat([df, gmean_row], ignore_index=True)

    color = ['#a3d5ff', '#f46036', '#001f54']


    ax = df.plot(
        x='App',
        y=["normal", "nor2", "nor3"],
        kind='bar',
        align='center',
        width=0.9,
        figsize=(11, 3),
        # alpha = 0.9,
        color=color,
        # colormap='tab20c_r',
        alpha = default_alpha-0.1,
        edgecolor='white',
        label=['CC', "Base+UVM", "CC+UVM"],
    )

    plt.axhline(y=1, color='#102542', linestyle='--', linewidth=0.5)
    plt.axvline(x=27.5, color='#102542', linestyle='--', linewidth=0.5)
    
    ax.set_ylim(0.3, 5000000)
    ax.set_yscale('log')
    ax.set_yticks([1, 1000, 1000000])
    ax.set_xlabel("")
    # x ticks font size
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    ax.set_ylabel("Norm. Performance", fontsize=12)
    plt.legend(bbox_to_anchor=(0.7, 0.95), loc='upper center', ncol=3, fontsize=12)
    plt.tight_layout()
    plt.savefig("/Users/yangyang/Desktop/ispass_25_artifact/figure/" +"fig-" + benchname+'-kern_sum_nog.pdf', format='pdf')


if __name__ == "__main__":
    draw_ng()