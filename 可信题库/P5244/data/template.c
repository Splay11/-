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

int minComputeCost(int* load, int loadSize, int runCost, int changeCost, int maxChanges);

int main() {
    char line[MAX_LEN], l2[64], l3[64], l4[64];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    if (!fgets(l2, sizeof(l2), stdin)) return 0;
    if (!fgets(l3, sizeof(l3), stdin)) return 0;
    if (!fgets(l4, sizeof(l4), stdin)) return 0;
    trim_nl(line); trim_nl(l2); trim_nl(l3); trim_nl(l4);
    int n = 0;
    int* load = parseIntList(line, &n);
    int ans = minComputeCost(load, n, atoi(l2), atoi(l3), atoi(l4));
    printf("%d\n", ans);
    free(load);
    return 0;
}
