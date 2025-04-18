
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <cuda.h>

#include "../../../common/polybenchUtilFuncts.h"

//define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.5

#define GPU_DEVICE 0

/* Problem size */
#define NI 256
#define NJ 256
#define NK 256

/* Thread block dimensions */
#define DIM_THREAD_BLOCK_X 32
#define DIM_THREAD_BLOCK_Y 8

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;



void conv3D(DATA_TYPE* A, DATA_TYPE* B)
{
        int i, j, k;
        DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

        c11 = +2;  c21 = +5;  c31 = -8;
        c12 = -3;  c22 = +6;  c32 = -9;
        c13 = +4;  c23 = +7;  c33 = +10;


        for (i = 1; i < NI - 1; ++i) // 0
        {
                for (j = 1; j < NJ - 1; ++j) // 1
                {
                        for (k = 1; k < NK -1; ++k) // 2
                        {
                                //printf("i:%d\nj:%d\nk:%d\n", i, j, k);
                                B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                             +   c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                             +   c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                             +   c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]  +  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]   
                                             +   c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]  +  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  
                                             +   c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  +  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  
                                             +   c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]  
                                             +   c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
                        }
                }
        }
}


void init(DATA_TYPE* A)
{
        int i, j, k;

        for (i = 0; i < NI; ++i)
        {
                for (j = 0; j < NJ; ++j)
                {
                        for (k = 0; k < NK; ++k)
                        {
                                A[i*(NK * NJ) + j*NK + k] = i % 12 + 2 * (j % 7) + 3 * (k % 13);
                        }
                }
        }
}


void compareResults(DATA_TYPE* B, DATA_TYPE* B_outputFromGpu)
{
        int i, j, k, fail;
        fail = 0;

        // Compare result from cpu and gpu...
        for (i = 1; i < NI - 1; ++i) // 0
        {
                for (j = 1; j < NJ - 1; ++j) // 1
                {
                        for (k = 1; k < NK - 1; ++k) // 2
                        {
                                if (percentDiff(B[i*(NK * NJ) + j*NK + k], B_outputFromGpu[i*(NK * NJ) + j*NK + k]) > PERCENT_DIFF_ERROR_THRESHOLD)
                                {
                                        fail++;
                                }
                        }
                }
        }

        // Print results
        printf("Non-Matching CPU-GPU Outputs Beyond Error Threshold of %4.2f Percent: %d\n", PERCENT_DIFF_ERROR_THRESHOLD, fail);
}


void GPU_argv_init()
{
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, GPU_DEVICE);
        printf("setting device %d with name %s\n",GPU_DEVICE,deviceProp.name);
        cudaSetDevice( GPU_DEVICE );
}


__global__ void convolution3D_kernel_fused_1(DATA_TYPE *A, DATA_TYPE *B)
{
        int k = blockIdx.x * blockDim.x + threadIdx.x;
        int j = blockIdx.y * blockDim.y + threadIdx.y;
        int i = blockIdx.z * blockDim.z + threadIdx.z;
        DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

        c11 = +2;  c21 = +5;  c31 = -8;
        c12 = -3;  c22 = +6;  c32 = -9;
        c13 = +4;  c23 = +7;  c33 = +10;
        
        if ((j < (NJ-1)) &&  (k < (NK-1))){
                // #pragma unroll 128
                for (int i = 1; i <= 64; ++i){
                        B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]  +  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]   
                                        +   c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]  +  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  
                                        +   c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  +  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  
                                        +   c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]  
                                        +   c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
                }
        }
}

__global__ void convolution3D_kernel_fused_3(DATA_TYPE *A, DATA_TYPE *B)
{
        int k = blockIdx.x * blockDim.x + threadIdx.x;
        int j = blockIdx.y * blockDim.y + threadIdx.y;
        int i = blockIdx.z * blockDim.z + threadIdx.z;
        DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

        c11 = +2;  c21 = +5;  c31 = -8;
        c12 = -3;  c22 = +6;  c32 = -9;
        c13 = +4;  c23 = +7;  c33 = +10;
        
        if ((j < (NJ-1)) &&  (k < (NK-1))){
                // #pragma unroll 128
                for (int i = 64; i <=128; ++i){
                        B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]  +  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]   
                                        +   c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]  +  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  
                                        +   c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  +  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  
                                        +   c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]  
                                        +   c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
                }
        }
}

