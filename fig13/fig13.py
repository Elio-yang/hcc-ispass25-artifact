#!/usr/bin/python3
import sys
# add .. in the path
sys.path.append("..")
from common import *


mode = ["-nor-","-cc-"]
post_fix = "_train_throughputs.csv"
post_fix2 = "_amp_train_throughputs.csv"
post_fix3 = "_fp16_train_throughputs.csv"

rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/fig12/"
csv_rootpath = rootpath +"dnn_results/"
out_dir ="/Users/yangyang/Desktop/ispass_25_artifact/fig12/saved/"

models = [
    "vgg16",
    "resnet50",
    "mobilenetv2",
    "squeezenet",
    "attention92",
    "inceptionv4",
]
ml_batch_size = ["64","512","1024"]
fp16_batch_size = ["1024"]


processed= []
processed2 = []
processed3 = []

def process(log, x_flag):

    mode = log[0].split("/")[-1].split("-")[1]
    if mode == "nor":
        mode = "Base"
    else:
        mode = "CC"
    
    fp32_log = log[0]
    amp_log = log[1]

    fp16_log = None
    if len(log) == 3:
        fp16_log = log[2]

    dnn_mdl = log[0].split("/")[-1].split("-")[0]
    dnn_mdl = dnn_mdl.upper()

    
    pd = process_pd(fp32_log)
    time_aligned = pd['Timestamps'] - pd['Timestamps'].min()
    bsize = pd['Bsize'].unique()
    pd['Timestamps (s)'] = time_aligned

    pd_time = pd['Timestamps (s)']
    end_time1 = pd_time.max()

    pd_epoch = pd['Epoch']
    pd_th = pd['Thput (img/s)']
    pd_loss = pd['Epoch Loss']
    avg_th = pd_th.mean()


    pd2 = process_pd(amp_log)
    time_aligned = pd2['Timestamps'] - pd2['Timestamps'].min()
    bsize = pd2['Bsize'].unique()
    pd2['Timestamps (s)'] = time_aligned
    pd2_time = pd2['Timestamps (s)']
    end_time2 = pd2_time.max()
    pd2_epoch = pd2['Epoch']
    pd2_th = pd2['Thput (img/s)']
    pd2_loss = pd2['Epoch Loss']
    avg_th2 = pd2_th.mean()

    if fp16_log:
        pd3 = process_pd(fp16_log)
        time_aligned = pd3['Timestamps'] - pd3['Timestamps'].min()
        bsize = pd3['Bsize'].unique()
        pd3['Timestamps (s)'] = time_aligned
        pd3_time = pd3['Timestamps (s)']
        end_time3 = pd3_time.max()
        pd3_epoch = pd3['Epoch']
        pd3_th = pd3['Thput (img/s)']
        pd3_loss = pd3['Epoch Loss']
        avg_th3 = pd3_th.mean()
    output_name = log[0].split("/")[-1].split(".csv")[0]
    model_name = output_name.split("-")[0]
    batch_size = output_name.split("-")[-1].split("b")[-1].split("_")[0]
    
    data = [model_name,mode,batch_size,avg_th, avg_th2]
    processed.append(data)

    if fp16_log:
        data = [model_name,mode,batch_size,avg_th3]
        processed2.append(data)


