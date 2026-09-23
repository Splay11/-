#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_LEN 200000
#define MAX_ROWS 1000

int* getMaxValues(int** data, int dataSize, int* dataColSize, int interval, int* returnSize);

static int findTopLevelComma(const char* s) {
    int bracket = 0;
    int len = (int)strlen(s);
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '[') bracket++;
        else if (c == ']') bracket--;
        else if (c == ',' && bracket == 0) return i;
    }
    return -1;
}

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 1;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int comma = findTopLevelComma(line);
    // 解析 interval
    int interval = atoi(line + comma + 1);

    // 解析 data 二维数组
    int** data = (int**)malloc(MAX_ROWS * sizeof(int*));
    int* dataColSize = (int*)malloc(MAX_ROWS * sizeof(int));
    int dataSize = 0;

    const char* p = line;
    // 跳到第一个 [
    while (*p && *p != '[') p++;
    p++; // 跳过外层 [
    while (*p) {
        while (*p && *p != '[') {
            if (*p == ']') { p++; break; }
            p++;
        }
        if (!*p || *(p - 1) == ']') break;
        p++; // 跳过内层 [

        // 解析 timestamp
        int sign = 1;
        if (*p == '-') { sign = -1; p++; }
        int t = 0;
        while (*p && isdigit(*p)) { t = t * 10 + (*p - '0'); p++; }
        t *= sign;

        p++; // 跳过逗号

        // 解析 value
        sign = 1;
        if (*p == '-') { sign = -1; p++; }
        int v = 0;
        while (*p && isdigit(*p)) { v = v * 10 + (*p - '0'); p++; }
        v *= sign;

        data[dataSize] = (int*)malloc(2 * sizeof(int));
        data[dataSize][0] = t;
        data[dataSize][1] = v;
        dataColSize[dataSize] = 2;
        dataSize++;

        p++; // 跳过内层 ]
    }

    int returnSize;
    int* result = getMaxValues(data, dataSize, dataColSize, interval, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("%d", result[i]);
    }
    printf("]\n");

    free(result);
    for (int i = 0; i < dataSize; i++) free(data[i]);
    free(data);
    free(dataColSize);

    return 0;
}
