#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

// 解析一维整数数组，如 [3,2,1]
static int* parseIntArray(const char* s, int* outCount) {
    int* arr = (int*)malloc(sizeof(int) * 1000);
    *outCount = 0;
    const char* p = s;
    while (*p) {
        if (*p == '[' || *p == ']' || *p == ' ' || *p == ',') {
            p++;
            continue;
        }
        char* end = NULL;
        long val = strtol(p, &end, 10);
        if (end != p) {
            arr[*outCount] = (int)val;
            (*outCount)++;
            p = end;
        } else {
            p++;
        }
    }
    return arr;
}

// 解析二维整数数组，如 [[0,1],[2,3]]
static int** parse2DIntArray(const char* s, int* outRows, int* outCols) {
    int** res = (int**)malloc(sizeof(int*) * 100);
    *outRows = 0;
    *outCols = 0;
    const char* p = s;
    while (*p && *p != '[') p++;
    while (*p) {
        if (*p == '[') {
            int temp[100];
            int cnt = 0;
            p++;
            while (*p && *p != ']') {
                if (*p == ',' || *p == ' ') {
                    p++;
                    continue;
                }
                char* end = NULL;
                long val = strtol(p, &end, 10);
                if (end != p) {
                    temp[cnt++] = (int)val;
                    p = end;
                } else {
                    p++;
                }
            }
            if (cnt > 0) {
                res[*outRows] = (int*)malloc(sizeof(int) * cnt);
                for (int i = 0; i < cnt; i++) res[*outRows][i] = temp[i];
                (*outRows)++;
                if (*outCols == 0) *outCols = cnt;
            }
        }
        if (!*p) break;
        p++;
    }
    return res;
}

int* processDataArray(int* data, int dataSize, int** operations, int operationsSize, int* operationsColSize, int* returnSize);

int main() {
    char input[MAX_LEN];
    fgets(input, MAX_LEN, stdin);
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';

    char dataStr[MAX_LEN];
    strcpy(dataStr, input);

    // 找到第一个二维数组的开始
    const char* dataEnd = strchr(dataStr, ']');
    char dataPart[MAX_LEN], opsPart[MAX_LEN];
    int endPos = (int)(dataEnd - dataStr);
    strncpy(dataPart, dataStr, endPos + 1);
    dataPart[endPos + 1] = '\0';

    const char* opsStart = dataStr + endPos + 1;
    while (*opsStart && (*opsStart == ',' || *opsStart == ' ')) opsStart++;

    strcpy(opsPart, opsStart);

    int dataSize, operationsSize, operationsColSize;
    int* data = parseIntArray(dataPart, &dataSize);
    int** operations = parse2DIntArray(opsPart, &operationsSize, &operationsColSize);

    int returnSize;
    int* result = processDataArray(data, dataSize, operations, operationsSize, &operationsColSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", result[i]);
        if (i < returnSize - 1) printf(",");
    }
    printf("]\n");

    free(data);
    for (int i = 0; i < operationsSize; i++) free(operations[i]);
    free(operations);
    free(result);
    return 0;
}
