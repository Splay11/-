#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 64
#define MAX_TOKENS 256

// 解析形如 ["a","b","c"] 的字符串数组（提取所有引号内的内容）
static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char cur[MAX_LEN];
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

char** normalizeDates(char** dates, int datesSize, int* returnSize);

int main() {
    // 输入上限：200 个字符串 × 约 53 字符（含引号/逗号）≈ 11KB
    char line[16384];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 整行即 JSON 字符串数组，提取所有字符串
    int datesSize = 0;
    char** dates = parseStringList(line, &datesSize);

    int returnSize = 0;
    char** ans = normalizeDates(dates, datesSize, &returnSize);

    // 按题面格式输出：["a","b",...]（无空格）
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(",");
        printf("\"%s\"", ans[i]);
    }
    printf("]\n");

    for (int i = 0; i < datesSize; i++) free(dates[i]);
    free(dates);
    for (int i = 0; i < returnSize; i++) free(ans[i]);
    free(ans);

    return 0;
}
