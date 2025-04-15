#!/usr/bin/python3
import sys
sys.path.append('..')
from common import *


rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/"
api_trace_dir = rootpath + "example_csv/"

modea = ["-nor-nor", "-cc-nor"]
api_trace_postfix = "_cuda_api_trace.csv"
kern_trace_postfix = "_cuda_gpu_trace.csv"

def draw_api_kern_trace(api_file:str, kern_file:str, app_name:str, ax, idx):
    modes = app_name.split('-')
    post_fix = ''
    marker1 = 'o'
    marker2 = '^'
    uvm_on = modes[2] == 'uvm'
    cc_on = modes[1] == 'cc'
    
    if cc_on:
        post_fix += '-CC'
        marker1 = 'P'
        marker2='X'
    else:
        post_fix += '-NOR'
    
    if uvm_on:
        post_fix += '-UVM'
    else:
        post_fix += ''
    
    data = process_pd(api_file)
    intrest_cols = ["Start (ns)","Duration (ns)","Name"]
    api_filtered_data = data[intrest_cols]
    api_filtered_data = api_filtered_data[
        (api_filtered_data['Name'] == "cudaLaunchKernel") | (api_filtered_data['Name'] == "cudaDeviceSynchronize")
    ]
    name_map = {"cudaLaunchKernel": "Launch", "cudaDeviceSynchronize": "Sync"}

    api_filtered_data = api_filtered_data.sort_values(by=['Duration (ns)'])
    api_filtered_data = api_filtered_data[:-5]
    api_start_aligned = api_filtered_data['Start (ns)'] - api_filtered_data['Start (ns)'].min()
    api_filtered_data['Aligned Start (ns)'] = api_start_aligned
    api_filtered_data['Aligned Start (us)'] = api_filtered_data['Aligned Start (ns)'] / 1_000
    api_filtered_data['Duration (us)'] = api_filtered_data['Duration (ns)'] / 1_000
    api_avg_duration = api_filtered_data['Duration (us)'].mean()
    api_unique_names = api_filtered_data['Name'].unique()
    sync_data = api_filtered_data[api_filtered_data['Name'] == "cudaDeviceSynchronize"]



    kdata = process_pd(kern_file)
    kern_filtered_data = kdata[intrest_cols]
    kern_filtered_data = kern_filtered_data[kern_filtered_data['Name'].str.contains(r'\(.*\)', regex=True)]
    kern_start_aligned = kern_filtered_data['Start (ns)'] - api_filtered_data['Start (ns)'].min()
    kern_filtered_data['Aligned Start (ns)'] = kern_start_aligned
    kern_filtered_data['Aligned Start (us)'] = kern_filtered_data['Aligned Start (ns)'] / 1_000
    kern_filtered_data['Duration (us)'] = kern_filtered_data['Duration (ns)'] / 1_000
    kern_avg_duration = kern_filtered_data['Duration (us)'].mean()

    name = app_name.split('-')[0]
    if name == "kmeans":
        print(api_filtered_data)
        launch_dur = api_filtered_data['Duration (us)'].sum()
        print('klo:{}'.format(launch_dur))

        # last stats time + last duration
        last_sync_time = api_filtered_data.iloc[0]['Aligned Start (us)']
        last_sync = api_filtered_data.iloc[0]['Duration (us)']
        print('last_launch_time:{}'.format(last_sync_time))
        print('last_launch_dur:{}'.format(last_sync))
        lq = last_sync_time + last_sync - launch_dur
        
        print('mode:{}'.format(api_file))
        print("app: {}, lq: {}".format(app_name, lq))


    alpha_d = default_alpha
    alpha_d2 = 0.4
    msize = 28
    idx = 0
    msize2 = 28
    colors2 =plt.cm.ocean(np.linspace(0, 1, 4))
    color_cus_1= ['#a597b6','#f74c0c']
    color_cus_2= ['#57c65f','#3892fa']

    if not cc_on:    
        colors = color_cus_1
        msize = 28
        alpha_d2 = 0.4
    else: #cc
        colors = color_cus_2
        alpha_d = 0.3
        alpha_d2 = 0.3
        idx = 2
        msize2 = 28

    markers = ['o','o']

    if post_fix == '-NOR':
        post_fix = '-Base'
    else:
        post_fix = '-CC'
    for i, name in enumerate(["cudaLaunchKernel"]):
        subset = api_filtered_data[api_filtered_data['Name'] == name]
        ax.scatter(
            subset['Aligned Start (us)'], 
            subset['Duration (us)'], 
            label=name_map[name]+post_fix, 
            marker=markers[i],
            s=msize2,
            color=colors[i],
            alpha=alpha_d2
        )

    if not cc_on:
        kcolor = '#f74c0c'
    else:
        kcolor= '#3892fa'
        alpha_d = 0.4
    
    ax.scatter(
        kern_filtered_data['Aligned Start (us)'], 
        kern_filtered_data['Duration (us)'], 
        label="Kernel"+post_fix, 
        marker='o',
        s=msize,
        color=kcolor,
        alpha=alpha_d
    )

    ax.tick_params(axis='x', labelsize=11)
    ax.tick_params(axis='y', labelsize=11)


if __name__ == "__main__":
    apps = ["hotspot3D","particlefilter", "streamcluster", "3DCONV"]
    fig, ax = plt.subplots(1,4, figsize=(12, 3))
    ax = ax.flatten()
    for idx,app in enumerate(apps):
        for mod in modea:
            new_app = app+mod
            api_trace_file = api_trace_dir + new_app + api_trace_postfix
            kern_trace_file = api_trace_dir + new_app + kern_trace_postfix
            print(api_trace_file)
            print(kern_trace_file)
            draw_api_kern_trace(api_trace_file,kern_trace_file,new_app,ax[idx],idx)

    plt.tight_layout()
    idx_to_adjust = 2 
    ax[idx_to_adjust].ticklabel_format(style='sci', axis='x', scilimits=(6, 6)) 
    ax[idx_to_adjust].xaxis.get_offset_text().set_fontsize(12)
    handles, labels = ax[3].get_legend_handles_labels()
    print(labels)
    sorted_indices = sorted(range(len(labels)), key=lambda i: labels[i])
    handles = [handles[i] for i in sorted_indices]
    labels = [labels[i] for i in sorted_indices]

    fig.legend(
        handles, labels, 
        loc="upper center",  
        fontsize=12,         
        ncol=4,             
        bbox_to_anchor=(0.53, 1.12)
    )
    fig.subplots_adjust(wspace=0.2, hspace=0.2)

    ytick_ranges = [
    (0, 60, 10),    
    (0, 160, 20),  
    (0, 80, 10), 
    (0, 30, 5), 
    ]

    for i, a in enumerate(ax):
        start, end, step = ytick_ranges[i]
        a.set_yticks(range(start, end + 1, step))
        a.set_ylim(start, end)

    labels = ['A', 'B', 'C', 'D']
    for i, a in enumerate(ax):
        a.text(
            0.95, 0.95,
            labels[i],  
            transform=a.transAxes, 
            color = 'black',
            fontsize=12,  
            fontweight='bold',  
            ha='right',  
            va='top'    
    )
        
    for i, a in enumerate(ax):
        a.text(
        0.5, 0.96,  
        apps[i].lower(),  
        transform=a.transAxes, 
        color='black', 
        fontsize=12,  
        ha='center',  
        va='top'      
        )


    output_file = "/Users/yangyang/Desktop/ispass_25_artifact/figure/fig-select_api_trace.pdf"
    plt.savefig(output_file, format='pdf', dpi=900, bbox_inches="tight")
    plt.close()
