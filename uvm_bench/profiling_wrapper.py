import os

import time
from time import localtime, strftime


# folders = ["rodinia"]
# 33 apps in total
folders = ["BN", "bfs", "CNN", "kmeans", "knn", "logistic-regression", "rodinia", "polybench"]
# folders = ["BN", "logistic-regression", "rodinia"]
# folders = ["rodinia", "polybench"]
subfolders = ["backprop", "dwt2d", "hotspot", "hotspot3D", "nw", "particlefilter", "pathfinder", "srad", "streamcluster"]
# subfolders = ["srad"]
subfolders2 = ["2DCONV", "2MM", "3DCONV", "3MM", "ATAX", "BICG", "CORR", "COVAR", "FDTD-2D", 
               "GEMM-1MB", "GEMM-4MB", "GEMM-64MB", "GEMM-100MB", "GEMM-400MB","GEMM-900MB", "GEMM-1024MB", "GEMM-1600MB",  
               "GESUMMV", "GRAMSCHM", "MVT", "SYR2K", "SYRK"]

all_apps = ["BN", "bfs", "CNN", "kmeans", "knn", "logistic-regression", 
            "backprop", "dwt2d", "hotspot", "hotspot3D", "nw", "particlefilter", "pathfinder", "srad", "streamcluster", 
            "2DCONV", "2MM", "3DCONV", "3MM", "ATAX", "BICG", "CORR", "COVAR", "FDTD-2D", 
            "GEMM-1MB", "GEMM-4MB", "GEMM-64MB", "GEMM-100MB", "GEMM-400MB","GEMM-900MB", "GEMM-1024MB", "GEMM-1600MB", 
            "GESUMMV", "GRAMSCHM", "MVT", "SYR2K", "SYRK"]



# all_apps = ["BN","logistic-regression","srad"]

print_options = "--trace=cuda --cuda-um-cpu-page-faults=true --cuda-um-gpu-page-faults=true --force-overwrite true "
print_file = " --output "

output_path = " /shared/uvm_bench/nsys_results/"
output_sub_path = " /shared/uvm_bench/nsys_results/"

abs_path = "/shared/uvm_bench/"


# cmd_osrt = "nsys stats --report osrt_sum --format=csv"
# cmd_mem_time = "nsys stats --report cuda_gpu_mem_time_sum --format=csv " 
# cmd_um = "nsys stats --report um_sum --format=csv "
# cmd_um_tot = "nsys stats --report um_total_sum --format=csv " 
cmd_api_trace = "nsys stats --report cuda_api_trace --format=csv "
cmd_kern_trace = "nsys stats --report cuda_gpu_trace --format=csv "
cmd_api_sum = "nsys stats --report cuda_api_sum --format=csv " 
cmd_kern_sum = "nsys stats --report cuda_gpu_kern_sum --format=csv " 
cmd_launch_queue = "nsys stats --report cuda_kern_exec_trace --format=csv "
cmd_save = " --force-export=true --output "

# change this to real nsys output file name
csv_osrt = "_osrt_sum.csv"
csv_api_sum = "_cuda_api_sum.csv"
csv_kern_sum = "_cuda_gpu_kern_sum.csv"
csv_mem_time = "_cuda_gpu_mem_time_sum.csv"
csv_um = "_um_sum.csv"
csv_um_tot = "_um_total_sum.csv"
# nsys stats --report osrt_sum --format=csv --output osrt_summary.csv report1.nsys-rep
# nsys stats --report cuda_api_sum --format=csv --output cuda_api_summary.csv report1.nsys-rep
# nsys stats --report cuda_gpu_kern_sum --format=csv --output cuda_gpu_kernel_summary.csv report1.nsys-rep
# nsys stats --report cuda_gpu_mem_time_sum --format=csv --output cuda_gpu_mem_time_summary.csv report1.nsys-rep
# nsys stats --report um_sum --format=csv --output um_summary.csv report1.nsys-rep
# nsys stats --report um_total_sum --format=csv --output um_total_summary.csv report1.nsys-rep

