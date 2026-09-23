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

int minFinishTime(int n, int* prev, int prevSize, int* next, int nextSize, int* time, int timeSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 1;
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    trim_nl(line);
    int n = atoi(line);

    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    trim_nl(line);
    int prevSize = 0;
    int* prev = parseIntList(line, &prevSize);

    if (!fgets(line, MAX_LEN, stdin)) { free(line); free(prev); return 0; }
    trim_nl(line);
    int nextSize = 0;
    int* next = parseIntList(line, &nextSize);

    if (!fgets(line, MAX_LEN, stdin)) { free(line); free(prev); free(next); return 0; }
    trim_nl(line);
    int timeSize = 0;
    int* time = parseIntList(line, &timeSize);

    printf("%d\n", minFinishTime(n, prev, prevSize, next, nextSize, time, timeSize));
    free(prev);
    free(next);
    free(time);
    free(line);
    return 0;
}
