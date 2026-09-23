#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2048
#define MAX_TOKENS 8

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char cur[MAX_LEN];
    int curLen = 0;
    bool inString = false;

    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '"') {
            if (inString) {
                cur[curLen] = '\0';
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
            inString = !inString;
        } else if (inString) {
            cur[curLen++] = c;
        }
    }
    return res;
}

char** magicFragments(char** fragments, int fragmentsSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int fragmentsSize;
    char** fragments = parseStringList(line, &fragmentsSize);

    int returnSize = 0;
    char** result = magicFragments(fragments, fragmentsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("\"%s\"", result[i]);
    }
    printf("]\n");

    for (int i = 0; i < fragmentsSize; i++) free(fragments[i]);
    free(fragments);
    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);

    return 0;
}
