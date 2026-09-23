#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 解析形如 [1,2,3] 的整数数组
static int* parseArray(const char* s, int* outCount) {
    int cap = 16, n = 0;
    int* res = (int*)malloc(cap * sizeof(int));
    char cur[16];
    int curLen = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            if (curLen < 15) cur[curLen++] = c;
        } else if (c == ',' || c == ']') {
            if (curLen > 0) {
                cur[curLen] = '\0';
                if (n >= cap) {
                    cap *= 2;
                    res = (int*)realloc(res, cap * sizeof(int));
                }
                res[n++] = atoi(cur);
                curLen = 0;
            }
        }
    }
    *outCount = n;
    return res;
}

int longestSubarray(int* nums, int numsSize);

int main() {
    char line[300005];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    int n;
    int* nums = parseArray(line, &n);
    int result = longestSubarray(nums, n);
    printf("%d\n", result);
    free(nums);
    return 0;
}
