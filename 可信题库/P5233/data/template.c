#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 200000
#define MAX_N 256

static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r' || isspace((unsigned char)s[len - 1])))
        s[--len] = '\0';
}

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_N * sizeof(char*));
    *outCount = 0;
    int i = 0;
    while (s[i] && isspace((unsigned char)s[i])) i++;
    if (s[i] != '[') return res;
    i++;
    while (s[i]) {
        while (s[i] && (isspace((unsigned char)s[i]) || s[i] == ',')) i++;
        if (s[i] == ']' || !s[i]) break;
        if (s[i] != '"') { i++; continue; }
        i++;
        int start = i;
        while (s[i] && s[i] != '"') i++;
        int len = i - start;
        char* v = (char*)malloc(len + 1);
        memcpy(v, s + start, len);
        v[len] = '\0';
        res[(*outCount)++] = v;
        if (s[i] == '"') i++;
    }
    return res;
}

int countSimilarGroups(char** uriReqs, int uriReqsSize);

int main() {
    char line[MAX_LEN];
    size_t total = 0;
    line[0] = '\0';
    char chunk[4096];
    while (fgets(chunk, sizeof(chunk), stdin)) {
        size_t cl = strlen(chunk);
        if (total + cl >= MAX_LEN - 1) break;
        memcpy(line + total, chunk, cl);
        total += cl;
        line[total] = '\0';
    }
    trim_nl(line);
    if (!line[0]) return 0;
    int n = 0;
    char** uriReqs = parseStringList(line, &n);
    printf("%d\n", countSimilarGroups(uriReqs, n));
    for (int i = 0; i < n; i++) free(uriReqs[i]);
    free(uriReqs);
    return 0;
}
