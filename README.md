# Code and Scripts for ISPASS '25 Paper  

**Paper Title:** *Dissecting Performance Overheads of Confidential Computing on GPU-based Systems*  

## Generating Figures (Fig. 3 – Fig. 13)  
To generate a specific figure, use the following command:  

```sh
# Replace 'x' with the desired figure number
# Ensure the file paths within each script are correctly set
# Raw and processed data are available within each corresponding folder
cd figx/; python figx.py
```

Processed data is provided in each folder. Additionally, scripts for collecting raw data are available in their respective directories.

## Guidelines  

### Collecting Performance CSVs  
Nsight System reports can be exported in CSV format. Refer to the **Benchmarks** section for further details. A full run may require over **500GB of disk storage** and **more than one week** to complete. The same code can be executed under either **TD** or a **normal VM**.

### Figure Details  

#### **Fig. 3**  
- **Bandwidth (BW):** The `bandwidthTest` benchmark from `cuda-samples` is used. Run the `run-bw.sh` script under both **VM** and **TD** environments.  
- **Crypto-TH:** OpenSSL is used. The `openssl.sh` script can be executed to collect results.

#### **Fig. 4**  
- Data is collected from the `_cuda_gpu_trace.csv` file in the Nsight report.  
- The following fields are extracted for **data movement operations**:  
  `["Duration (ns)", "Bytes (MB)", "Throughput (MB/s)", "SrcMemKd", "DstMemKd", "Name"]`

#### **Fig. 5**  
- Data is collected from `_cuda_api_sum.csv`.  
- The following CUDA API calls are analyzed:  
  `["cudaMalloc", "cudaMallocHost", "cudaFree"]`  
- The total execution time of each API is measured.

#### **Fig. 6**  
- Data is collected from `_cuda_kern_exec_trace.csv`.  
- The following fields are extracted:  
  `["API Start (ns)", "API Dur (ns)", "Queue Dur (ns)"]`

#### **Fig. 7**  
- Example **flame graphs** are provided.  
- Use `grep` to search for the elements included in Fig. 7 to view the corresponding stack traces.

#### **Fig. 8**  
- Data is collected from both `_cuda_api_trace.csv` and `_cuda_gpu_trace.csv`.

#### **Fig. 9**  
- Data is collected from `_cuda_gpu_kern_sum.csv`.  
- The **"Total Time (ns)"** field is analyzed.

#### **Fig. 10**  
- Data is collected from both `_cuda_api_trace.csv` and `_cuda_gpu_trace.csv`.

#### **Fig. 11**  
- Processed data is provided.  
- The micro-benchmark code is described in the paper.

#### **Fig. 12**  
- Code for **DNN training** is provided in the relevant directory.  
- Processed training logs are included.

#### **Fig. 13**  
- Follow the official setup instructions for **vLLM** and **Hugging Face**.

## Benchmarks  
This repository includes benchmark code for:  
- `uvm_bench`  
- `graphBIG`  
- `DNNs`  

Profiling and data processing scripts are available within their respective directories.

## System Setup Scripts  
The repository contains various scripts for system setup, including:  

1. Locking CPU frequency  
2. Disabling hyperthreading  
3. Disabling NUMA balancing  
4. Checking GPU IRQs  
5. Unloading DRM  
6. Checking IOMMU status  
7. Unbinding the GPU PCI driver  
8. Unbinding the GPU VFIO driver  
9. Configuring **TD launch** settings  
10. Configuring **GPU operating modes**  

## Steps for Launching TD  
If the GPU needs to be **passed through** to a **TD**, always unbind the PCI driver first.

## Building the TDX Kernel  
The TDX tools used in our setup are included. A **Dockerfile** is provided to facilitate the creation of a suitable build environment.

## Citation  
If you use this work, please cite the following:

```
@inproceedings{yang2025confidentialgpu,
  title = {Dissecting Performance Overheads of Confidential Computing on GPU-based Systems},
  author = {Yang, Yang and Sonji, Mohammad and Jog, Adwait},
  booktitle = {Proceedings of the IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS)},
  year = {2025},
  note = {To appear}
}
```