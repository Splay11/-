#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 500000
#define MAX_TOKENS 2000

// 解析 ["a","b"] 形式的字符串数组
static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char* cur = (char*)malloc(MAX_LEN);
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
    free(cur);
    return res;
}

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 按照输入 ["..."],"prefix" 解析
    // 找到第一个 ] 后的逗号
    const char* endArr = strchr(line, ']');
    if (!endArr) {
        printf("[]\n");
        free(line);
        return 0;
    }
    int arrLen = endArr - line + 1;
    char* arrStr = (char*)malloc(arrLen + 1);
    strncpy(arrStr, line, arrLen);
    arrStr[arrLen] = '\0';

    const char* prefixPart = endArr + 1;
    while (*prefixPart && (*prefixPart == ',' || *prefixPart == ' ')) prefixPart++;

    // prefix 部分形如 "prefix"
    char* prefix = (char*)malloc(MAX_LEN);
    prefix[0] = '\0';
    int pLen = 0;
    bool inStr = false;
    for (int i = 0; prefixPart[i]; i++) {
        if (prefixPart[i] == '"') {
            inStr = !inStr;
            if (!inStr) break;
        } else if (inStr) {
            prefix[pLen++] = prefixPart[i];
        }
    }
    prefix[pLen] = '\0';

    int commandsSize = 0;
    char** commands = parseStringList(arrStr, &commandsSize);

    int returnSize = 0;
    char** result = FindNextKeywords(commands, commandsSize, prefix, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("\"%s\"", result[i]);
        if (i + 1 < returnSize) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < commandsSize; i++) free(commands[i]);
    free(commands);
    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);
    free(line);
    free(arrStr);
    free(prefix);

    return 0;
}
