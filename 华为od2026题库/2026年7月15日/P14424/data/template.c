#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 10000
#define MAX_TOKENS 200

// 解析形如 [1,5,3] 的整数列表（忽略括号、空格，按逗号切分）
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    char cur[32];
    int curLen = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '[' || c == ']' || c == ' ') continue;
        if (c == ',') {
            if (curLen > 0) {
                cur[curLen] = '\0';
                res[*outCount] = atoi(cur);
                (*outCount)++;
                curLen = 0;
            }
        } else {
            cur[curLen++] = c;
        }
    }
    if (curLen > 0) {
        cur[curLen] = '\0';
        res[*outCount] = atoi(cur);
        (*outCount)++;
    }
    return res;
}

int* findMissingStudents(int n, int* submitted, int submittedSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 顶层逗号：分隔 N 与已交卷列表
    int comma = (int)(strchr(line, ',') - line);
    char nStr[32];
    strncpy(nStr, line, comma);
    nStr[comma] = '\0';
    int n = atoi(nStr);

    const char* rest = line + comma + 1;
    int submittedSize = 0;
    int* submitted = parseIntList(rest, &submittedSize);

    int returnSize = 0;
    int* ans = findMissingStudents(n, submitted, submittedSize, &returnSize);

    // 按题面格式输出：[a,b,c]（无空格）
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(",");
        printf("%d", ans[i]);
    }
    printf("]\n");

    free(submitted);
    free(ans);
    return 0;
}
