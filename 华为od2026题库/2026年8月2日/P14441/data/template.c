#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2000000

// 解析整数列表 [a1,a2,...,an]
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(100000 * sizeof(int));
    *outCount = 0;
    int i = 0;
    int n = (int)strlen(s);
    while (i < n && s[i] != '[') i++; // 跳过非括号字符
    i++; // 跳过 [
    int cur = 0;
    bool hasNum = false;
    while (i < n) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            cur = cur * 10 + (c - '0');
            hasNum = true;
        } else if (c == ',' || c == ']') {
            if (hasNum) {
                res[(*outCount)++] = cur;
                cur = 0;
                hasNum = false;
            }
            if (c == ']') break;
        }
        i++;
    }
    return res;
}

// 前置声明用户函数
int minSkillSegments(int k, int m, int w, int* a, int n);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) return 1;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析 k,m,w,[...]
    const char* firstComma = strchr(line, ',');
    char kStr[32];
    int kLen = (int)(firstComma - line);
    strncpy(kStr, line, kLen);
    kStr[kLen] = '\0';
    int k = atoi(kStr);

    const char* rest1 = firstComma + 1;
    const char* secondComma = strchr(rest1, ',');
    char mStr[32];
    int mLen = (int)(secondComma - rest1);
    strncpy(mStr, rest1, mLen);
    mStr[mLen] = '\0';
    int m = atoi(mStr);

    const char* rest2 = secondComma + 1;
    const char* thirdComma = strchr(rest2, ',');
    char wStr[32];
    int wLen = (int)(thirdComma - rest2);
    strncpy(wStr, rest2, wLen);
    wStr[wLen] = '\0';
    int w = atoi(wStr);

    const char* rest3 = thirdComma + 1;
    int aCount;
    int* a = parseIntList(rest3, &aCount);

    int result = minSkillSegments(k, m, w, a, aCount);
    printf("%d\n", result);

    free(a);
    free(line);
    return 0;
}
