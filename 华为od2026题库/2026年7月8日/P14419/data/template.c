#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 100
#define MAX_INPUT 262144

// 切分顶层逗号
static void splitTopLevel(const char* s, char** parts) {
    int depth = 0, start = 0, partIdx = 0, len = (int)strlen(s);
    for (int i = 0; i <= len; i++) {
        if (i == len || (s[i] == ',' && depth == 0)) {
            int partLen = i - start;
            parts[partIdx] = (char*)malloc(partLen + 1);
            strncpy(parts[partIdx], s + start, partLen);
            parts[partIdx][partLen] = '\0';
            partIdx++;
            start = i + 1;
        } else if (s[i] == '[') depth++;
          else if (s[i] == ']') depth--;
    }
}

// 解析 "[1,2,3]" → int 数组
static int* parseIntArray(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_N * sizeof(int));
    *outCount = 0;
    int val = 0, sign = 1, inNum = 0;
    for (int i = 0; s[i]; i++) {
        if (s[i] == '-') { sign = -1; inNum = 1; }
        else if (s[i] >= '0' && s[i] <= '9') { val = val * 10 + (s[i] - '0'); inNum = 1; }
        else {
            if (inNum) { res[(*outCount)++] = sign * val; val = 0; sign = 1; inNum = 0; }
        }
    }
    return res;
}

// 解析 "[[0,1],[2,3]]" → 二维 int 数组
static int** parseInt2DArray(const char* s, int* outRows, int** outCols) {
    int** res = (int**)malloc(MAX_N * MAX_N / 2 * sizeof(int*));
    *outRows = 0;
    *outCols = (int*)malloc(MAX_N * MAX_N / 2 * sizeof(int));
    const char* p = s;
    while (*p) {
        if (*p == '[' && (*(p+1) >= '0' && *(p+1) <= '9' || *(p+1) == '-')) {
            p++;
            int row[2], col = 0;
            while (*p && *p != ']') {
                if ((*p >= '0' && *p <= '9') || *p == '-') {
                    row[col++] = atoi(p);
                    while (*p >= '0' && *p <= '9') p++;
                } else { p++; }
            }
            if (*p == ']') p++;
            res[*outRows] = (int*)malloc(2 * sizeof(int));
            res[*outRows][0] = row[0];
            res[*outRows][1] = row[1];
            (*outCols)[*outRows] = 2;
            (*outRows)++;
        } else { p++; }
    }
    return res;
}

int maxCarbonReduction(int* green, int greenSize, int* carbon, int carbonSize,
                       int** edges, int edgesRows, int* edgesCols);

int main() {
    char line[MAX_INPUT];
    fgets(line, MAX_INPUT, stdin);
    int len = (int)strlen(line);
    while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r'))
        line[--len] = '\0';

    char* parts[3] = {NULL, NULL, NULL};
    splitTopLevel(line, parts);

    int greenSize, carbonSize, edgesRows, *edgesCols;
    int* green = parseIntArray(parts[0], &greenSize);
    int* carbon = parseIntArray(parts[1], &carbonSize);
    int** edges = parseInt2DArray(parts[2], &edgesRows, &edgesCols);

    int result = maxCarbonReduction(green, greenSize, carbon, carbonSize,
                                     edges, edgesRows, edgesCols);
    printf("%d\n", result);

    free(green); free(carbon);
    for (int i = 0; i < edgesRows; i++) free(edges[i]);
    free(edges); free(edgesCols);
    for (int i = 0; i < 3; i++) free(parts[i]);
    return 0;
}
