#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 100000

static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}

static char* parseQuoted(const char* line) {
    const char* a = strchr(line, '"');
    const char* b = strrchr(line, '"');
    if (!a || !b || b <= a) {
        char* r = (char*)malloc(strlen(line) + 1);
        strcpy(r, line);
        return r;
    }
    int n = (int)(b - a - 1);
    char* r = (char*)malloc(n + 1);
    memcpy(r, a + 1, n);
    r[n] = '\0';
    return r;
}

char* sortLetter(char* lettersStr);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    trim_nl(line);
    char* s = parseQuoted(line);
    char* ans = sortLetter(s);
    printf("\"%s\"\n", ans ? ans : "");
    free(s);
    free(ans);
    return 0;
}
