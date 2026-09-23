#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000
#define MAX_TEAMS 16
#define MAX_MATCHES 256

// 声明用户函数
char** getTopThree(int teamNum, char*** matches, int matchesSize, int* returnSize);

// 寻找顶层逗号位置
static int findTopLevelComma(const char* s) {
    int bracket = 0;
    bool inString = false;
    int len = (int)strlen(s);
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '"') {
            inString = !inString;
        } else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

// 手动解析二维 JSON 字符串数组
// 输入为 [[match1],[match2],...]
static char*** parseMatches(const char* s, int* outMatchesSize) {
    char*** matches = (char***)malloc(MAX_MATCHES * sizeof(char**));
    *outMatchesSize = 0;
    int pos = 0;
    int len = (int)strlen(s);

    while (pos < len) {
        if (s[pos] == '[' && (pos == 0 || s[pos - 1] == '[' || s[pos - 1] == ',')) {
            pos++;  // 跳过内层 [
            // 解析一个 match [str, str, str, str]
            char** match = (char**)malloc(4 * sizeof(char*));
            int field = 0;
            char buf[MAX_LEN];
            int bl = 0;

            while (pos < len && s[pos] != ']' && field < 4) {
                if (s[pos] == '"') {
                    pos++;  // 跳过左引号
                    bl = 0;
                    while (pos < len && s[pos] != '"') {
                        buf[bl++] = s[pos];
                        pos++;
                    }
                    buf[bl] = '\0';
                    match[field] = (char*)malloc(bl + 1);
                    strcpy(match[field], buf);
                    field++;
                    pos++;  // 跳过右引号
                } else {
                    pos++;
                }
            }

            matches[*outMatchesSize] = match;
            (*outMatchesSize)++;
            pos++;  // 跳过内层 ]
        } else {
            pos++;
        }
    }
    return matches;
}

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int comma = findTopLevelComma(line);

    // 提取 teamNum
    char teamNumStr[16];
    // 安全地复制 teamNum 部分
    int tnLen = comma;
    if (tnLen >= 16) tnLen = 15;
    memcpy(teamNumStr, line, tnLen);
    teamNumStr[tnLen] = '\0';
    int teamNum = atoi(teamNumStr);

    // 提取 matches 部分
    const char* rest = line + comma + 1;

    int matchesSize = 0;
    char*** matches = parseMatches(rest, &matchesSize);

    int returnSize = 0;
    char** result = getTopThree(teamNum, matches, matchesSize, &returnSize);

    // 输出 JSON 数组
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("\"%s\"", result[i]);
    }
    printf("]\n");

    // 清理
    for (int i = 0; i < matchesSize; i++) {
        for (int j = 0; j < 4; j++) free(matches[i][j]);
        free(matches[i]);
    }
    free(matches);

    return 0;
}
