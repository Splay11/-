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

int peakConcurrent(int* starts, int startsSize, int* ends, int endsSize);

int main() {
    char* line1 = (char*)malloc(MAX_LEN);
    char* line2 = (char*)malloc(MAX_LEN);
    if (!line1 || !line2) return 1;
    if (!fgets(line1, MAX_LEN, stdin)) { free(line1); free(line2); return 0; }
    if (!fgets(line2, MAX_LEN, stdin)) { free(line1); free(line2); return 0; }
    trim_nl(line1);
    trim_nl(line2);
    int ns = 0, ne = 0;
    int* starts = parseIntList(line1, &ns);
    int* ends = parseIntList(line2, &ne);
    printf("%d\n", peakConcurrent(starts, ns, ends, ne));
    free(starts);
    free(ends);
    free(line1);
    free(line2);
    return 0;
}
