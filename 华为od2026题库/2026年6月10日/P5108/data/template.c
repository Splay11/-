#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000
#define MAX_TOKENS 10000

// 解析 [1,2,3] 形式的整数数组
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int i = 0;
    int n = strlen(s);
    int num = 0;
    bool neg = false, inNum = false;
    for (i = 0; i < n; i++) {
        char c = s[i];
        if ((c >= '0' && c <= '9') || c == '-') {
            if (!inNum) { inNum = true; neg = false; num = 0; if (c == '-') neg = true; else num = c - '0'; }
            else {
                if (c == '-') neg = true;
                else num = num * 10 + (c - '0');
            }
        } else if (c == ',' || c == ']') {
            if (inNum) {
                res[*outCount] = neg ? -num : num;
                (*outCount)++;
                inNum = false;
            }
        }
    }
    return res;
}

int* analyzeTemperatureData(int* temperatures, int temperaturesSize, int k, int t, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    // 输入格式: n,[arr],k,t
    // 例: 8,[20,25,30,28,35,40,42,25],3,10
    // 找到第一个逗号（在 n 之后）
    int firstComma = -1;
    for (int i = 0; i < len; i++) {
        if (line[i] == ',') { firstComma = i; break; }
    }

    // 找到数组的 [ ]
    int bracketStart = -1, bracketEnd = -1;
    for (int i = 0; i < len; i++) {
        if (line[i] == '[') bracketStart = i;
        else if (line[i] == ']') { bracketEnd = i; break; }
    }

    // 截取数组部分（含方括号）
    char arrStr[MAX_LEN];
    int arrLen = bracketEnd - bracketStart + 1;
    strncpy(arrStr, line + bracketStart, arrLen);
    arrStr[arrLen] = '\0';

    // 解析数组
    int temperaturesSize = 0;
    int* temperatures = parseIntList(arrStr, &temperaturesSize);

    // 解析 k 和 t：从 ] 后面的逗号之后开始
    const char* afterBracket = line + bracketEnd + 1;
    // 跳过逗号
    if (*afterBracket == ',') afterBracket++;
    int kParam, tParam;
    char* comma2 = strchr(afterBracket, ',');
    if (comma2) {
        char kPart[50];
        strncpy(kPart, afterBracket, comma2 - afterBracket);
        kPart[comma2 - afterBracket] = '\0';
        kParam = atoi(kPart);
        tParam = atoi(comma2 + 1);
    } else {
        kParam = 0;
        tParam = 0;
    }

    int returnSize = 0;
    int* result = analyzeTemperatureData(temperatures, temperaturesSize, kParam, tParam, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(",");
        printf("%d", result[i]);
    }
    printf("]\n");

    free(temperatures);
    free(result);
    return 0;
}
