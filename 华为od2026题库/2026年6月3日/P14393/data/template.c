#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 1000000
#define MAX_GROUPS 200
#define MAX_PAIRS 200000

static int parseIntList(const char* s, int** outArr) {
    int* arr = (int*)malloc(MAX_GROUPS * sizeof(int));
    int count = 0;
    const char* p = s;
    while (*p) {
        if ((*p >= '0' && *p <= '9') || *p == '-') {
            int val = atoi(p);
            arr[count++] = val;
            while ((*p >= '0' && *p <= '9') || *p == '-') p++;
        } else {
            p++;
        }
    }
    *outArr = arr;
    return count;
}

static int*** allocConf3D(int groupCount, int* sizes) {
    int*** res = (int***)malloc(groupCount * sizeof(int**));
    for (int i = 0; i < groupCount; i++) {
        res[i] = (int**)malloc(sizes[i] * sizeof(int*));
        for (int j = 0; j < sizes[i]; j++) {
            res[i][j] = (int*)malloc(2 * sizeof(int));
        }
    }
    return res;
}

int* canIsolateWithTwoPools(int* resourceCount, int resourceCountSize, int*** conflicts, int* conflictsSizes, int* returnSize);

int main() {
    char* input = (char*)malloc(MAX_LEN);
    if (!input || !fgets(input, MAX_LEN, stdin)) { free(input); return 0; }
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';

    // Find first part [...] and then remaining conflict parts
    const char* p = input;
    const char* firstEnd = strchr(p, ']');
    if (!firstEnd) { free(input); return 0; }
    int firstLen = (int)(firstEnd - p + 1);
    char* resourcePart = (char*)malloc(firstLen + 1);
    memcpy(resourcePart, p, firstLen);
    resourcePart[firstLen] = '\0';
    int* resourceCount;
    int resourceCountSize = parseIntList(resourcePart, &resourceCount);
    free(resourcePart);

    const char* rest = input + firstLen;
    int groupCount = resourceCountSize;
    int* conflictsSizes = (int*)malloc(groupCount * sizeof(int));
    int*** conflicts = (int***)malloc(groupCount * sizeof(int**));
    for (int i = 0; i < groupCount; i++) {
        const char* start = strchr(rest, '[');
        if (!start) {
            conflictsSizes[i] = 0;
            conflicts[i] = NULL;
            continue;
        }
        const char* end = strchr(start, ']');
        if (!end) end = start;
        int segLen = (int)(end - start + 1);
        char* seg = (char*)malloc(segLen + 1);
        memcpy(seg, start, segLen);
        seg[segLen] = '\0';
        int pairs = 0;
        for (int j = 0; seg[j]; j++) if (seg[j] == '(') pairs++;
        conflictsSizes[i] = pairs;
        conflicts[i] = (int**)malloc(pairs * sizeof(int*));
        for (int j = 0; j < pairs; j++) conflicts[i][j] = (int*)malloc(2 * sizeof(int));
        int pairIndex = 0;
        const char* q = seg;
        while ((q = strchr(q, '(')) != NULL && pairIndex < pairs) {
            q++;
            int a = atoi(q);
            while (*q && *q != ',') q++;
            if (*q == ',') q++;
            int b = atoi(q);
            conflicts[i][pairIndex][0] = a;
            conflicts[i][pairIndex][1] = b;
            pairIndex++;
            q = strchr(q, ')');
            if (!q) break;
            q++;
        }
        free(seg);
        rest = end + 1;
    }
    free(input);

    int returnSize;
    int* ans = canIsolateWithTwoPools(resourceCount, resourceCountSize, conflicts, conflictsSizes, &returnSize);
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", ans[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < resourceCountSize; i++) {
        for (int j = 0; j < conflictsSizes[i]; j++) free(conflicts[i][j]);
        free(conflicts[i]);
    }
    free(conflicts);
    free(conflictsSizes);
    free(resourceCount);
    free(ans);
    return 0;
}