def process2(log, x_flag):
    print(log)

    mode = log[0].split("/")[-1].split("-")[1]
    if mode == "nor":
        mode = "Base"
    else:
        mode = "CC"
    
    fp32_log = log[0]
    amp_log = log[1]

    fp16_log = None
    if len(log) == 3:
        fp16_log = log[2]

    dnn_mdl = log[0].split("/")[-1].split("-")[0]
    dnn_mdl = dnn_mdl.upper()

    
    pd = process_pd(fp32_log)
    time_aligned = pd['Timestamps'] - pd['Timestamps'].min()
    pd['Timestamps (s)'] = time_aligned

    pd_time = pd['Timestamps (s)']
    # finish time
    end_time1 = pd_time.max()


    pd2 = process_pd(amp_log)
    time_aligned = pd2['Timestamps'] - pd2['Timestamps'].min()
    bsize = pd2['Bsize'].unique()
    pd2['Timestamps (s)'] = time_aligned
    pd2_time = pd2['Timestamps (s)']
    end_time2 = pd2_time.max()

    end_time3 = 0
    if fp16_log:
        pd3 = process_pd(fp16_log)
        time_aligned = pd3['Timestamps'] - pd3['Timestamps'].min()
        bsize = pd3['Bsize'].unique()
        pd3['Timestamps (s)'] = time_aligned
        pd3_time = pd3['Timestamps (s)']
        end_time3 = pd3_time.max()

    output_name = log[0].split("/")[-1].split(".csv")[0]
    model_name = output_name.split("-")[0]
    batch_size = output_name.split("-")[-1].split("b")[-1].split("_")[0]


    data = [model_name,mode,batch_size,end_time1, end_time2, end_time3]
    processed3.append(data)


