#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 1000000
#define MAX_TOKENS 200000

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char cur[128];
    int curLen = 0;
    bool inString = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '"') {
            if (inString) {
                cur[curLen] = '\0';
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
            inString = !inString;
        } else if (inString) {
            cur[curLen++] = c;
        }
    }
    return res;
}

static int* parseIntList(const char* s, int* outCount) {
    int* arr = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0, sign = 1;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') {
            sign = -1;
        } else if (c >= '0' && c <= '9') {
            if (!inNum) {
                inNum = true;
                num = 0;
            }
            num = num * 10 + (c - '0');
        } else {
            if (inNum) {
                arr[*outCount] = num * sign;
                (*outCount)++;
                num = 0;
                sign = 1;
                inNum = false;
            }
        }
    }
    if (inNum) {
        arr[*outCount] = num * sign;
        (*outCount)++;
    }
    return arr;
}

int* monitor(char** ops, int opsSize, int* vals, int valsSize, int* returnSize);

int main() {
    // 读取整行输入（格式: ["add","query"],[1,1]）
    char* line = (char*)malloc(MAX_LEN);
    size_t total = 0, cap = MAX_LEN;
    while (1) {
        size_t r = fread(line + total, 1, cap - total - 1, stdin);
        if (r == 0) break;
        total += r;
        if (total + 1 >= cap) {
            cap *= 2;
            char* newline = (char*)realloc(line, cap);
            if (!newline) { free(line); return 0; }
            line = newline;
        }
    }
    line[total] = '\0';
    int len = total;
    while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = '\0';

    // 找到 "],[" 分隔符
    char* split = strstr(line, "],[");
    if (!split) return 0;
    int opsLen = (int)(split - line) + 1;
    char* opsStr = (char*)malloc(opsLen + 1);
    strncpy(opsStr, line, opsLen);
    opsStr[opsLen] = '\0';

    const char* valsStr = split + 2;

    int opsSize, valsSize;
    char** ops = parseStringList(opsStr, &opsSize);
    int* vals = parseIntList(valsStr, &valsSize);
    free(opsStr);

    int returnSize;
    int* result = monitor(ops, opsSize, vals, valsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("%d", result[i]);
    }
    printf("]\n");

    for (int i = 0; i < opsSize; i++) free(ops[i]);
    free(ops);
    free(vals);
    if (result) free(result);
    free(line);

    return 0;
}
