#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2000000
#define MAX_N 100000

int* StatPortRates(int* portRates, int portRatesSize, int* returnSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int* arr = (int*)malloc(MAX_N * sizeof(int));
    int n = 0;
    int i = 0;
    while (line[i] && line[i] != '[') i++;
    i++;
    char numbuf[50];
    int nb = 0;
    while (line[i] && line[i] != ']') {
        char c = line[i];
        if ((c >= '0' && c <= '9') || c == '-') {
            numbuf[nb++] = c;
        } else if (c == ',' || c == ' ') {
            if (nb > 0) {
                numbuf[nb] = '\0';
                arr[n++] = atoi(numbuf);
                nb = 0;
            }
        }
        i++;
    }
    if (nb > 0) {
        numbuf[nb] = '\0';
        arr[n++] = atoi(numbuf);
    }

    int returnSize = 0;
    int* res = StatPortRates(arr, n, &returnSize);

    printf("[");
    for (int j = 0; j < returnSize; j++) {
        printf("%d", res[j]);
        if (j < returnSize - 1) printf(",");
    }
    printf("]\n");

    free(arr);
    free(res);
    free(line);
    return 0;
}
