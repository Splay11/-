#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 2000000
#define MAX_TOKENS 10000

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char* cur = (char*)malloc(MAX_LEN);
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
    free(cur);
    return res;
}

char** findAnomalyLogs(char** logs, int logsSize, int* returnSize);

int main() {
    char* input = (char*)malloc(MAX_LEN);
    fgets(input, MAX_LEN, stdin);
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r'))
        input[--len] = '\0';

    int logsSize;
    char** logs = parseStringList(input, &logsSize);

    int returnSize = 0;
    char** result = findAnomalyLogs(logs, logsSize, &returnSize);

    if (returnSize == 0) {
        printf("NONE\n");
    } else {
        printf("[");
        for (int i = 0; i < returnSize; i++) {
            printf("\"%s\"", result[i]);
            if (i != returnSize - 1) printf(",");
        }
        printf("]\n");
    }

    for (int i = 0; i < logsSize; i++) free(logs[i]);
    free(logs);
    if (result) {
        for (int i = 0; i < returnSize; i++) free(result[i]);
        free(result);
    }
    free(input);
    return 0;
}
