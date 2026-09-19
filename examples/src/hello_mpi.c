#include <mpi.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char **argv) {
    int rank = 0, size = 0;
    char host[256] = {0};

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    gethostname(host, sizeof(host) - 1);

    printf("rank=%d size=%d host=%s\n", rank, size, host);

    MPI_Finalize();
    return 0;
}
