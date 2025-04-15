#!/bin/bash

# Define an array of executables
executables=(

"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_data_thread_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_data_warp_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_topo_atomic"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_topo_frontier"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_topo_thread_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_topo_unroll"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BFS/bfs_topo_warp_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_BetweennessCentr/betweenness"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_ConnectedComp/connected_comp"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_DegreeCentr/degree_centr"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_GraphColoring/gc_data_thread_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_GraphColoring/gc_data_warp_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_GraphColoring/gc_topo_thread_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_GraphColoring/gc_topo_warp_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_SSSP/sssp_data_thread_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_SSSP/sssp_data_warp_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_SSSP/sssp_topo_thread_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_SSSP/sssp_topo_warp_centric"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_TriangleCount/triangle_count"
"/p/confidentialgpu/graphBIG/gpu_bench/gpu_kCore/kcore"

)

export CUDA_VISIBLE_DEVICES=0

# Loop through each executable and run it 15 times
for exe in "${executables[@]}"; do
    for i in {1..20}; do
        eval "$exe"
    done
done

