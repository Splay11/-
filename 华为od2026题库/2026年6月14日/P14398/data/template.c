#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000
#define MAX_TOKENS 1000

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int nums[MAX_TOKENS];
    int numsSize = 0;
    int base = 0;

    // 解析类似 [10,25,3,15,8],16
    char *p = line;
    while (*p && *p != '[') p++;
    if (*p == '[') p++;
    while (*p && *p != ']') {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']') break;
        nums[numsSize++] = strtol(p, &p, 10);
    }
    while (*p && *p != ',') p++;
    if (*p == ',') p++;
    base = atoi(p);

    int returnSize = 0;
    char** res = sortConvertedNums(nums, numsSize, base, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("\"%s\"", res[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < returnSize; i++) free(res[i]);
    free(res);
    return 0;
}
