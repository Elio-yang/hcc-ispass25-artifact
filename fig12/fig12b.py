import sys
sys.path.append('..')
from common import *



kern_sum_dir = root_dir + "size-csv/"
benchname = "uench"


# non uvm mode
mod_nor = ["-nor-nor", "-cc-nor"]
# keep the nor-nor baseline
mod_uvm = ["-nor-nor", "-nor-uvm", "-cc-uvm"]


api_trace_postfix = "_cuda_api_trace.csv"
kern_trace_postfix = "_cuda_gpu_trace.csv"

api_sum = "_cuda_kern_exec_trace.csv"

processed_sums_1 = []
processed_sums_2 = []

def get_api_sum(app_name:str, idx = -1):
    intrest_cols = ["API Start (ns)","API Dur (ns)","Queue Dur (ns)"]
    if idx != -1:
        app_name = "csv_queue"+app_name
    kern_sum_file1 = kern_sum_dir + app_name + mod_nor[0] + api_sum

    df = process_pd(kern_sum_file1)
    df = df[intrest_cols].reset_index(drop=True)
    df = df.fillna(0)
    tot_time = (df.iloc[-1]["API Start (ns)"] + df.iloc[-1]["API Dur (ns)"]) - df.iloc[0]["API Start (ns)"]
    launch_dur = df["API Dur (ns)"].sum()
    lauch_queue_dur = tot_time - launch_dur
    kern_queue_dur = df["Queue Dur (ns)"].sum()
    kernel_num = df.shape[0]
    average_launch_dur = df["API Dur (ns)"].mean()
    average_queue_dur = df["Queue Dur (ns)"].mean()
    print(f"in ns, Base tot_time: {tot_time}, launch_dur: {launch_dur}, launch_queue_dur:{lauch_queue_dur}, queue_dur: {kern_queue_dur}, kernel_num: {kernel_num}, average_launch_dur: {average_launch_dur}, average_queue_dur: {average_queue_dur}")
   
    mode = "base"
    if idx != -1:
        name = all_app_names[idx]
    else:
        name = app_name
    data_nor = [name, mode, tot_time, launch_dur, lauch_queue_dur, kern_queue_dur, kernel_num, average_launch_dur, average_queue_dur]

    kern_sum_file2 = kern_sum_dir + app_name + mod_nor[1] + api_sum
    df2 = process_pd(kern_sum_file2)
    df2 = df2[intrest_cols].reset_index(drop=True)
    df2 = df2.fillna(0)


    tot_time = (df2.iloc[-1]["API Start (ns)"] + df2.iloc[-1]["API Dur (ns)"]) - df2.iloc[0]["API Start (ns)"]
    launch_dur = df2["API Dur (ns)"].sum()
    lauch_queue_dur = tot_time - launch_dur
    kern_queue_dur = df2["Queue Dur (ns)"].sum()
    kernel_num = df2.shape[0]
    average_launch_dur = df2["API Dur (ns)"].mean()
    average_queue_dur = df2["Queue Dur (ns)"].mean()
    print(f"in ns, Base tot_time: {tot_time}, launch_dur: {launch_dur}, launch_queue_dur: {lauch_queue_dur}, kern_queue_dur: {kern_queue_dur}, kernel_num: {kernel_num}, average_launch_dur: {average_launch_dur}, average_queue_dur: {average_queue_dur}")

    mode = "cc"
    if idx != -1:
        name = all_app_names[idx]
    else:
        name = app_name
    data_cc = [name, mode, tot_time, launch_dur, lauch_queue_dur, kern_queue_dur, kernel_num, average_launch_dur, average_queue_dur]

    processed_sums_1.append(data_nor)
    processed_sums_2.append(data_cc)


