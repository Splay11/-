#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// 用户函数声明 — 匹配服务器模板签名
int countHikingPaths(int** grid, int gridSize, int* gridColSize, int maxDiff);

// 读取全部 stdin
static char* read_all(void) {
    size_t cap = 4096, len = 0;
    char* buf = (char*)malloc(cap);
    if (!buf) return NULL;
    int c;
    while ((c = getchar()) != EOF) {
        if (len + 1 >= cap) {
            cap *= 2;
            char* tmp = (char*)realloc(buf, cap);
            if (!tmp) { free(buf); return NULL; }
            buf = tmp;
        }
        buf[len++] = (char)c;
    }
    buf[len] = '\0';
    return buf;
}

int main() {
    char* input = read_all();
    if (!input) return 1;

    // 去尾部换行
    size_t len = strlen(input);
    while (len > 0 && (input[len-1] == '\n' || input[len-1] == '\r'))
        input[--len] = '\0';

    const char* p = input;

    // 解析二维数组 [[...],[...],...]
    // 格式: [[a,b],[c,d]],maxDiff
    if (*p != '[') return 1;
    p++; // 跳过外层 [
    if (*p != '[') return 1;

    // 先解析所有行
    int** grid = (int**)malloc(10 * sizeof(int*));
    int* colSizes = (int*)malloc(10 * sizeof(int));
    int rows = 0;

    while (*p == '[') {
        p++; // 跳过 [
        int* row = (int*)malloc(10 * sizeof(int));
        int cols = 0;

        while (1) {
            // 跳过空白
            while (*p == ' ') p++;
            // 解析数字
            int neg = 1;
            if (*p == '-') { neg = -1; p++; }
            int val = 0;
            while (*p >= '0' && *p <= '9') {
                val = val * 10 + (*p - '0');
                p++;
            }
            row[cols++] = neg * val;
            // 跳过空白
            while (*p == ' ') p++;
            if (*p == ']') { p++; break; }  // 行结束
            if (*p == ',') p++;  // 列分隔
        }

        grid[rows] = row;
        colSizes[rows] = cols;
        rows++;

        // 跳过空白
        while (*p == ' ') p++;
        if (*p == ',') p++;  // 行分隔
        while (*p == ' ') p++;
    }
    // 现在 p 指向外层 ] 之后

    // 跳过 ]
    if (*p == ']') p++;

    // 跳过 ,
    while (*p == ' ' || *p == ',') p++;

    // 解析 maxDiff
    int maxDiff = 0;
    while (*p >= '0' && *p <= '9') {
        maxDiff = maxDiff * 10 + (*p - '0');
        p++;
    }

    // 调用用户函数
    int result = countHikingPaths(grid, rows, colSizes, maxDiff);

    printf("%d\n", result);

    // 释放内存
    for (int i = 0; i < rows; i++) free(grid[i]);
    free(grid);
    free(colSizes);
    free(input);

    return 0;
}