gmeans = []
gmeans2 = []
def draw(axes):
    print(len(axes))
    csv_file = out_dir + "dnn-train/dnn_train_throughputs.csv"
    df = pd.read_csv(csv_file)

    df_base = df[df["mode"] == "Base"]
    df_cc = df[df["mode"] == "CC"]

    df_base_64 = df_base[df_base["batch_size"] == 64].reset_index(drop=True)
    print(df_base_64)
    df_base_512 = df_base[df_base["batch_size"] == 512].reset_index(drop=True)
    df_base_1024 = df_base[df_base["batch_size"] == 1024].reset_index(drop=True)

    df_cc_64 = df_cc[df_cc["batch_size"] == 64].reset_index(drop=True)
    print(df_cc_64)
    df_cc_512 = df_cc[df_cc["batch_size"] == 512].reset_index(drop=True)
    df_cc_1024 = df_cc[df_cc["batch_size"] == 1024].reset_index(drop=True)


    df_cc_64["norm_fp32_th"] = df_cc_64["fp32"] / df_base_64["fp32"]
    df_cc_64["norm_amp_th"] = df_cc_64["amp"] / df_base_64["fp32"]
    cc_64_fp32_gmean = gmean(df_cc_64["norm_fp32_th"])
    cc_64_fp32_min = df_cc_64["norm_fp32_th"].min()
    cc_64_fp32_max = df_cc_64["norm_fp32_th"].max()
    cc_64_amp_gmean = gmean(df_cc_64["norm_amp_th"])
    cc_64_amp_min = df_cc_64["norm_amp_th"].min()
    cc_64_amp_max = df_cc_64["norm_amp_th"].max()
    print(cc_64_fp32_gmean, cc_64_fp32_min, cc_64_fp32_max)
    print(cc_64_amp_gmean, cc_64_amp_min, cc_64_amp_max)


    df_cc_512["norm_fp32_th"] = df_cc_512["fp32"] / df_base_512["fp32"]
    df_cc_512["norm_amp_th"] = df_cc_512["amp"] / df_base_512["fp32"]
    cc_512_fp32_gmean = gmean(df_cc_512["norm_fp32_th"])
    cc_512_fp32_min = df_cc_512["norm_fp32_th"].min()
    cc_512_fp32_max = df_cc_512["norm_fp32_th"].max()
    cc_512_amp_gmean = gmean(df_cc_512["norm_amp_th"])
    cc_512_amp_min = df_cc_512["norm_amp_th"].min()
    cc_512_amp_max = df_cc_512["norm_amp_th"].max()
    print(cc_512_fp32_gmean, cc_512_fp32_min, cc_512_fp32_max)
    print(cc_512_amp_gmean, cc_512_amp_min, cc_512_amp_max)

    df_cc_1024["norm_fp32_th"] = df_cc_1024["fp32"] / df_base_1024["fp32"]
    df_cc_1024["norm_amp_th"] = df_cc_1024["amp"] / df_base_1024["fp32"]
    df_cc_1024["norm_fp16_th"] = df_cc_1024["fp16"] / df_base_1024["fp32"]
    cc_1024_fp32_gmean = gmean(df_cc_1024["norm_fp32_th"])
    cc_1024_fp32_min = df_cc_1024["norm_fp32_th"].min()
    cc_1024_fp32_max = df_cc_1024["norm_fp32_th"].max()

    cc_1024_amp_gmean = gmean(df_cc_1024["norm_amp_th"])
    cc_1024_amp_min = df_cc_1024["norm_amp_th"].min()
    cc_1024_amp_max = df_cc_1024["norm_amp_th"].max()

    cc_1024_fp16_gmean = gmean(df_cc_1024["norm_fp16_th"])
    cc_1024_fp16_min = df_cc_1024["norm_fp16_th"].min()
    cc_1024_fp16_max = df_cc_1024["norm_fp16_th"].max()
    print(cc_1024_fp32_gmean, cc_1024_fp32_min, cc_1024_fp32_max)
    print(cc_1024_amp_gmean, cc_1024_amp_min, cc_1024_amp_max)
    print(cc_1024_fp16_gmean, cc_1024_fp16_min, cc_1024_fp16_max)


    df_base_64["norm_fp32_th"] = df_base_64["fp32"] / df_base_64["fp32"]
    df_base_64["norm_amp_th"] = df_base_64["amp"] / df_base_64["fp32"]
    base_64_fp32_gmean = gmean(df_base_64["norm_fp32_th"])
    base_64_fp32_min = df_base_64["norm_fp32_th"].min()
    base_64_fp32_max = df_base_64["norm_fp32_th"].max()
    
    base_64_amp_gmean = gmean(df_base_64["norm_amp_th"])
    base_64_amp_min = df_base_64["norm_amp_th"].min()
    base_64_amp_max = df_base_64["norm_amp_th"].max()

    df_base_512["norm_fp32_th"] = df_base_512["fp32"] / df_base_512["fp32"]
    df_base_512["norm_amp_th"] = df_base_512["amp"] / df_base_512["fp32"]
    base_512_fp32_gmean = gmean(df_base_512["norm_fp32_th"])
    base_512_fp32_min = df_base_512["norm_fp32_th"].min()
    base_512_fp32_max = df_base_512["norm_fp32_th"].max()
    
    base_512_amp_gmean = gmean(df_base_512["norm_amp_th"])
    base_512_amp_min = df_base_512["norm_amp_th"].min()
    base_512_amp_max = df_base_512["norm_amp_th"].max()


    df_base_1024["norm_fp32_th"] = df_base_1024["fp32"] / df_base_1024["fp32"]
    df_base_1024["norm_amp_th"] = df_base_1024["amp"] / df_base_1024["fp32"]
    df_base_1024["norm_fp16_th"] = df_base_1024["fp16"] / df_base_1024["fp32"]
    base_1024_fp32_gmean = gmean(df_base_1024["norm_fp32_th"])
    base_1024_fp32_min = df_base_1024["norm_fp32_th"].min()
    base_1024_fp32_max = df_base_1024["norm_fp32_th"].max()

    base_1024_amp_gmean = gmean(df_base_1024["norm_amp_th"])
    base_1024_amp_min = df_base_1024["norm_amp_th"].min()
    base_1024_amp_max = df_base_1024["norm_amp_th"].max()

    base_1024_fp16_gmean = gmean(df_base_1024["norm_fp16_th"])
    base_1024_fp16_min = df_base_1024["norm_fp16_th"].min()
    base_1024_fp16_max = df_base_1024["norm_fp16_th"].max()

    datas = [
        base_64_fp32_gmean, base_64_fp32_min, base_64_fp32_max,
        base_64_amp_gmean, base_64_amp_min, base_64_amp_max,
        base_512_fp32_gmean, base_512_fp32_min, base_512_fp32_max,
        base_512_amp_gmean, base_512_amp_min, base_512_amp_max,
        base_1024_fp32_gmean, base_1024_fp32_min, base_1024_fp32_max,
        base_1024_amp_gmean, base_1024_amp_min, base_1024_amp_max,
        base_1024_fp16_gmean, base_1024_fp16_min, base_1024_fp16_max,
        cc_64_fp32_gmean, cc_64_fp32_min, cc_64_fp32_max,
        cc_64_amp_gmean, cc_64_amp_min, cc_64_amp_max,
        cc_512_fp32_gmean, cc_512_fp32_min, cc_512_fp32_max,
        cc_512_amp_gmean, cc_512_amp_min, cc_512_amp_max,
        cc_1024_fp32_gmean, cc_1024_fp32_min, cc_1024_fp32_max,
        cc_1024_amp_gmean, cc_1024_amp_min, cc_1024_amp_max,
        cc_1024_fp16_gmean, cc_1024_fp16_min, cc_1024_fp16_max,
    ]

    gmeans.append(datas)


    colors = ['#00609b', '#1d8dcc', '#7722e7', '#539b32', '#84cc60', '#f72585']

    batch_sizes = [(64, df_base_64, df_cc_64), (512, df_base_512, df_cc_512), (1024, df_base_1024, df_cc_1024)]
    
    for idx, (batch_size, df_base_batch, df_cc_batch) in enumerate(batch_sizes):
        ax = axes[idx]
        if batch_size != 1024:
            df_base_batch.plot(
                x="model",
                position=1,
                y=["fp32", "amp"],
                kind="bar",
                width=0.4,
                color=[colors[0], colors[1]],
                alpha=default_alpha-0.3,
                ax=ax,
                label=["Base-fp32", "Base-amp"]
            )
            df_cc_batch.plot(
                x="model",
                position=0,
                y=["fp32", "amp"],
                kind="bar",
                width=0.4,
                color=[colors[3], colors[4]],
                alpha=default_alpha-0.3,
                ax=ax,
                label=["CC-fp32", "CC-amp"]
            )
        else:
            df_base_batch.plot(
                x="model",
                position=1,
                y=["fp32", "amp", "fp16"],
                kind="bar",
                width=0.4,
                color=[colors[0], colors[1], colors[2]],
                alpha=default_alpha-0.3,
                ax=ax,
                label=["Base-FP32", "Base-AMP", "Base-FP16"]
            )
            df_cc_batch.plot(
                x="model",
                position=0,
                y=["fp32", "amp", "fp16"],
                kind="bar",
                width=0.4,
                color=[colors[3], colors[4], colors[5]],
                alpha=default_alpha-0.3,
                ax=ax,
                label=["CC-FP32", "CC-AMP", "CC-FP16"]
            )
        # Set axis limits and labels
        ax.set_xlim(-0.5, len(df_base_batch["model"]) - 0.5)
        ax.set_ylim(0, 14000)
        ax.set_xlabel("")
        ax.set_ylabel("")

        if idx == 0:
            ax.tick_params(axis='x', labelsize=15)
            ax.tick_params(axis='y', labelsize=15)
        if idx != 0:
            ax.tick_params(axis='y', which='both', left=False, labelleft=False)
            ax.set_yticklabels([])
            ax.set_xticklabels([])

        ax.set_xticklabels([])

        if idx != 0:
            ax.set_yticklabels([])

        if idx == 0:
            ax.set_ylabel("Throughput (img/s)", fontsize=15)
            ax.legend().set_visible(False)
        else:
            ax.legend().set_visible(False)

    labels = ['BS 64', 'BS 512', 'BS 1024']
    for i, a in enumerate(axes):
        a.text(
            0.95, 0.95,
            labels[i],  
            transform=a.transAxes, 
            color = 'black',
            fontsize=15,  
            fontweight='bold',  
            ha='right',  
            va='top'    
    )

    handles, labels = axes[2].get_legend_handles_labels()

    axes[0].legend(handles, labels, loc="upper left", fontsize=15, bbox_to_anchor=(0.1, 1))



