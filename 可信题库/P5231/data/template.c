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

char* packFields(int* sectionWidth, int sectionWidthSize, int* sectionValues, int sectionValuesSize);

int main() {
    char line1[MAX_LEN], line2[MAX_LEN];
    if (!fgets(line1, MAX_LEN, stdin)) return 0;
    if (!fgets(line2, MAX_LEN, stdin)) return 0;
    trim_nl(line1);
    trim_nl(line2);
    int wSize = 0, vSize = 0;
    int* sectionWidth = parseIntList(line1, &wSize);
    int* sectionValues = parseIntList(line2, &vSize);
    char* ans = packFields(sectionWidth, wSize, sectionValues, vSize);
    printf("\"%s\"\n", ans ? ans : "");
    free(sectionWidth);
    free(sectionValues);
    free(ans);
    return 0;
}
