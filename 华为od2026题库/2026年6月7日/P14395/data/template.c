#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000
#define MAX_TOKENS 1000

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

char** filterValidAClassIPs(char** ips, int ipsSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int ipsSize;
    char** ips = parseStringList(line, &ipsSize);

    int returnSize = 0;
    char** result = filterValidAClassIPs(ips, ipsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("\"%s\"", result[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < ipsSize; i++) free(ips[i]);
    free(ips);
    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);
    return 0;
}