def draw_launch_cnt():

    unrolls = [1,2,4,8,16,32,64,128]

    folder = "/Users/yangyang/Desktop/ispass_25_artifact/fig11/cnt-csv/csv-"
    mode1 = "cc-"
    mode2 = "nor-"
    postfix = "_cuda_kern_exec_trace.csv"

    nbase = []
    ncc = []
    config = []

    for idx, app in enumerate(unrolls):
        base = []
        cc = []
        for runs in [1,2,3,4,5]:
            file1 = folder + str(runs) + "/"+ mode1 + "launch-"+ str(app) + postfix
            file2 = folder + str(runs) + "/"+ mode2 + "launch-"+ str(app) + postfix
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)
            intrest_cols = ["API Dur (ns)"]
            df1 = df1[intrest_cols].reset_index()
            df2 = df2[intrest_cols].reset_index()
            df1["us"] = df1["API Dur (ns)"] / 1000000
            df2["us"] = df2["API Dur (ns)"] / 1000000
            cc.append(df1)
            base.append(df2)
        
        base_df = pd.concat(base).groupby(level=0).mean()
        cc_df = pd.concat(cc).groupby(level=0).mean()

        mean1 = base_df["us"].mean()
        mean2 = cc_df["us"].mean()


        nbase.append(mean1)
        ncc.append(mean2)
        config.append(idx)
    
    fig, axs = plt.subplots(1,2,figsize=(3.5, 1.5))
    axs = axs.flatten()
    dfn = pd.DataFrame({'cnt': config, 'base': nbase, 'cc': ncc})
    h1= dfn.plot.scatter(x="cnt", y="base", ax=axs[0], color='royalblue', alpha=0.7, label='Base')
    h2= dfn.plot.scatter(x="cnt", y="cc", ax=axs[0], color='teal', alpha=0.7, label='CC')


    nbase = []
    ncc = []
    config = []

    for idx, app in enumerate(unrolls):
        base = []
        cc = []
        for runs in [1,2,3,4,5]:
            file1 = folder + str(runs) + "/"+ mode1 + "launch-"+ str(app) + postfix
            file2 = folder + str(runs) + "/"+ mode2 + "launch-"+ str(app) + postfix
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)
            intrest_cols = ["API Start (ns)","API Dur (ns)"]
            df1 = df1[intrest_cols].reset_index()
            df2 = df2[intrest_cols].reset_index()
            tot_time1 = (df1.iloc[-1]["API Start (ns)"] + df1.iloc[-1]["API Dur (ns)"]) - df1.iloc[0]["API Start (ns)"]
            tot_time2 = (df2.iloc[-1]["API Start (ns)"] + df2.iloc[-1]["API Dur (ns)"]) - df2.iloc[0]["API Start (ns)"]
            
            sum1 = df1["API Dur (ns)"].sum()
            sum2 = df2["API Dur (ns)"].sum()

            lq1 = tot_time1 - sum1
            lq2 = tot_time2 - sum2
            cc.append(lq1/1000)
            base.append(lq2/1000)
        
        # base mean
        mean1 = np.mean(base)
        mean2 = np.mean(cc)

        nbase.append(mean1)
        ncc.append(mean2)
        config.append(idx)
    
    dfn = pd.DataFrame({'cnt': config, 'base': nbase, 'cc': ncc})
    dfn.plot.scatter(x="cnt", y="base", ax=axs[1], color='royalblue', alpha=0.7, label='Base')
    dfn.plot.scatter(x="cnt", y="cc", ax=axs[1], color='teal', alpha=0.7, label='CC')


    for ax in axs:
        ax.set_xticks(range(0, len(unrolls))) 
        ax.set_xticklabels([0,1,2,3,4,5,6,7], fontsize=8)
        ax.tick_params(axis='y', labelsize=8)
    axs[0].set_ylabel("Time (ms)", fontsize=8)
    axs[1].set_ylabel("Time (us)", fontsize=8)
    axs[0].set_xlabel("Launch cnt. (2^i)", fontsize=8)
    axs[1].set_xlabel("Launch cnt. (2^i)", fontsize=8)
    axs[0].legend(fontsize=8).set_visible(False)
    axs[1].legend().set_visible(False)



    labels = ['KLO', 'LQT']
    for i, a in enumerate(axs):
        a.text(
            0.6, 0.95,
            labels[i],  
            transform=a.transAxes, 
            color = 'black',
            fontsize=8,
            fontweight='bold',
            ha='right',  
            va='top'    
    )


    plt.subplots_adjust(wspace=0)
    plt.subplots_adjust(hspace=0)
    plt.tight_layout()
    output_path = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    plt.savefig(output_path +"fig-kcnt.pdf", format='pdf', dpi = 900)



if __name__ == "__main__":

    draw_launch_cnt()