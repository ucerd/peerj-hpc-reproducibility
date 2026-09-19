#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>

__global__ void add(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

static void check(cudaError_t err, const char *what) {
    if (err != cudaSuccess) {
        std::fprintf(stderr, "%s: %s\n", what, cudaGetErrorString(err));
        std::exit(1);
    }
}

int main() {
    constexpr int n = 1 << 20;
    const size_t bytes = n * sizeof(float);

    float *ha = (float*)std::malloc(bytes);
    float *hb = (float*)std::malloc(bytes);
    float *hc = (float*)std::malloc(bytes);
    for (int i = 0; i < n; ++i) { ha[i] = 1.0f; hb[i] = 2.0f; }

    float *da = nullptr, *db = nullptr, *dc = nullptr;
    check(cudaMalloc(&da, bytes), "cudaMalloc a");
    check(cudaMalloc(&db, bytes), "cudaMalloc b");
    check(cudaMalloc(&dc, bytes), "cudaMalloc c");
    check(cudaMemcpy(da, ha, bytes, cudaMemcpyHostToDevice), "copy a");
    check(cudaMemcpy(db, hb, bytes, cudaMemcpyHostToDevice), "copy b");

    const int threads = 256;
    const int blocks = (n + threads - 1) / threads;
    add<<<blocks, threads>>>(da, db, dc, n);
    check(cudaGetLastError(), "kernel launch");
    check(cudaDeviceSynchronize(), "kernel execution");
    check(cudaMemcpy(hc, dc, bytes, cudaMemcpyDeviceToHost), "copy c");

    std::printf("c[0]=%.1f expected=3.0\n", hc[0]);

    cudaFree(da); cudaFree(db); cudaFree(dc);
    std::free(ha); std::free(hb); std::free(hc);
    return hc[0] == 3.0f ? 0 : 2;
}
