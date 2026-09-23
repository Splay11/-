#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 20000000
#define MAX_N 200000

static char gbuf[MAX_LEN];

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

int main(void) {
    size_t nread = fread(gbuf, 1, MAX_LEN - 1, stdin);
    gbuf[nread] = '\0';
    while (nread > 0 && (gbuf[nread - 1] == '\n' || gbuf[nread - 1] == '\r')) gbuf[--nread] = '\0';
    int n = 0;
    int* desks = parseIntList(gbuf, &n);
    printf("%s\n", canPassBooks(desks, n) ? "true" : "false");
    free(desks);
    return 0;
}
