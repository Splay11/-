#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 10000
#define MAX_TOKENS 50

/**
 * 提取引号内的字符串
 */
static void parseQuotedString(const char* s, char* out) {
    const char* start = strchr(s, '"');
    if (!start) { out[0] = '\0'; return; }
    start++;
    const char* end = strrchr(s, '"');
    if (!end || end <= start) { out[0] = '\0'; return; }
    int len = (int)(end - start);
    strncpy(out, start, len);
    out[len] = '\0';
}

/**
 * 解析整型数组 [a,b,c,...]
 */
static int* parseIntList(const char* s, int* outSize) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outSize = 0;
    int num = 0;
    bool hasNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            hasNum = true;
        } else if ((c == ',' || c == ']') && hasNum) {
            res[(*outSize)++] = num;
            num = 0;
            hasNum = false;
            if (c == ']') break;
        }
    }
    return res;
}

/**
 * 找到第一个顶层逗号（不在引号内且括号深度为 0）
 */
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

// 前置声明用户函数
char** allocateSubnets(const char* cidr, int n, int* requirements,
                       int requirementsSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析: "CIDR",N,[requirements]
    int comma1 = findTopLevelComma(line);
    char cidrPart[100];
    strncpy(cidrPart, line, comma1);
    cidrPart[comma1] = '\0';

    char cidr[50];
    parseQuotedString(cidrPart, cidr);

    const char* rest = line + comma1 + 1;
    int comma2 = findTopLevelComma(rest);
    char nStr[16];
    strncpy(nStr, rest, comma2);
    nStr[comma2] = '\0';
    int n = atoi(nStr);

    const char* reqStr = rest + comma2 + 1;
    int reqSize;
    int* requirements = parseIntList(reqStr, &reqSize);

    int returnSize;
    char** result = allocateSubnets(cidr, n, requirements, reqSize, &returnSize);

    // 输出结果
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("\"%s\"", result[i]);
        free(result[i]);
    }
    printf("]\n");
    free(result);
    free(requirements);

    return 0;
}