def profile():
    warmuped1 = False
    warmuped2 = False
    app_cnt = 0

    for UVM_flag in [False, True]:
        base_path = "UVM_benchmarks/"
        if not UVM_flag:
            base_path = "non_UVM_benchmarks/"
        
        for i, folder in enumerate(folders):
            if folder != "rodinia" and folder != "polybench":
                path = base_path + folder + "/"
                if UVM_flag:
                    command = "cd " + path + "; nsys profile " + print_options + print_file + output_path + "uvm" + "/"  + folder + "-nor-uvm"   + " " + " ./run"
                    if warmuped1 == False:
                        #warmup 5 times
                        for i in range(5):
                            print(f"[warmup] {i}")
                            warmup_command = "cd " + path +"; ./run"
                            os.system(warmup_command)
                        warmuped1 = True
                else:
                    if warmuped2 == False:
                        #warmup 5 times
                        for i in range(5):
                            print(f"[warmup] {i}")
                            warmup_command = "cd " + path +"; ./run"
                            os.system(warmup_command)
                        warmuped2 = True
                    command = "cd " + path + "; nsys profile " + print_options + print_file + output_path + "nor" + "/"  + folder + "-nor-nor"   + " " + " ./run"                
                
                print(f"{[app_cnt]} Profiling: {path}")
                os.system(command)
                print(f"{[app_cnt]} Profiling Done: {path}")
                app_cnt += 1
            elif folder == "polybench":
                for j, subfolder in enumerate(subfolders2):
                    path = base_path + folder + "/" + subfolder
                    if UVM_flag:
                        command = "cd " + path + "; nsys profile " + print_options + print_file + output_sub_path + "uvm" + "/"  + subfolder + "-nor-uvm"   + " " + " ./run"
                        if warmuped1 == False:
                            #warmup 5 times
                            for i in range(5):
                                print(f"[warmup] {i}")
                                warmup_command = "cd " + path +"; ./run"
                                os.system(warmup_command)
                            warmuped1 = True
                    else:
                        if warmuped2 == False:
                            #warmup 5 times
                            for i in range(5):
                                print(f"[warmup] {i}")
                                warmup_command = "cd " + path +"; ./run"
                                os.system(warmup_command)
                            warmuped2 = True
                        command = "cd " + path + "; nsys profile " + print_options + print_file + output_sub_path + "nor" + "/"  + subfolder + "-nor-nor"   + " " + " ./run"                
                    print(f"{[app_cnt]} Profiling: {path}")
                    os.system(command)
                    print(f"{[app_cnt]} Profiling Done: {path}")
                    app_cnt += 1
            else:
                for j, subfolder in enumerate(subfolders):
                    path = base_path + folder + "/" + subfolder
                    if UVM_flag:
                        command = "cd " + path + "; nsys profile " + print_options + print_file + output_sub_path + "uvm" + "/"  + subfolder + "-nor-uvm"   + " " + " ./run"
                        if warmuped1 == False:
                            #warmup 5 times
                            for i in range(5):
                                print(f"[warmup] {i}")
                                warmup_command = "cd " + path +"; ./run"
                                os.system(warmup_command)
                            warmuped1 = True
                    else:
                        if warmuped2 == False:
                            #warmup 5 times
                            for i in range(5):
                                print(f"[warmup] {i}")
                                warmup_command = "cd " + path +"; ./run"
                                os.system(warmup_command)
                            warmuped2 = True
                        command = "cd " + path + "; nsys profile " + print_options + print_file + output_sub_path + "nor" + "/"  + subfolder + "-nor-nor"   + " " + " ./run"                
                    print(f"{[app_cnt]} Profiling: {path}")
                    os.system(command)
                    print(f"{[app_cnt]} Profiling Done: {path}")
                    app_cnt += 1

# generate needed csv from nsys report
# the commands for nsys stats
# nsys stats --report osrt_sum --report cuda_api_sum --report cuda_gpu_kern_sum --report cuda_gpu_mem_time_sum --report um_sum --report um_total_sum --format=csv --output . xxx
# all reports are stored results/
def process_csv():
    # get file folder and file name
    csv_path2 =  "uvmbench-nsys_results/csv_queue/"

    for UVM_flag in [False,True]:
        base_path2 = "uvmbench-nsys_results/nor/"
        postfix1 = "-nor-nor"
        postfix2 = "-cc-nor"
        if UVM_flag:
            base_path2 = "uvmbench-nsys_results/uvm/"
            postfix1 = "-nor-uvm"
            postfix2 = "-cc-uvm"

        files = [postfix1, postfix2]
        for i, app in enumerate(all_apps):
            for pf in files:
                result_file = abs_path + base_path2 + app +pf+".nsys-rep"
                csv_file_base = abs_path + csv_path2 + app + pf
                # # stats_osrt_cmd = cmd_osrt + cmd_save + csv_file_base + " " + result_file         
                # stats_api_sum_cmd = cmd_api_sum + cmd_save + csv_file_base + " " + result_file
                # stats_kern_sum_cmd = cmd_kern_sum + cmd_save + csv_file_base + " " + result_file
                # stats_api_trace = cmd_api_trace + cmd_save + csv_file_base + " " + result_file
                # stats_kern_trace = cmd_kern_trace + cmd_save + csv_file_base + " " + result_file
                stats_launch_queue = cmd_launch_queue + cmd_save + csv_file_base + " " + result_file
                # os.system(stats_api_sum_cmd)
                # os.system(stats_kern_sum_cmd)
                # os.system(stats_api_trace)
                # os.system(stats_kern_trace)
                os.system(stats_launch_queue)
                print(f"{[i]} {app} {pf} Done")

if __name__ == "__main__":
    # profile()
    process_csv()