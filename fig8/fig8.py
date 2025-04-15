#!/usr/bin/python3
import sys
sys.path.append('..')
from common import *


rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/"
api_trace_dir = rootpath + "example_csv/"

modea = ["-nor-nor", "-cc-nor", "-nor-uvm", "-cc-uvm"]

api_trace_postfix = "_cuda_api_trace.csv"
kern_trace_postfix = "_cuda_gpu_trace.csv"

fig_api, axes_api = plt.subplots(2, 6, figsize=(9, 3.2))  # For API
fig_kern, axes_kern = plt.subplots(2, 6, figsize=(9, 3.2))  # For Kernel

axes_api = axes_api.flatten()
axes_kern = axes_kern.flatten()


def draw_api_trace(file_1:str, file_2:str, app_name:str, type:str, ax, first_col):

    if type == "api":
        data1 = process_pd(file_1)
        intrest_cols = ["Duration (ns)", "Name"]
        api_filtered_data1 = data1[intrest_cols]
        api_filtered_data1 = api_filtered_data1[api_filtered_data1['Name'] == "cudaLaunchKernel"]
        api_filtered_data1['Duration (us)'] = api_filtered_data1['Duration (ns)'] / 1_000
        api_mean_1 = api_filtered_data1['Duration (us)'].mean()
        durations1 = np.sort(api_filtered_data1['Duration (us)'])
        # remove the last 5 elements
        durations1 = durations1[:-4]
        cdf1 = np.arange(1, len(durations1) + 1) / len(durations1)
        # Process second file
        data2 = process_pd(file_2)
        api_filtered_data2 = data2[intrest_cols]
        api_filtered_data2 = api_filtered_data2[api_filtered_data2['Name'] == "cudaLaunchKernel"]
        api_filtered_data2['Duration (us)'] = api_filtered_data2['Duration (ns)'] / 1_000
        api_mean_2 = api_filtered_data2['Duration (us)'].mean()
        durations2 = np.sort(api_filtered_data2['Duration (us)'])
        durations2 = durations2[:-4]
        cdf2 = np.arange(1, len(durations2) + 1) / len(durations2)
        print("app: {}, api mean 1: {}, api mean 2: {}".format(app_name, api_mean_1, api_mean_2))
    else:
        data1 = process_pd(file_1)
        intrest_cols = ["Duration (ns)", "Name"]
        api_filtered_data1 = data1[intrest_cols]
        api_filtered_data1 = api_filtered_data1[api_filtered_data1['Name'].str.contains(r'\(.*\)', regex=True)]
        api_filtered_data1['Duration (us)'] = api_filtered_data1['Duration (ns)'] / 1_000
        api_mean_1 = api_filtered_data1['Duration (us)'].mean()
        durations1 = np.sort(api_filtered_data1['Duration (us)'])
        cdf1 = np.arange(1, len(durations1) + 1) / len(durations1)
        data2 = process_pd(file_2)
        api_filtered_data2 = data2[intrest_cols]
        api_filtered_data2 = api_filtered_data2[api_filtered_data2['Name'].str.contains(r'\(.*\)', regex=True)]
        api_filtered_data2['Duration (us)'] = api_filtered_data2['Duration (ns)'] / 1_000
        api_mean_2 = api_filtered_data2['Duration (us)'].mean()
        durations2 = np.sort(api_filtered_data2['Duration (us)'])
        cdf2 = np.arange(1, len(durations2) + 1) / len(durations2)
        print("app: {}, kern mean 1: {}, kern mean 2: {}".format(app_name, api_mean_1,  api_mean_2))
    

    ax.plot(durations1, cdf1, color='royalblue', label='Base')
    ax.plot(durations2, cdf2, color='tab:orange', label='CC', alpha=0.7)

    ax.axvline(api_mean_1, color='royalblue', linestyle='--', label='Base Mean')
    ax.axvline(api_mean_2, color='tab:orange', linestyle='--', label='CC Mean')

    if not first_col:
        ax.set_yticks([])
    else:
        ax.set_yticks([0,0.5,1])
        # y ticks font size
        ax.tick_params(axis='y', labelsize=12)
    
        

    ax.set_xticks([])
    if app_name == "logistic-regression":
        app_name = "log-reg"
    elif app_name == "particlefilter":
        app_name = "partfil"
    elif app_name == "streamcluster":
        app_name = "sc"
    ax.set_xlabel(app_name.lower(), fontsize=12)
    
if __name__ == "__main__":

    all_apps1 = ["BN", "CNN", "kmeans", "knn","logistic-regression", "hotspot3D", "nw","particlefilter", "streamcluster", "3DCONV", "FDTD-2D", "GRAMSCHM"]

    for i, app in enumerate(all_apps1):
        #normal
        first_col = (i %6 == 0)
        api_trace_file_1 = api_trace_dir + app + modea[0] + api_trace_postfix
        # cc
        api_trace_file_2 = api_trace_dir + app + modea[1] + api_trace_postfix
        draw_api_trace(api_trace_file_1,api_trace_file_2,app, "api", axes_api[i], first_col)
        #normal
        kern_trace_file_1 = api_trace_dir + app + modea[0] + kern_trace_postfix
        # cc
        kern_trace_file_2 = api_trace_dir + app + modea[1] + kern_trace_postfix
        draw_api_trace(kern_trace_file_1,kern_trace_file_2,app, "kern", axes_kern[i], first_col)
    

    fig_api.subplots_adjust(wspace=0.1, hspace=0.3)
    fig_kern.subplots_adjust(wspace=0.1, hspace=0.3)
    
    handles, labels = axes_api[0].get_legend_handles_labels()

    axes_api[0].legend(handles, labels,bbox_to_anchor=(3.5, 1.42), loc='upper center', ncol=4, fontsize=12)
    
    handles, labels = axes_kern[0].get_legend_handles_labels()
    axes_kern[0].legend(handles, labels,bbox_to_anchor=(3.5, 1.42), loc='upper center', ncol=4, fontsize=12)
    
    output_path = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
    fig_api.savefig(output_path+"fig-api_combined_cdf.pdf", dpi=900)
    fig_kern.savefig(output_path+"fig-kern_combined_cdf.pdf", dpi=900)
    plt.close(fig_api)
    plt.close(fig_kern)