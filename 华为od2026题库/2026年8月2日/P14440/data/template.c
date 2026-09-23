#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE_LEN 204800

// 解析 JSON 字符串列表，如 ["a","b","c"]
static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(100 * sizeof(char*));
    *outCount = 0;
    char* cur = (char*)malloc(2048);  // 单个版本号最长 1024，用堆避免栈溢出
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

// 前置声明用户函数
char* findLatestVersion(char** versions, int versionsSize, int* resultSize);

int main() {
    char line[MAX_LINE_LEN];
    if (!fgets(line, MAX_LINE_LEN, stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int count = 0;
    char** versions = parseStringList(line, &count);

    int resultSize = 0;
    char* result = findLatestVersion(versions, count, &resultSize);

    printf("\"%s\"\n", result);

    free(result);
    for (int i = 0; i < count; i++) free(versions[i]);
    free(versions);

    return 0;
}
