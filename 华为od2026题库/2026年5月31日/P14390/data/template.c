#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2000000

long long maxEnergyDivisibleByK(int* nums, int n, int k);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    size_t total = 0, cap = MAX_LEN;
    while (1) {
        size_t r = fread(line + total, 1, cap - total - 1, stdin);
        if (r == 0) break;
        total += r;
        if (total + 1 >= cap) {
            cap *= 2;
            line = (char*)realloc(line, cap);
        }
    }
    line[total] = '\0';
    while (total > 0 && (line[total - 1] == '\n' || line[total - 1] == '\r')) line[--total] = '\0';

    char* start = strchr(line, '[');
    char* end = strchr(line, ']');
    if (!start || !end || end <= start) { free(line); return 0; }

    // 解析数组
    char arrStr[MAX_LEN];
    int arrLen = end - start - 1;
    if (arrLen < 0 || arrLen >= MAX_LEN) { free(line); return 0; }
    strncpy(arrStr, start + 1, arrLen);
    arrStr[arrLen] = '\0';

    int* nums = (int*)malloc(MAX_LEN * sizeof(int));
    int nParsed = 0;
    char* token = strtok(arrStr, ",");
    while (token != NULL) {
        while (*token == ' ') token++;
        nums[nParsed++] = atoi(token);
        token = strtok(NULL, ",");
    }

    // 解析 n 和 k
    char* afterArr = end + 1;
    while (*afterArr == ',' || *afterArr == ' ') afterArr++;
    int firstVal = atoi(afterArr);
    char* comma2 = strchr(afterArr, ',');
    int nVal, kVal;
    if (comma2) {
        // 格式: [nums],n,k
        nVal = firstVal;
        kVal = atoi(comma2 + 1);
    } else {
        // 格式: [nums],k（n 自动取自数组长度）
        nVal = nParsed;
        kVal = firstVal;
    }

    long long result = maxEnergyDivisibleByK(nums, nVal, kVal);
    printf("%lld\n", result);

    free(nums);
    free(line);
    return 0;
}
