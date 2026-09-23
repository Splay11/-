#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2000000

// 解析整型二维数组 [[p,w],[p,w],...]，返回 int** 与 packetsSize、packetsColSize
static int** parse2DArray(const char* s, int* outSize, int** outColSize) {
    // 统计内层 '[' 数量 = 行数（总 '[' 数减 1 个外层）
    int rows = 0;
    for (int i = 0; s[i]; i++) if (s[i] == '[') rows++;
    rows -= 1;
    if (rows < 0) rows = 0;
    *outSize = rows;

    int** arr = (int**)malloc((rows > 0 ? rows : 1) * sizeof(int*));
    int* colSize = (int*)malloc((rows > 0 ? rows : 1) * sizeof(int));

    int r = 0;
    int i = 0;
    while (s[i] && s[i] != '[') i++;  // 跳过外层 [
    i++;                              // 进入外层内部
    while (r < rows) {
        while (s[i] && s[i] != '[') i++;  // 找到下一个内层 [
        if (!s[i]) break;
        i++;                          // 进入内层
        int vals[2];
        int cnt = 0;
        char* endptr;
        while (s[i] && s[i] != ']') {
            if (s[i] >= '0' && s[i] <= '9') {
                long v = strtol(s + i, &endptr, 10);
                vals[cnt++] = (int)v;
                i = (int)(endptr - s);
            } else {
                i++;
            }
        }
        arr[r] = (int*)malloc(2 * sizeof(int));
        arr[r][0] = vals[0];
        arr[r][1] = vals[1];
        colSize[r] = 2;
        r++;
        i++;                          // 跳过 ']'
    }
    *outColSize = colSize;
    return arr;
}

int* findPacket(int** packets, int packetsSize, int* packetsColSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int packetsSize = 0;
    int* packetsColSize = NULL;
    int** packets = parse2DArray(line, &packetsSize, &packetsColSize);

    int returnSize = 0;
    int* result = findPacket(packets, packetsSize, packetsColSize, &returnSize);

    // 按题面样例格式输出：[id1,id2,...]（无空格）
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", result[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < packetsSize; i++) free(packets[i]);
    free(packets);
    free(packetsColSize);
    free(result);
    return 0;
}