def draw2(axes):
    csv_file = out_dir + "dnn-train/dnn_train_time.csv"
    df = pd.read_csv(csv_file)

    df_base = df[df["mode"] == "Base"]
    df_cc = df[df["mode"] == "CC"]

    # base 64
    df_base_64 = df_base[df_base["batch_size"] == 64].reset_index(drop=True)
    df_base_64["fp32_norm"] = df_base_64["fp32"] / df_base_64["fp32"]
    df_base_64["amp_norm"] = df_base_64["amp"] / df_base_64["fp32"]

    base_64_fp32_gmean = gmean(df_base_64["fp32_norm"])
    base_64_fp32_min = df_base_64["fp32_norm"].min()
    base_64_fp32_max = df_base_64["fp32_norm"].max()
    base_64_amp_gmean = gmean(df_base_64["amp_norm"])
    base_64_amp_min = df_base_64["amp_norm"].min()
    base_64_amp_max = df_base_64["amp_norm"].max()
    

    # print(df_base_64)
    # 512
    df_base_512 = df_base[df_base["batch_size"] == 512].reset_index(drop=True)
    df_base_512["fp32_norm"] = df_base_512["fp32"] / df_base_512["fp32"]
    df_base_512["amp_norm"] = df_base_512["amp"] / df_base_512["fp32"]

    base_512_fp32_gmean = gmean(df_base_512["fp32_norm"])
    base_512_fp32_min = df_base_512["fp32_norm"].min()
    base_512_fp32_max = df_base_512["fp32_norm"].max()
    base_512_amp_gmean = gmean(df_base_512["amp_norm"])
    base_512_amp_min = df_base_512["amp_norm"].min()
    base_512_amp_max = df_base_512["amp_norm"].max()


    # 1024
    df_base_1024 = df_base[df_base["batch_size"] == 1024].reset_index(drop=True)
    df_base_1024["fp32_norm"] = df_base_1024["fp32"] / df_base_1024["fp32"]
    df_base_1024["amp_norm"] = df_base_1024["amp"] / df_base_1024["fp32"]
    df_base_1024["fp16_norm"] = df_base_1024["fp16"] / df_base_1024["fp32"]

    base_1024_fp32_gmean = gmean(df_base_1024["fp32_norm"])
    base_1024_fp32_min = df_base_1024["fp32_norm"].min()
    base_1024_fp32_max = df_base_1024["fp32_norm"].max()
    base_1024_amp_gmean = gmean(df_base_1024["amp_norm"])
    base_1024_amp_min = df_base_1024["amp_norm"].min()
    base_1024_amp_max = df_base_1024["amp_norm"].max()
    base_1024_fp16_gmean = gmean(df_base_1024["fp16_norm"])
    base_1024_fp16_min = df_base_1024["fp16_norm"].min()
    base_1024_fp16_max = df_base_1024["fp16_norm"].max()

    # cc 64
    df_cc_64 = df_cc[df_cc["batch_size"] == 64].reset_index(drop=True)
    df_cc_64["fp32_norm"] = df_cc_64["fp32"] / df_base_64["fp32"]
    df_cc_64["amp_norm"] = df_cc_64["amp"] / df_base_64["fp32"]

    cc_64_fp32_gmean = gmean(df_cc_64["fp32_norm"])
    cc_64_fp32_min = df_cc_64["fp32_norm"].min()
    cc_64_fp32_max = df_cc_64["fp32_norm"].max()
    cc_64_amp_gmean = gmean(df_cc_64["amp_norm"])
    cc_64_amp_min = df_cc_64["amp_norm"].min()
    cc_64_amp_max = df_cc_64["amp_norm"].max()



    # 512
    df_cc_512 = df_cc[df_cc["batch_size"] == 512].reset_index(drop=True)
    df_cc_512["fp32_norm"] = df_cc_512["fp32"] / df_base_512["fp32"]
    df_cc_512["amp_norm"] = df_cc_512["amp"] / df_base_512["fp32"]

    cc_512_fp32_gmean = gmean(df_cc_512["fp32_norm"])
    cc_512_fp32_min = df_cc_512["fp32_norm"].min()
    cc_512_fp32_max = df_cc_512["fp32_norm"].max()
    cc_512_amp_gmean = gmean(df_cc_512["amp_norm"])
    cc_512_amp_min = df_cc_512["amp_norm"].min()
    cc_512_amp_max = df_cc_512["amp_norm"].max()


    # 1024
    df_cc_1024 = df_cc[df_cc["batch_size"] == 1024].reset_index(drop=True)
    df_cc_1024["fp32_norm"] = df_cc_1024["fp32"] / df_base_1024["fp32"]
    df_cc_1024["amp_norm"] = df_cc_1024["amp"] / df_base_1024["fp32"]
    df_cc_1024["fp16_norm"] = df_cc_1024["fp16"] / df_base_1024["fp32"]

    cc_1024_fp32_gmean = gmean(df_cc_1024["fp32_norm"])
    cc_1024_fp32_min = df_cc_1024["fp32_norm"].min()
    cc_1024_fp32_max = df_cc_1024["fp32_norm"].max()
    cc_1024_amp_gmean = gmean(df_cc_1024["amp_norm"])
    cc_1024_amp_min = df_cc_1024["amp_norm"].min()
    cc_1024_amp_max = df_cc_1024["amp_norm"].max()
    cc_1024_fp16_gmean = gmean(df_cc_1024["fp16_norm"])
    cc_1024_fp16_min = df_cc_1024["fp16_norm"].min()
    cc_1024_fp16_max = df_cc_1024["fp16_norm"].max()

    data = [
        base_64_fp32_gmean, base_64_fp32_min, base_64_fp32_max,
        base_64_amp_gmean, base_64_amp_min, base_64_amp_max,
        base_512_fp32_gmean, base_512_fp32_min, base_512_fp32_max,
        base_512_amp_gmean, base_512_amp_min, base_512_amp_max,
        base_1024_fp32_gmean, base_1024_fp32_min, base_1024_fp32_max,
        base_1024_amp_gmean, base_1024_amp_min, base_1024_amp_max,
        base_1024_fp16_gmean, base_1024_fp16_min, base_1024_fp16_max,
        cc_64_fp32_gmean, cc_64_fp32_min, cc_64_fp32_max,
        cc_64_amp_gmean, cc_64_amp_min, cc_64_amp_max,
        cc_512_fp32_gmean, cc_512_fp32_min, cc_512_fp32_max,
        cc_512_amp_gmean, cc_512_amp_min, cc_512_amp_max,
        cc_1024_fp32_gmean, cc_1024_fp32_min, cc_1024_fp32_max,
        cc_1024_amp_gmean, cc_1024_amp_min, cc_1024_amp_max,
        cc_1024_fp16_gmean, cc_1024_fp16_min, cc_1024_fp16_max
    ]

    gmeans2.append(data)

    colors = ['#00609b', '#1d8dcc', '#7722e7', '#539b32', '#84cc60', '#f72585']

    batch_sizes = [(64, df_base_64, df_cc_64), (512, df_base_512, df_cc_512), (1024, df_base_1024, df_cc_1024)]
    
    for idx, (batch_size, df_base_batch, df_cc_batch) in enumerate(batch_sizes):
        ax = axes[idx]
        if batch_size != 1024:
            df_base_batch.plot(
                x="model",
                position=1,
                y=["fp32_norm", "amp_norm"],
                kind="bar",
                width=0.4,
                color=[colors[0], colors[1]],
                alpha= default_alpha-0.3,
                ax=ax,
                label=["Base-fp32", "Base-amp"]
            )
            df_cc_batch.plot(
                x="model",
                position=0,
                y=["fp32_norm", "amp_norm"],
                kind="bar",
                width=0.4,
                color=[colors[3], colors[4]],
                alpha= default_alpha-0.3,

                ax=ax,
                label=["CC-fp32", "CC-amp"]
            )
        else:
            df_base_batch.plot(
                x="model",
                position=1,
                y=["fp32_norm", "amp_norm", "fp16_norm"],
                kind="bar",
                width=0.4,
                color=[colors[0], colors[1], colors[2]],
                alpha= default_alpha-0.3,

                ax=ax,
                label=["Base-fp32", "Base-amp", "Base-fp16"]
            )
            df_cc_batch.plot(
                x="model",
                position=0,
                y=["fp32_norm", "amp_norm", "fp16_norm"],
                kind="bar",
                width=0.4,
                color=[colors[3], colors[4], colors[5]],
                alpha= default_alpha-0.3,

                ax=ax,
                label=["CC-fp32", "CC-amp", "CC-fp16"]
            )
        ax.set_xlim(-0.5, len(df_base_batch["model"]) - 0.5)
        ax.set_ylim(0.5, 2.2)
        ax.set_xlabel("")
        ax.set_ylabel("")
        if idx == 0:
            ax.tick_params(axis='x', labelsize=15)
            ax.tick_params(axis='y', labelsize=15)
        # set xticks labels
        ax.set_xticklabels(["vgg16","rn50", "mobv2", "sqnet", "att92", "incpv4"], ha="right", fontsize=15)
        if idx != 0:
            ax.tick_params(axis='y', which='both', left=False, labelleft=False)
            ax.set_yticklabels([])
        if idx == 0:
            ax.set_ylabel("Normalized training time", fontsize=15)
            ax.legend().set_visible(False)
        else:
            ax.legend().set_visible(False)

    labels = ['BS 64', 'BS 512', 'BS 1024']
    for i, a in enumerate(axes):
        a.text(
            0.95, 0.95,
            labels[i],  
            transform=a.transAxes, 
            color = 'black',
            fontsize=15, 
            fontweight='bold',
            ha='right',  
            va='top'    
    )
        
    for ax in axes:
        ax.axhline(y=1, color='#102542', linestyle='--',linewidth=0.5)
        
