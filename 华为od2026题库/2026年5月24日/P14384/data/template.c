#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000

int countFailedCharging(int n, int** cars, int carsSize);

static int** parseCars(const char* s, int* outSize) {
    int** res = (int**)malloc(1000 * sizeof(int*));
    *outSize = 0;
    const char* p = s;
    while (*p && *p != '[') p++;
    if (!*p) return res;
    p++; 
    while (*p) {
        if (*p == '[') {
            p++;
            int arr[3], idx = 0;
            while (*p && *p != ']') {
                char numbuf[50];
                int ni = 0;
                while (*p && ((*p >= '0' && *p <= '9') || *p == '-')) {
                    numbuf[ni++] = *p;
                    p++;
                }
                numbuf[ni] = '\0';
                if (ni > 0) {
                    arr[idx++] = atoi(numbuf);
                }
                if (*p == ',') p++;
            }
            if (*p == ']') p++;
            res[*outSize] = (int*)malloc(3 * sizeof(int));
            for (int i = 0; i < 3; i++) res[*outSize][i] = arr[i];
            (*outSize)++;
        } else {
            p++;
        }
    }
    return res;
}

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    int n, m;
    const char* p = line;
    n = atoi(p);
    while (*p && *p != ',') p++;
    if (*p == ',') p++;
    m = atoi(p);
    while (*p && *p != '[') p++;

    int carsSize;
    int** cars = parseCars(p, &carsSize);

    int result = countFailedCharging(n, cars, carsSize);
    printf("%d\n", result);

    for (int i = 0; i < carsSize; i++) free(cars[i]);
    free(cars);
    return 0;
}
