#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 4000000
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

int sumPeakRisk(int* loads, int loadsSize);

int main() {
    char* line1 = (char*)malloc(MAX_LEN);
    if (!line1) return 1;
    if (!fgets(line1, MAX_LEN, stdin)) { free(line1); return 0; }
    trim_nl(line1);
    int n = 0;
    int* loads = parseIntList(line1, &n);
    printf("%d\n", sumPeakRisk(loads, n));
    free(loads);
    free(line1);
    return 0;
}