if __name__ == "__main__":
    



    # files = []
    # sp_files = []
    # for mdl in models:
    #     for m in mode:
    #         for bs in ml_batch_size:
    #             if bs == "1024":
    #                 for ep in epoches:
    #                     csv_file = mdl + m + "e"+ep + "-b" + bs + post_fix
    #                     csv_file2 = mdl + m + "e"+ep + "-b" + bs + post_fix2
    #                     csv_file3 = mdl + m + "e"+ep + "-b" + bs + post_fix3
    #                     files.append([csv_rootpath+csv_file,csv_rootpath+csv_file2, csv_rootpath+csv_file3])
    #             else:
    #                 for ep in epoches:
    #                     csv_file = mdl + m + "e"+ep + "-b" + bs + post_fix
    #                     csv_file2 = mdl + m + "e"+ep + "-b" + bs + post_fix2
    #                     files.append([csv_rootpath+csv_file,csv_rootpath+csv_file2])

    # for mdl in models:
    #     for m in mode:
    #         for bs in fp16_batch_size:
    #             for ep in epoches:
    #                 csv_file = mdl + m + "e"+ep + "-b" + bs + post_fix
    #                 csv_file2 = mdl + m + "e"+ep + "-b" + bs + post_fix2
    #                 csv_file3 = mdl + m + "e"+ep + "-b" + bs + post_fix3
    #                 sp_files.append([csv_rootpath+csv_file, csv_rootpath+csv_file2, csv_rootpath+csv_file3])


    # for log in files:
    #     process2(log,"time")

    # outpath = out_dir + "dnn-train/dnn_train_time.csv"
    # # save the processed data
    # df = pd.DataFrame(processed3, columns=["model","mode","batch_size","fp32","amp", "fp16"])
    # df.to_csv(outpath,index=False)

    # for log in sp_files:
    #     process(log,"time")
    
    # outpath = out_dir + "dnn-train/dnn_fp16_train_throughputs.csv"
    # # save the processed data
    # df = pd.DataFrame(processed2, columns=["model","mode","batch_size","fp16"])
    # df.to_csv(outpath,index=False)


    fig, ax_all = plt.subplots(2,3, figsize=(12, 8))
    ax_all = ax_all.flatten()

    ax1 = ax_all[0:3]
    ax2 = ax_all[3:6] 


    draw(ax1)
    draw2(ax2)


    labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
    for i, a in enumerate(ax_all):
        a.text(
            0.95, 0.85,
            labels[i],
            transform=a.transAxes, 
            color = 'black',
            fontsize=15,
            fontweight='bold',
            ha='right',  
            va='top'    
    )



    plt.tight_layout()
    plt.savefig("/Users/yangyang/Desktop/ispass_25_artifact/figure/" + "fig-dnn_train_all.pdf", format='pdf', dpi=900, bbox_inches="tight")
   
    # write gmeans to csv
    outpath = out_dir + "dnn-train/dnn_train_gmeans.csv"
    df = pd.DataFrame(gmeans, columns=[
        "base_64_fp32_gmean", "base_64_fp32_min", "base_64_fp32_max",
        "base_64_amp_gmean", "base_64_amp_min", "base_64_amp_max",
        "base_512_fp32_gmean", "base_512_fp32_min", "base_512_fp32_max",
        "base_512_amp_gmean", "base_512_amp_min", "base_512_amp_max",
        "base_1024_fp32_gmean", "base_1024_fp32_min", "base_1024_fp32_max",
        "base_1024_amp_gmean", "base_1024_amp_min", "base_1024_amp_max",
        "base_1024_fp16_gmean", "base_1024_fp16_min", "base_1024_fp16_max",
        "cc_64_fp32_gmean", "cc_64_fp32_min", "cc_64_fp32_max",
        "cc_64_amp_gmean", "cc_64_amp_min", "cc_64_amp_max",
        "cc_512_fp32_gmean", "cc_512_fp32_min", "cc_512_fp32_max",
        "cc_512_amp_gmean", "cc_512_amp_min", "cc_512_amp_max",
        "cc_1024_fp32_gmean", "cc_1024_fp32_min", "cc_1024_fp32_max",
        "cc_1024_amp_gmean", "cc_1024_amp_min", "cc_1024_amp_max",
        "cc_1024_fp16_gmean", "cc_1024_fp16_min", "cc_1024_fp16_max",
    ])
    df.to_csv(outpath, index=False)
    
    outpath = out_dir + "dnn-train/dnn_train_time_gmeans.csv"
    df = pd.DataFrame(gmeans2, columns=[
        "base_64_fp32_gmean", "base_64_fp32_min", "base_64_fp32_max",
        "base_64_amp_gmean", "base_64_amp_min", "base_64_amp_max",
        "base_512_fp32_gmean", "base_512_fp32_min", "base_512_fp32_max",
        "base_512_amp_gmean", "base_512_amp_min", "base_512_amp_max",
        "base_1024_fp32_gmean", "base_1024_fp32_min", "base_1024_fp32_max",
        "base_1024_amp_gmean", "base_1024_amp_min", "base_1024_amp_max",
        "base_1024_fp16_gmean", "base_1024_fp16_min", "base_1024_fp16_max",
        "cc_64_fp32_gmean", "cc_64_fp32_min", "cc_64_fp32_max",
        "cc_64_amp_gmean", "cc_64_amp_min", "cc_64_amp_max",
        "cc_512_fp32_gmean", "cc_512_fp32_min", "cc_512_fp32_max",
        "cc_512_amp_gmean", "cc_512_amp_min", "cc_512_amp_max",
        "cc_1024_fp32_gmean", "cc_1024_fp32_min", "cc_1024_fp32_max",
        "cc_1024_amp_gmean", "cc_1024_amp_min", "cc_1024_amp_max",
        "cc_1024_fp16_gmean", "cc_1024_fp16_min", "cc_1024_fp16_max",
    ])
    df.to_csv(outpath, index=False)
