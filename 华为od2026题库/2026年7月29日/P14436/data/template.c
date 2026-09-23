#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 100000

int* energyCollision(int* energies, int energiesSize, int* returnSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 查找第一个逗号（分割 n 和数组）
    int comma = 0;
    while (line[comma] && line[comma] != ',') comma++;

    // 解析 n
    char nStr[16];
    strncpy(nStr, line, comma);
    nStr[comma] = '\0';
    int n = atoi(nStr);

    // 解析数组 [a1,a2,...,an]
    int* energies = (int*)malloc(n * sizeof(int));
    int eSize = 0;
    char* p = line + comma + 1;
    while (*p && *p != '[') p++;
    if (*p == '[') p++;

    char num[16];
    int numLen = 0;
    while (*p) {
        if (*p == ',' || *p == ']') {
            if (numLen > 0) {
                num[numLen] = '\0';
                energies[eSize++] = atoi(num);
                numLen = 0;
            }
            if (*p == ']') break;
        } else {
            num[numLen++] = *p;
        }
        p++;
    }

    int returnSize;
    int* result = energyCollision(energies, eSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("%d", result[i]);
    }
    printf("]\n");

    free(energies);
    free(result);
    free(line);

    return 0;
}
