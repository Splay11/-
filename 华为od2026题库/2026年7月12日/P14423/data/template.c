#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 300000
#define MAX_TOKENS 6000

// 解析字符串数组 ["a:v1:","b:v1:"] -> char**（每条为去引号后的内容）
static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    static char cur[MAX_LEN];   // 单条字符串缓冲（静态存储，避免栈溢出）
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

// 找到两个顶层数组之间的逗号（括号深度为 0 且不在字符串内）
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

char** getDependencyOrder(char** directDeps, int directDepsSize,
                          char** depRules, int depRulesSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int comma = findTopLevelComma(line);
    char arr1[MAX_LEN];
    strncpy(arr1, line, comma);
    arr1[comma] = '\0';
    int directDepsSize = 0;
    char** directDeps = parseStringList(arr1, &directDepsSize);

    const char* arr2 = line + comma + 1;
    int depRulesSize = 0;
    char** depRules = parseStringList(arr2, &depRulesSize);

    int returnSize = 0;
    char** result = getDependencyOrder(directDeps, directDepsSize, depRules, depRulesSize, &returnSize);

    // 按题面样例格式输出：["name:version",...]（无空格）
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(",");
        printf("\"%s\"", result[i]);
    }
    printf("]\n");

    for (int i = 0; i < directDepsSize; i++) free(directDeps[i]);
    for (int i = 0; i < depRulesSize; i++) free(depRules[i]);
    free(directDeps);
    free(depRules);
    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);

    return 0;
}
