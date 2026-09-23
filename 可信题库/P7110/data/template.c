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

int minPassDays(int* slots, int slotsSize, int* prep, int prepSize);

int main() {
    char* l1 = (char*)malloc(MAX_LEN);
    char* l2 = (char*)malloc(MAX_LEN);
    if (!fgets(l1, MAX_LEN, stdin)) return 0;
    if (!fgets(l2, MAX_LEN, stdin)) return 0;
    trim_nl(l1); trim_nl(l2);
    int n = 0, m = 0;
    int* slots = parseIntList(l1, &n);
    int* prep = parseIntList(l2, &m);
    printf("%d\n", minPassDays(slots, n, prep, m));
    free(slots); free(prep); free(l1); free(l2);
    return 0;
}