__global__ void convolution3D_kernel_fused_2(DATA_TYPE *A, DATA_TYPE *B)
{
        int k = blockIdx.x * blockDim.x + threadIdx.x;
        int j = blockIdx.y * blockDim.y + threadIdx.y;
        int i = blockIdx.z * blockDim.z + threadIdx.z;
        DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

        c11 = +2;  c21 = +5;  c31 = -8;
        c12 = -3;  c22 = +6;  c32 = -9;
        c13 = +4;  c23 = +7;  c33 = +10;
        
        if ((j < (NJ-1)) &&  (k < (NK-1))){
                // #pragma unroll 128
                for (int i = 128; i <= 192; ++i){
                        B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]  +  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]   
                                        +   c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]  +  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  
                                        +   c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  +  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  
                                        +   c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]  
                                        +   c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
                }
        }
}

__global__ void convolution3D_kernel_fused_4(DATA_TYPE *A, DATA_TYPE *B)
{
        int k = blockIdx.x * blockDim.x + threadIdx.x;
        int j = blockIdx.y * blockDim.y + threadIdx.y;
        int i = blockIdx.z * blockDim.z + threadIdx.z;
        DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

        c11 = +2;  c21 = +5;  c31 = -8;
        c12 = -3;  c22 = +6;  c32 = -9;
        c13 = +4;  c23 = +7;  c33 = +10;
        
        if ((j < (NJ-1)) &&  (k < (NK-1))){
                // #pragma unroll 128
                for (int i = 192; i < NI - 1; ++i){
                        B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
                                        +   c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]  +  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]   
                                        +   c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]  +  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  
                                        +   c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  +  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  
                                        +   c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]  
                                        +   c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
                }
        }
}


void convolution3DCuda(DATA_TYPE* A, DATA_TYPE* B, DATA_TYPE* B_outputFromGpu)
{
        double t_start, t_end, tl1;

        DATA_TYPE *A_gpu;
        DATA_TYPE *B_gpu;


        double t_malloc_s = rtclock();
        cudaMalloc((void **)&A_gpu, sizeof(DATA_TYPE) * NI * NJ * NK);
        cudaMalloc((void **)&B_gpu, sizeof(DATA_TYPE) * NI * NJ * NK);
        double t_malloc_e = rtclock();
        cudaMemcpy(A_gpu, A, sizeof(DATA_TYPE) * NI * NJ * NK, cudaMemcpyHostToDevice);
        cudaMemcpy(B_gpu, B, sizeof(DATA_TYPE) * NI * NJ * NK, cudaMemcpyHostToDevice);
        double t_memcpy_h2d = rtclock();

        dim3 block(DIM_THREAD_BLOCK_X, DIM_THREAD_BLOCK_Y);
        dim3 grid((size_t)(ceil( ((float)NK) / ((float)block.x) )), (size_t)(ceil( ((float)NJ) / ((float)block.y) )));

        convolution3D_kernel_fused_1<<< grid, block >>>(A_gpu, B_gpu);
        convolution3D_kernel_fused_2<<< grid, block >>>(A_gpu, B_gpu);
        convolution3D_kernel_fused_3<<< grid, block >>>(A_gpu, B_gpu);
        convolution3D_kernel_fused_4<<< grid, block >>>(A_gpu, B_gpu);
        cudaDeviceSynchronize();
        // fprintf(stdout, "GPU Runtime: %0.6lfs\n", t_end - t_start);
        // save_log(__FILE__,"nor",NULL, "%0.6lf\n", t_end - t_start);
        cudaMemcpy(B_outputFromGpu, B_gpu, sizeof(DATA_TYPE) * NI * NJ * NK, cudaMemcpyDeviceToHost);
        cudaFree(A_gpu);
        cudaFree(B_gpu);
       printf("B[0] = %f\n", B_outputFromGpu[0]);
}


int main(int argc, char *argv[])
{
        double t_start, t_end;

        DATA_TYPE* A;
        DATA_TYPE* B;
        DATA_TYPE* B_outputFromGpu;

        // A = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));
        // B = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));
        // B_outputFromGpu = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));
        cudaMallocHost((void **)&A,NI*NJ*NK*sizeof(DATA_TYPE));
        cudaMallocHost((void **)&B,NI*NJ*NK*sizeof(DATA_TYPE));
        cudaMallocHost((void **)&B_outputFromGpu,NI*NJ*NK*sizeof(DATA_TYPE));

        init(A);

        GPU_argv_init();

        convolution3DCuda(A, B, B_outputFromGpu);

        // t_start = rtclock();
        // conv3D(A, B);
        // t_end = rtclock();
        // fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);

        // compareResults(B, B_outputFromGpu);

        printf("B[0] = %f\n", B_outputFromGpu[0]);

        cudaFree(A);
        cudaFree(B);
        cudaFree(B_outputFromGpu);

        return 0;
}


