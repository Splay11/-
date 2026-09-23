#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 输入规模很小（n<=20, m<=12），缓冲区足够
#define MAX_LEN 8192

// 找到括号深度为 0 的第一个逗号（用于切分顶层字段 n,m,files,cost）
static int findTopLevelComma(const char* s) {
    int bracket = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '[') bracket++;
        else if (c == ']') bracket--;
        else if (c == ',' && bracket == 0) return i;
    }
    return -1;
}

// 解析一维整数列表，如 [1,2,2]
static void parseCost(const char* s, int* cost, int* nCost) {
    int i = 0;
    while (s[i] && s[i] != '[') i++;
    i++;  // 跳过 '['
    int cur = 0, has = 0;
    *nCost = 0;
    while (s[i]) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            cur = cur * 10 + (c - '0');
            has = 1;
        } else if (c == ',' || c == ']') {
            // 遇到逗号或 ']' 时结算当前整数
            if (has) {
                cost[(*nCost)++] = cur;
                cur = 0;
                has = 0;
            }
            if (c == ']') break;  // 列表结束
        }
        i++;
    }
}

// 解析二维整数列表，如 [[0,1],[1,2],[0,2]]
static void parseFiles(const char* s, int files[20][12], int filesLen[20], int* nRows) {
    int i = 0;
    while (s[i] && s[i] != '[') i++;
    i++;  // 跳过外层 '['
    *nRows = 0;
    while (s[i] && s[i] != ']') {
        if (s[i] == '[') {
            i++;  // 跳过本行 '['
            int cnt = 0, cur = 0, has = 0;
            while (s[i]) {
                char c = s[i];
                if (c >= '0' && c <= '9') {
                    cur = cur * 10 + (c - '0');
                    has = 1;
                } else if (c == ',' || c == ']') {
                    // 遇到逗号或 ']' 时结算当前整数
                    if (has) {
                        if (cnt < 12) files[*nRows][cnt] = cur;
                        cnt++;
                        cur = 0;
                        has = 0;
                    }
                    if (c == ']') break;  // 本行结束
                }
                i++;
            }
            filesLen[*nRows] = cnt;
            (*nRows)++;
            i++;  // 跳过本行 ']'
            if (s[i] == ',') i++;  // 跳过行分隔逗号
        } else {
            i++;
        }
    }
}

int minCost(int n, int m, int** files, int filesSize, int* filesColSize, int* cost, int costSize);

int main() {
    static char line[MAX_LEN];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 依次按顶层逗号切分为 n, m, files, cost 四段
    int c1 = findTopLevelComma(line);
    char nbuf[16];
    strncpy(nbuf, line, c1);
    nbuf[c1] = '\0';
    int n = atoi(nbuf);

    const char* rest1 = line + c1 + 1;
    int c2 = findTopLevelComma(rest1);
    char mbuf[16];
    strncpy(mbuf, rest1, c2);
    mbuf[c2] = '\0';
    int m = atoi(mbuf);

    const char* rest2 = rest1 + c2 + 1;
    int c3 = findTopLevelComma(rest2);
    if (c3 < 0) return 0;

    char filesBuf[MAX_LEN];
    if (c3 < MAX_LEN) {
        strncpy(filesBuf, rest2, c3);
        filesBuf[c3] = '\0';
    } else {
        filesBuf[0] = '\0';
    }

    int files[20][12];
    int filesLen[20];
    int nRows = 0;
    parseFiles(filesBuf, files, filesLen, &nRows);

    int cost[12];
    int nCost = 0;
    parseCost(rest2 + c3 + 1, cost, &nCost);

    // 组装 int** 传给选手函数
    int* filesPtr[20];
    for (int r = 0; r < nRows; r++) filesPtr[r] = files[r];
    int result = minCost(n, m, (int**)filesPtr, nRows, filesLen, cost, nCost);
    printf("%d\n", result);
    return 0;
}
