#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

long long calcWriteIndex(long long capacity, long long align, long long read_index, long long write_index, long long pkt_size);

int main() {
    long long capacity, align, read_index, write_index, pkt_size;
    if (scanf("%lld,%lld,%lld,%lld,%lld", &capacity, &align, &read_index, &write_index, &pkt_size) != 5) {
        return 0;
    }

    long long result = calcWriteIndex(capacity, align, read_index, write_index, pkt_size);
    printf("%lld\n", result);
    return 0;
}
