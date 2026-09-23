#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// 输入整行最大长度（warehouses 最多 100*100*3=30000 个整数）
#define MAX_LINE 400000
#define MAX_WAREHOUSES 200000
#define MAX_QUERIES 100000

// 返回从 start 处的 '[' 匹配的 ']' 的下标
static int matchBracket(const char* s, int start) {
    int depth = 0;
    for (int i = start; s[i]; i++) {
        if (s[i] == '[') depth++;
        else if (s[i] == ']') {
            depth--;
            if (depth == 0) return i;
        }
    }
    return -1;
}

// 解析形如 [1, 2, -3] 的一维整型数组（忽略空格与括号），返回元素个数
static int parse1D(const char* s, int len, int* out) {
    int cnt = 0, i = 0;
    while (i < len) {
        if ((s[i] == '-' && i + 1 < len && isdigit((unsigned char)s[i + 1])) || isdigit((unsigned char)s[i])) {
            int sign = 1;
            if (s[i] == '-') { sign = -1; i++; }
            long long val = 0;
            while (i < len && isdigit((unsigned char)s[i])) { val = val * 10 + (s[i] - '0'); i++; }
            out[cnt++] = (int)(sign * val);
        } else {
            i++;
        }
    }
    return cnt;
}

int** getWarehouseReport(int* warehouses, int warehousesSize, int** queries, int queriesSize,
                         int* queriesColSize, int numOfWarehouse, int* returnSize, int** returnColumnSizes);

int main() {
    char* line = (char*)malloc(MAX_LINE);
    if (!fgets(line, MAX_LINE, stdin)) { free(line); return 0; }
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    // warehouses：第一个 [...] 数组
    int p1 = 0;
    while (line[p1] && line[p1] != '[') p1++;
    int e1 = matchBracket(line, p1);
    int* warehouses = (int*)malloc(sizeof(int) * MAX_WAREHOUSES);
    int warehousesSize = parse1D(line + p1, e1 - p1 + 1, warehouses);

    // queries：第二个 [[...]] 数组
    int p2 = e1 + 1;
    while (line[p2] && line[p2] != '[') p2++;
    int e2 = matchBracket(line, p2);

    int** queries = (int**)malloc(sizeof(int*) * MAX_QUERIES);
    int* queriesColSize = (int*)malloc(sizeof(int) * MAX_QUERIES);
    int queriesSize = 0;
    int j = p2 + 1; // 跳过外层 '['
    while (j <= e2) {
        if (line[j] == '[') {
            int k = matchBracket(line, j);
            int* row = (int*)malloc(sizeof(int) * 8);
            queriesColSize[queriesSize] = parse1D(line + j, k - j + 1, row);
            queries[queriesSize] = row;
            queriesSize++;
            j = k + 1;
        } else {
            j++;
        }
    }

    // 末尾整数 numOfWarehouse
    int numOfWarehouse = atoi(line + e2 + 1);

    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** res = getWarehouseReport(warehouses, warehousesSize, queries, queriesSize,
                                   queriesColSize, numOfWarehouse, &returnSize, &returnColumnSizes);

    // 紧凑输出 [[..],[..]]
    printf("[");
    for (int a = 0; a < returnSize; a++) {
        if (a) printf(",");
        printf("[");
        for (int b = 0; b < returnColumnSizes[a]; b++) {
            if (b) printf(",");
            printf("%d", res[a][b]);
        }
        printf("]");
    }
    printf("]\n");

    free(line);
    return 0;
}
