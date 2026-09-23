#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 500000
#define MAX_TOKENS 2500

static char** parse2DLayout(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char* cur = (char*)malloc(MAX_LEN);
    int curLen = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '.' || c == '#') {
            cur[curLen++] = c;
        } else if (c == ']') {
            if (curLen > 0) {
                cur[curLen] = '\0';
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
        }
    }
    free(cur);
    return res;
}

int networkPlanning(char** roomArrangement, int rows);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int count;
    char** roomArrangement = parse2DLayout(line, &count);
    int result = networkPlanning(roomArrangement, count);
    printf("%d\n", result);

    for (int i = 0; i < count; i++) free(roomArrangement[i]);
    free(roomArrangement);
    free(line);
    return 0;
}
