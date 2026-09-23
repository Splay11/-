#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 200000

// 解析整数列表 [a1,a2,...,an]
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(1000 * sizeof(int));
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
int longestNonConsecutiveSubstring(int* nums, int n);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) return 1;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int numCount;
    int* nums = parseIntList(line, &numCount);

    int result = longestNonConsecutiveSubstring(nums, numCount);
    printf("%d\n", result);

    free(nums);
    free(line);
    return 0;
}
