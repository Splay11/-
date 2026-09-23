#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 2000000
#define MAX_N 200000

static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_N * sizeof(int));
    *outCount = 0;
    int i = 0;
    while (s[i] && s[i] != '[') i++;
    if (!s[i]) return res;
    i++;
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        int sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        long long v = 0;
        int have = 0;
        while (s[i] >= '0' && s[i] <= '9') {
            v = v * 10 + (s[i] - '0');
            have = 1;
            i++;
        }
        if (have) res[(*outCount)++] = (int)(sign * v);
        else i++;
    }
    return res;
}

int* finishTimes(int* arrival, int arrivalSize, int* duration, int durationSize,
                 int* priority, int prioritySize, int* returnSize);

int main() {
    char l1[MAX_LEN], l2[MAX_LEN], l3[MAX_LEN];
    if (!fgets(l1, MAX_LEN, stdin)) return 0;
    if (!fgets(l2, MAX_LEN, stdin)) return 0;
    if (!fgets(l3, MAX_LEN, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); trim_nl(l3);
    int aSize=0,dSize=0,pSize=0;
    int* arrival = parseIntList(l1, &aSize);
    int* duration = parseIntList(l2, &dSize);
    int* priority = parseIntList(l3, &pSize);
    int returnSize = 0;
    int* ans = finishTimes(arrival, aSize, duration, dSize, priority, pSize, &returnSize);
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(", ");
        printf("%d", ans[i]);
    }
    printf("]\n");
    free(arrival); free(duration); free(priority); free(ans);
    return 0;
}
