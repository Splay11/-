#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 3000000
#define MAX_TOKENS 200000

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    const char* p = s;
    while (*p) {
        while (*p && (*p == '[' || *p == ']' || *p == ',' || *p == ' ' || *p == '\n' || *p == '\r')) p++;
        if (!*p) break;
        char* end;
        long val = strtol(p, &end, 10);
        if (p == end) break;
        res[(*outCount)++] = (int)val;
        p = end;
    }
    return res;
}

long long minSplitRangeSum(int* nums, int numsSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 1;
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    char* comma = strchr(line, ',');
    if (!comma) { free(line); return 0; }
    char* arrStr = comma + 1;

    int numsSize;
    int* nums = parseIntList(arrStr, &numsSize);

    long long result = minSplitRangeSum(nums, numsSize);
    printf("%lld\n", result);

    free(nums);
    free(line);
    return 0;
}
