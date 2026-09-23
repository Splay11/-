#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

// 解析 [a,b,c] 形式的整数数组
static int* parseIntArray(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_LEN * sizeof(int));
    *outCount = 0;
    int i = 0, sign = 1, num = 0;
    bool inNum = false;
    while (s[i]) {
        if (s[i] == '-') {
            sign = -1;
            inNum = true;
            num = 0;
        } else if (s[i] >= '0' && s[i] <= '9') {
            if (!inNum) {
                inNum = true;
                sign = 1;
                num = 0;
            }
            num = num * 10 + (s[i] - '0');
        } else {
            if (inNum) {
                res[(*outCount)++] = num * sign;
                inNum = false;
                sign = 1;
                num = 0;
            }
        }
        i++;
    }
    if (inNum) {
        res[(*outCount)++] = num * sign;
    }
    return res;
}

int** threeSumWithParity(int* nums, int numsSize, int target, int* returnSize, int** returnColumnSizes);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    char* comma = strrchr(line, ',');
    if (!comma) return 0;
    *comma = '\0';
    const char* arrStr = line;
    const char* targetStr = comma + 1;
    int numsSize;
    int* nums = parseIntArray(arrStr, &numsSize);
    int target = atoi(targetStr);

    int returnSize;
    int* returnColumnSizes;
    int** result = threeSumWithParity(nums, numsSize, target, &returnSize, &returnColumnSizes);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("[");
        for (int j = 0; j < returnColumnSizes[i]; j++) {
            printf("%d", result[i][j]);
            if (j + 1 < returnColumnSizes[i]) printf(",");
        }
        printf("]");
        if (i + 1 < returnSize) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);
    free(returnColumnSizes);
    free(nums);
    return 0;
}
