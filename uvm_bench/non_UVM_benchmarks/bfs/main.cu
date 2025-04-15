#include <cstdio>
#include <cuda.h>
#include <cuda_runtime.h>
#include <string>
#include <cstring>
#include <iostream>
#include "graph.h"
#include "bfsCPU.h"
#include "bfsCUDA.cuh"

#include "../../common/file_op.h"

void runCpu(int startVertex, Graph &G, std::vector<int> &distance,
            std::vector<int> &parent, std::vector<bool> &visited) {
    printf("Starting sequential bfs.\n");
    auto start = std::chrono::steady_clock::now();
    bfsCPU(startVertex, G, distance, parent, visited);
    auto end = std::chrono::steady_clock::now();
    long duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    printf("Elapsed time in milliseconds : %li ms.\n\n", duration);
}


#define checkError(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true)
{
   if (code != cudaSuccess) 
   {
      fprintf(stderr,"GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
      if (abort) exit(code);
   }

}

int *d_adjacencyList;
int *d_edgesOffset;
int *d_edgesSize;
int *d_distance;
int *d_parent;
int *d_currentQueue;
int *d_nextQueue;
int *d_degrees;

int *incrDegrees;

// shared for all
float bt_malloc;
float bt_memcpy_h2d;
float bt_free;
float bt_memset;

// per kernel
float bt_malloc_simple;
float bt_memcpy_h2d_simple;
float bt_lauch_simple;
float bt_kernel_simple;
float bt_memcpy_d2h_simple;

float bt_malloc_queue;
float bt_memcpy_h2d_queue;
float bt_lauch_queue;
float bt_kernel_queue;
float bt_memcpy_d2h_queue;

float bt_malloc_scan;
float bt_memcpy_h2d_scan;
float bt_lauch_scan;
float bt_kernel_scan;
float bt_memcpy_d2h_scan;




void initCuda(Graph &G) {

    // checkError(cudaMalloc((void **)&d_adjacencyList, G.numEdges * sizeof(int) ));
    // checkError(cudaMalloc((void **)&d_edgesOffset, G.numVertices * sizeof(int) ));
    // checkError(cudaMalloc((void **)&d_edgesSize, G.numVertices * sizeof(int)) );
    // checkError(cudaMalloc((void **)&d_distance, G.numVertices * sizeof(int) ));
    // checkError(cudaMalloc((void **)&d_parent, G.numVertices * sizeof(int) ));
    // checkError(cudaMalloc((void **)&d_currentQueue, G.numVertices * sizeof(int) ));
    // checkError(cudaMalloc((void **)&d_nextQueue, G.numVertices * sizeof(int) ));
    // checkError(cudaMalloc((void **)&d_degrees, G.numVertices * sizeof(int) ));
    // checkError(cudaMallocHost((void **) &incrDegrees, sizeof(int) * G.numVertices));
    // checkError(cudaMemcpy(d_adjacencyList, G.adjacencyList.data(), G.numEdges * sizeof(int), cudaMemcpyHostToDevice));
    // checkError(cudaMemcpy(d_edgesOffset, G.edgesOffset.data(), G.numVertices * sizeof(int), cudaMemcpyHostToDevice));
    // checkError(cudaMemcpy(d_edgesSize, G.edgesSize.data(), G.numVertices * sizeof(int), cudaMemcpyHostToDevice ));
    clock_t t1 = clock();
    cudaMalloc((void **)&d_adjacencyList, G.numEdges * sizeof(int) );
    cudaMalloc((void **)&d_edgesOffset, G.numVertices * sizeof(int) );
    cudaMalloc((void **)&d_edgesSize, G.numVertices * sizeof(int)) ;
    cudaMalloc((void **)&d_distance, G.numVertices * sizeof(int) );
    cudaMalloc((void **)&d_parent, G.numVertices * sizeof(int) );
    cudaMalloc((void **)&d_currentQueue, G.numVertices * sizeof(int) );
    cudaMalloc((void **)&d_nextQueue, G.numVertices * sizeof(int) );
    cudaMalloc((void **)&d_degrees, G.numVertices * sizeof(int) );
    clock_t t2 = clock();
    cudaMallocHost((void **) &incrDegrees, sizeof(int) * G.numVertices);

    clock_t t3 = clock();
    cudaMemcpy(d_adjacencyList, G.adjacencyList.data(), G.numEdges * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_edgesOffset, G.edgesOffset.data(), G.numVertices * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_edgesSize, G.edgesSize.data(), G.numVertices * sizeof(int), cudaMemcpyHostToDevice );
    clock_t t4 = clock();

    // shared for all
    bt_malloc = (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_memcpy_h2d = (float)(t4 - t3) / CLOCKS_PER_SEC;

    // per kernel
    bt_malloc_simple += bt_malloc;
    bt_memcpy_h2d_simple += bt_memcpy_h2d;

    bt_malloc_queue += bt_malloc;
    bt_memcpy_h2d_queue += bt_memcpy_h2d;
    
    bt_malloc_scan += bt_malloc;
    bt_memcpy_h2d_scan += bt_memcpy_h2d;


}

void finalizeCuda() {
    clock_t t1 = clock();
    cudaFree(d_adjacencyList);
    cudaFree(d_edgesOffset);
    cudaFree(d_edgesSize);
    cudaFree(d_distance);
    cudaFree(d_parent);
    cudaFree(d_currentQueue);
    cudaFree(d_nextQueue);
    cudaFree(d_degrees);
    clock_t t2 = clock();
    cudaFreeHost(incrDegrees);
    bt_free = (float)(t2 - t1) / CLOCKS_PER_SEC;
}



void checkOutput(std::vector<int> &distance, std::vector<int> &expectedDistance, Graph &G) {
    for (int i = 0; i < G.numVertices; i++) {
        if (distance[i] != expectedDistance[i]) {
            printf("%d %d %d\n", i, distance[i], expectedDistance[i]);
            printf("Wrong output!\n");
            exit(1);
        }
    }

    printf("Output OK!\n\n");
}


void initializeCudaBfs(int startVertex, std::vector<int> &distance, std::vector<int> &parent, Graph &G) {
    //initialize values
    std::fill(distance.begin(), distance.end(), std::numeric_limits<int>::max());
    std::fill(parent.begin(), parent.end(), std::numeric_limits<int>::max());
    distance[startVertex] = 0;
    parent[startVertex] = 0;

    clock_t t1 = clock();
    cudaMemcpy(d_distance, distance.data(), G.numVertices * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_parent, parent.data(), G.numVertices * sizeof(int), cudaMemcpyHostToDevice);
    int firstElementQueue = startVertex;
    cudaMemcpy(d_currentQueue, &firstElementQueue, sizeof(int), cudaMemcpyHostToDevice);
    clock_t t2 = clock();
    // bt_memcpy_h2d = (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_memcpy_h2d_simple += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_memcpy_h2d_queue += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_memcpy_h2d_scan += (float)(t2 - t1) / CLOCKS_PER_SEC;
}

void finalizeCudaBfs(std::vector<int> &distance, std::vector<int> &parent, Graph &G) {
    //copy memory from device
    clock_t t1 = clock();
    cudaMemcpy(distance.data(), d_distance, G.numVertices * sizeof(int), cudaMemcpyDeviceToHost);
    cudaMemcpy(parent.data(), d_parent, G.numVertices * sizeof(int), cudaMemcpyDeviceToHost);
    clock_t t2 = clock();
    // bt_memcpy_d2h = (float)(t2 - t1) / CLOCKS_PER_SEC;

    bt_memcpy_d2h_simple += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_memcpy_d2h_queue += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_memcpy_d2h_scan += (float)(t2 - t1) / CLOCKS_PER_SEC;
}

// gpu
void runCudaSimpleBfs(int startVertex, Graph &G, std::vector<int> &distance,
                      std::vector<int> &parent) {
    
    initializeCudaBfs(startVertex, distance, parent, G);


    int *changed;
    checkError(cudaMallocHost((void **) &changed, sizeof(int)));

    //launch kernel
    printf("Starting simple parallel bfs.\n");
    
    clock_t start_time = clock();
    *changed = 1;
    int level = 0;
    while (*changed) {
        *changed = 0;
        clock_t t1 = clock();
        simpleBfs<<<G.numVertices / 1024 + 1, 1024>>>(G.numVertices, level, d_adjacencyList, d_edgesOffset, d_edgesSize, d_distance, d_parent, changed);                 
        clock_t t2 = clock();
        cudaDeviceSynchronize();
        clock_t t3 = clock();
        level++;
        
        bt_lauch_simple += (float)(t2 - t1) / CLOCKS_PER_SEC;
        bt_kernel_simple += (float)(t3 - t2) / CLOCKS_PER_SEC;
    }
    clock_t end_time = clock();
    float duration = (float)(end_time - start_time) / CLOCKS_PER_SEC;
    
    printf("Elapsed time in : %f s.\n", duration);
    printf("My time in : %f s.\n", bt_kernel_simple + bt_lauch_simple);

    // FILE * fp = fopen("/shared/uvm_bench/log/simple-bfs.txt", "a");
	// if (fp == NULL) {
	// 	fprintf(stderr, "Error opening file!\n");
	// 	exit(1);
	// }
	// fprintf(fp, "%f\n", duration);
    // fclose(fp);
    finalizeCudaBfs(distance, parent, G);
}

// gpu
void runCudaQueueBfs(int startVertex, Graph &G, std::vector<int> &distance,
    std::vector<int> &parent) {
    initializeCudaBfs(startVertex, distance, parent, G);

    int *nextQueueSize;
    checkError(cudaMallocHost((void **)&nextQueueSize, sizeof(int)));
    //launch kernel
    printf("Starting queue parallel bfs.\n");

    clock_t start_time = clock();
    int queueSize = 1;
    *nextQueueSize = 0;
    int level = 0;
    while (queueSize) {
        clock_t t1 = clock();
        queueBfs<<<queueSize / 1024 + 1, 1024>>>(level, d_adjacencyList, d_edgesOffset, d_edgesSize, d_distance, d_parent, queueSize,
                                                nextQueueSize, d_currentQueue, d_nextQueue);
        clock_t t2 = clock();
        cudaDeviceSynchronize();
        clock_t t3 = clock();
        level++;
        queueSize = *nextQueueSize;
        *nextQueueSize = 0;
        std::swap(d_currentQueue, d_nextQueue);

        bt_lauch_queue += (float)(t2 - t1) / CLOCKS_PER_SEC;
        bt_kernel_queue += (float)(t3 - t2) / CLOCKS_PER_SEC;
    }
    clock_t end_time = clock();
    float duration = (float)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Elapsed time : %f s.\n", duration);
    printf("My time in : %f s.\n", bt_kernel_queue + bt_lauch_queue);

    // FILE * fp = fopen("/shared/uvm_bench/log/queue-bfs.txt", "a");
	// if (fp == NULL) {
	// 	fprintf(stderr, "Error opening file!\n");
	// 	exit(1);
	// }
	// fprintf(fp, "%f\n", duration);
    // fclose(fp);
    finalizeCudaBfs(distance, parent, G);
}

void nextLayer(int level, int queueSize) {
    clock_t t1 = clock();
    nextLayer<<<queueSize / 1024 + 1, 1024>>>(level, d_adjacencyList, d_edgesOffset, d_edgesSize, d_distance, d_parent, queueSize,
                                            d_currentQueue);
    clock_t t2 = clock();
    cudaDeviceSynchronize();
    clock_t t3 = clock();

    bt_lauch_scan += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_kernel_scan += (float)(t3 - t2) / CLOCKS_PER_SEC;
}

void countDegrees(int level, int queueSize) {
    clock_t t1 = clock();
    countDegrees<<<queueSize / 1024 + 1, 1024>>>(d_adjacencyList, d_edgesOffset, d_edgesSize, d_parent, queueSize,
        d_currentQueue, d_degrees);
    clock_t t2 = clock();
    cudaDeviceSynchronize();
    clock_t t3 = clock();

    bt_lauch_scan += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_kernel_scan += (float)(t3 - t2) / CLOCKS_PER_SEC;

}

void scanDegrees(int queueSize) {
//run kernel so every block in d_currentQueue has prefix sums calculated
    clock_t t1 = clock();
    scanDegrees<<<queueSize / 1024 + 1, 1024>>>(queueSize, d_degrees, incrDegrees);
    clock_t t2 = clock();
    cudaDeviceSynchronize();
    clock_t t3 = clock();

    bt_lauch_scan += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_kernel_scan += (float)(t3 - t2) / CLOCKS_PER_SEC;

    //count prefix sums on CPU for ends of blocks exclusive
    //already written previous block sum
    incrDegrees[0] = 0;
    for (int i = 1024; i < queueSize + 1024; i += 1024) {
        incrDegrees[i / 1024] += incrDegrees[i / 1024 - 1];
    }
}

void assignVerticesNextQueue(int queueSize, int nextQueueSize) {
    clock_t t1 = clock();
    assignVerticesNextQueue<<<queueSize / 1024 + 1, 1024>>>(d_adjacencyList, d_edgesOffset, d_edgesSize, d_parent, queueSize, d_currentQueue,
        d_nextQueue, d_degrees, incrDegrees, nextQueueSize);
    clock_t t2 = clock();
    cudaDeviceSynchronize();
    clock_t t3 = clock();

    bt_lauch_scan += (float)(t2 - t1) / CLOCKS_PER_SEC;
    bt_kernel_scan += (float)(t3 - t2) / CLOCKS_PER_SEC;
}

// gpu
void runCudaScanBfs(int startVertex, Graph &G, std::vector<int> &distance,
   std::vector<int> &parent) {
    initializeCudaBfs(startVertex, distance, parent, G);

    //launch kernel
    printf("Starting scan parallel bfs.\n");

    clock_t start_time = clock();
    int queueSize = 1;
    int nextQueueSize = 0;
    int level = 0;
    while (queueSize) {
        // next layer phase
        nextLayer(level, queueSize);
        // counting degrees phase
        countDegrees(level, queueSize);
        // doing scan on degrees
        scanDegrees(queueSize);
        nextQueueSize = incrDegrees[(queueSize - 1) / 1024 + 1];
        // assigning vertices to nextQueue
        assignVerticesNextQueue(queueSize, nextQueueSize);

        level++;
        queueSize = nextQueueSize;
        std::swap(d_currentQueue, d_nextQueue);
    }

    clock_t end_time = clock();
    float duration = (float)(end_time - start_time) / CLOCKS_PER_SEC;
   
    printf("Elapsed time: %f s.\n", duration);
    printf("My time in : %f s.\n", bt_kernel_scan + bt_lauch_scan);

    // FILE * fp = fopen("/shared/uvm_bench/log/scan-bfs.txt", "a");
	// if (fp == NULL) {
	// 	fprintf(stderr, "Error opening file!\n");
	// 	exit(1);
	// }
	// fprintf(fp, "%f\n", duration);
    // fclose(fp);


    finalizeCudaBfs(distance, parent, G);
}


int main(int argc, char **argv) {

    // read graph from standard input
    Graph G;
    int startVertex = atoi(argv[1]);
    readGraph(G, argc, argv);

    printf("Number of vertices %d\n", G.numVertices);
    printf("Number of edges %d\n\n", G.numEdges);

    //vectors for results
    std::vector<int> distance(G.numVertices, std::numeric_limits<int>::max());
    std::vector<int> parent(G.numVertices, std::numeric_limits<int>::max());
    std::vector<bool> visited(G.numVertices, false);

    //run CPU sequential bfs
    runCpu(startVertex, G, distance, parent, visited);

    //save results from sequential bfs
    std::vector<int> expectedDistance(distance);
    std::vector<int> expectedParent(parent);
   
    auto start = std::chrono::steady_clock::now();
    initCuda(G);
    //run CUDA simple parallel bfs
    runCudaSimpleBfs(startVertex, G, distance, parent);
    checkOutput(distance, expectedDistance, G);
    std::cout << distance[0] << std::endl;

    // // //run CUDA scan parallel bfs
    runCudaScanBfs(startVertex, G, distance, parent);
    //checkOutput(distance, expectedDistance, G);
    std::cout << distance[0] << std::endl;

    finalizeCuda();

	save_log("simple-bfs", "nor-brk", NULL, "%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\n", bt_malloc_simple, bt_memcpy_h2d_simple, bt_lauch_simple, bt_kernel_simple, bt_memcpy_d2h_simple, bt_free, bt_memset);
	save_log("queue-bfs", "nor-brk", NULL, "%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\n", bt_malloc_queue, bt_memcpy_h2d_queue, bt_lauch_queue, bt_kernel_queue, bt_memcpy_d2h_queue, bt_free, bt_memset);
	save_log("scan-bfs", "nor-brk", NULL, "%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\n", bt_malloc_scan, bt_memcpy_h2d_scan, bt_lauch_scan, bt_kernel_scan, bt_memcpy_d2h_scan, bt_free, bt_memset);
    

    auto end = std::chrono::steady_clock::now();
    long duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    printf("Overall Elapsed time in milliseconds : %li ms.\n", duration);
    return 0;
}


