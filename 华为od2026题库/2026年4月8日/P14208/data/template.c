#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000
#define MAX_TOKENS 1000

// 解析 ["a","b"] 形式的字符串数组
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

int countBirthdayGifts(int month, char** employees, char** birthdays, int size);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int firstComma = -1;
    bool inStr = false;
    for (int i = 0; i < len; i++) {
        char c = line[i];
        if (c == '"') inStr = !inStr;
        else if (c == ',' && !inStr) {
            firstComma = i;
            break;
        }
    }
    if (firstComma == -1) return 0;
    char monthStr[20];
    strncpy(monthStr, line, firstComma);
    monthStr[firstComma] = '\0';
    int month = atoi(monthStr);

    const char* rest = line + firstComma + 1;
    const char* split = strstr(rest, "],[");
    if (!split) return 0;
    int splitPos = (int)(split - rest);
    char empStr[MAX_LEN];
    strncpy(empStr, rest, splitPos + 1);
    empStr[splitPos + 1] = '\0';
    const char* birthStr = rest + splitPos + 2;

    int empSize, birthSize;
    char** employees = parseStringList(empStr, &empSize);
    char** birthdays = parseStringList(birthStr, &birthSize);

    int result = countBirthdayGifts(month, employees, birthdays, empSize);
    printf("%d\n", result);

    for (int i = 0; i < empSize; i++) free(employees[i]);
    for (int i = 0; i < birthSize; i++) free(birthdays[i]);
    free(employees);
    free(birthdays);
    return 0;
}
