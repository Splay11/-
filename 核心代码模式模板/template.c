#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// 最大字符串长度
#define MAX_LEN 100000
#define MAX_TOKENS 1000

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

static int findTopLevelComma(const char* s) {
    bool inString = false;
    int bracket = 0;
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

int countBirthdayGifts(int month, char** employees, int employeesSize,
                       char** birthdays, int birthdaysSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int comma = findTopLevelComma(line);
    char monthStr[16];
    strncpy(monthStr, line, comma);
    monthStr[comma] = '\0';
    int month = atoi(monthStr);

    const char* rest = line + comma + 1;
    const char* split = strstr(rest, "],[");
    int splitPos = (int)(split - rest);

    char employeesStr[MAX_LEN];
    strncpy(employeesStr, rest, splitPos + 1);
    employeesStr[splitPos + 1] = '\0';

    const char* birthdaysStr = rest + splitPos + 2;

    int employeesSize, birthdaysSize;
    char** employees = parseStringList(employeesStr, &employeesSize);
    char** birthdays = parseStringList(birthdaysStr, &birthdaysSize);

    int result = countBirthdayGifts(month, employees, employeesSize, birthdays, birthdaysSize);
    printf("%d\n", result);

    for (int i = 0; i < employeesSize; i++) free(employees[i]);
    for (int i = 0; i < birthdaysSize; i++) free(birthdays[i]);
    free(employees);
    free(birthdays);

    return 0;
}
