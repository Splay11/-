#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 200000
#define MAX_ROWS 2000

// 声明用户函数
int splitSQLToFiles(int splitLine, char** sqlText, int sqlTextSize);

// 找顶层逗号
static int findTopLevelComma(const char* s) {
    int bracket = 0;
    bool inString = false;
    int len = (int)strlen(s);
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '"') inString = !inString;
        else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

// 解析 JSON 字符串数组
static char** parseStringArray(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_ROWS * sizeof(char*));
    *outCount = 0;
    int pos = 0;
    int len = (int)strlen(s);
    char buf[MAX_LEN];
    int bl = 0;
    bool inStr = false;

    while (pos < len) {
        char c = s[pos];
        if (c == '"') {
            if (inStr) {
                buf[bl] = '\0';
                res[*outCount] = (char*)malloc(bl + 1);
                strcpy(res[*outCount], buf);
                (*outCount)++;
                bl = 0;
            }
            inStr = !inStr;
        } else if (inStr) {
            if (bl < MAX_LEN - 1) buf[bl++] = c;
        }
        pos++;
    }
    return res;
}

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int comma = findTopLevelComma(line);

    char slStr[16];
    int tnLen = comma;
    if (tnLen >= 16) tnLen = 15;
    memcpy(slStr, line, tnLen);
    slStr[tnLen] = '\0';
    int splitLine = atoi(slStr);

    const char* rest = line + comma + 1;
    int sqlTextSize = 0;
    char** sqlText = parseStringArray(rest, &sqlTextSize);

    int result = splitSQLToFiles(splitLine, sqlText, sqlTextSize);
    printf("%d\n", result);

    for (int i = 0; i < sqlTextSize; i++) free(sqlText[i]);
    free(sqlText);

    return 0;
}
