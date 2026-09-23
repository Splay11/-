#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_LEN 100000
#define MAX_TOKENS 1000

static int** parseIntMatrix(const char* s, int* outCount) {
    int** res = (int**)malloc(MAX_TOKENS * sizeof(int*));
    *outCount = 0;
    int curRow[3];
    int curIndex = 0;
    int num = 0;
    bool inNum = false;
    bool neg = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') {
            neg = true;
            inNum = true;
            num = 0;
        } else if (isdigit((unsigned char)c)) {
            num = num * 10 + (c - '0');
            inNum = true;
        } else if (inNum && (c == ',' || c == ']')) {
            curRow[curIndex++] = neg ? -num : num;
            num = 0;
            neg = false;
            inNum = false;
            if (c == ']' && curIndex == 3) {
                res[*outCount] = (int*)malloc(3 * sizeof(int));
                for (int j = 0; j < 3; j++) res[*outCount][j] = curRow[j];
                (*outCount)++;
                curIndex = 0;
            }
        }
    }
    return res;
}

int* predictGeneration(int** sub_arrays, int subArraysSize, int station_capacity, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    int bracketEnd = -1;
    for (int i = 0; i < len; i++) {
        if (line[i] == ']') bracketEnd = i;
    }

    char arrStr[MAX_LEN];
    strncpy(arrStr, line, bracketEnd + 1);
    arrStr[bracketEnd + 1] = '\0';
    const char* after = line + bracketEnd + 2;
    int station_capacity = atoi(after);

    int subArraysSize;
    int** sub_arrays = parseIntMatrix(arrStr, &subArraysSize);

    int returnSize = 0;
    int* result = predictGeneration(sub_arrays, subArraysSize, station_capacity, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", result[i]);
        if (i < returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < subArraysSize; i++) free(sub_arrays[i]);
    free(sub_arrays);
    free(result);
    return 0;
}
