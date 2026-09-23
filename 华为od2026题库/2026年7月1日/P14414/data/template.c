#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 200000

int main() {
    char input[MAX_LEN];
    if (!fgets(input, MAX_LEN, stdin)) return 0;
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';

    int N, K, M;
    char *p = input;
    sscanf(p, "%d,%d,%d", &N, &K, &M);

    // find the '['
    char *arrStart = strchr(input, '[');
    if (!arrStart) return 0;
    arrStart++;
    char *arrEnd = strchr(arrStart, ']');
    if (!arrEnd) return 0;

    int *A = (int*)malloc(sizeof(int) * N);
    int idx = 0;
    char *token = strtok(arrStart, ",]");
    while (token && idx < N) {
        A[idx++] = atoi(token);
        token = strtok(NULL, ",]");
    }

    long long result = maxSpiritPower(N, K, M, A);
    printf("%lld\n", result);

    free(A);
    return 0;
}
