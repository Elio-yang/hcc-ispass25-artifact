import os
import time


all_apps =[
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_data_thread_centric",
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_data_warp_centric",
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_topo_atomic",
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_topo_frontier",
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_topo_thread_centric",
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_topo_unroll",
"/shared/graphBIG/gpu_bench/gpu_BFS/bfs_topo_warp_centric",
"/shared/graphBIG/gpu_bench/gpu_BetweennessCentr/betweenness",
"/shared/graphBIG/gpu_bench/gpu_ConnectedComp/connected_comp",
"/shared/graphBIG/gpu_bench/gpu_DegreeCentr/degree_centr",
"/shared/graphBIG/gpu_bench/gpu_GraphColoring/gc_data_thread_centric",
"/shared/graphBIG/gpu_bench/gpu_GraphColoring/gc_data_warp_centric",
"/shared/graphBIG/gpu_bench/gpu_GraphColoring/gc_topo_thread_centric",
"/shared/graphBIG/gpu_bench/gpu_GraphColoring/gc_topo_warp_centric",
"/shared/graphBIG/gpu_bench/gpu_SSSP/sssp_data_thread_centric",
"/shared/graphBIG/gpu_bench/gpu_SSSP/sssp_data_warp_centric",
"/shared/graphBIG/gpu_bench/gpu_SSSP/sssp_topo_thread_centric",
"/shared/graphBIG/gpu_bench/gpu_SSSP/sssp_topo_warp_centric",
"/shared/graphBIG/gpu_bench/gpu_TriangleCount/triangle_count",
"/shared/graphBIG/gpu_bench/gpu_kCore/kcore"
]


# all_apps = ["BN","logistic-regression","srad"]

print_options = "--trace=cuda --force-overwrite true "
print_file = " --output "

output_path = " /shared/graphBIG/graph-nsys_results/"
output_sub_path = " /shared/graphBIG/graph-nsys_results/"

abs_path = "/shared/graphBIG/"


# cmd_osrt = "nsys stats --report osrt_sum --format=csv"
# cmd_mem_time = "nsys stats --report cuda_gpu_mem_time_sum --format=csv " 
# cmd_um = "nsys stats --report um_sum --format=csv "
# cmd_um_tot = "nsys stats --report um_total_sum --format=csv " 
cmd_api_trace = "nsys stats --report cuda_api_trace --format=csv "
cmd_kern_trace = "nsys stats --report cuda_gpu_trace --format=csv "
cmd_api_sum = "nsys stats --report cuda_api_sum --format=csv " 
cmd_kern_sum = "nsys stats --report cuda_gpu_kern_sum --format=csv " 

cmd_save = " --force-export=true --output "

# change this to real nsys output file name
csv_osrt = "_osrt_sum.csv"
csv_api_sum = "_cuda_api_sum.csv"
csv_kern_sum = "_cuda_gpu_kern_sum.csv"
csv_mem_time = "_cuda_gpu_mem_time_sum.csv"
csv_um = "_um_sum.csv"
cmd_launch_queue = "nsys stats --report cuda_kern_exec_trace --format=csv "
csv_um_tot = "_um_total_sum.csv"
# nsys stats --report osrt_sum --format=csv --output osrt_summary.csv report1.nsys-rep
# nsys stats --report cuda_api_sum --format=csv --output cuda_api_summary.csv report1.nsys-rep
# nsys stats --report cuda_gpu_kern_sum --format=csv --output cuda_gpu_kernel_summary.csv report1.nsys-rep
# nsys stats --report cuda_gpu_mem_time_sum --format=csv --output cuda_gpu_mem_time_summary.csv report1.nsys-rep
# nsys stats --report um_sum --format=csv --output um_summary.csv report1.nsys-rep
# nsys stats --report um_total_sum --format=csv --output um_total_summary.csv report1.nsys-rep

def profile():
    warmuped2 = False
    runs = 0
    # run 5 times for each app
    for ptime in range(0,5):
        save_folder = "nor"+str(ptime)
        app_cnt = 0
        for app in all_apps:
            if warmuped2 == False:
                #warmup 5 times
                for i in range(5):
                    print(f"[warmup] {i}")
                    warmup_command = app
                    os.system(warmup_command)
                warmuped2 = True
            short_name = app.split("/")[-1]
            command ="nsys profile " + print_options + print_file + output_path + save_folder + "/"  + short_name + "-cc-nor"   + " " + app                
            print(command)
            print(f"{[app_cnt]} Profiling: {short_name}")
            os.system(command)
            print(f"{[app_cnt]} Profiling Done: {short_name}")
            app_cnt += 1
        print(f"Run {runs} Done")
        runs += 1

def process_csv():


    postfix1 = "-nor-nor"
    postfix2 = "-cc-nor"
    files = [postfix1, postfix2]


    csvs = ["0/", "1/", "2/", "3/", "4/"]
    # get file folder and file name
    csv_path2 =  "graph-nsys_results/csv"
    base_path2 = "graph-nsys_results/nor"
    queue_path = "graph-nsys_results/csv_queue"
    for i, app in enumerate(all_apps):
        for pf in files:
            # /shared/uvm_bench/cc-results/uvm/nw_summary_UVM.nsys-rep
            short_name = app.split("/")[-1]
            for runid in csvs:
                # csv0/
                csv_save = abs_path + queue_path + short_name + pf
                rep_file = abs_path + base_path2 + runid + short_name + pf +".nsys-rep"

                # stats_osrt_cmd = cmd_osrt + cmd_save + csv_file_base + " " + result_file         
                # stats_api_sum_cmd = cmd_api_sum + cmd_save + csv_save + " " + rep_file
                # stats_kern_sum_cmd = cmd_kern_sum + cmd_save + csv_save + " " + rep_file
                # stats_api_trace = cmd_api_trace + cmd_save + csv_save + " " + rep_file
                # stats_kern_trace = cmd_kern_trace + cmd_save + csv_save + " " + rep_file
                stats_launch_queue = cmd_launch_queue + cmd_save + csv_save + " " + rep_file
                # os.system(stats_api_sum_cmd)
                # os.system(stats_kern_sum_cmd)
                # os.system(stats_api_trace)
                # os.system(stats_kern_trace)
                os.system(stats_launch_queue)
                print(f"{[runid]} {app} {pf} Done")
            
        print(f"{[i]} {app} {pf} Done")


if __name__ == "__main__":
    # profile()
    process_csv()