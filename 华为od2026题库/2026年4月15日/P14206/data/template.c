#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#define MAX_LEN 2500000
#define MAX_TOKENS 100000

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char cur[256];
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

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else if (inNum) {
            res[*outCount] = num;
            (*outCount)++;
            num = 0;
            inNum = false;
        }
    }
    if (inNum) {
        res[*outCount] = num;
        (*outCount)++;
    }
    return res;
}

int main() {
    char* line = (char*)malloc(MAX_LEN);
    int len = (int)read(STDIN_FILENO, line, MAX_LEN - 1);
    line[len] = '\0';
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    char *split = strstr(line, "],[");
    if (!split) {
        printf("[]\n");
        free(line);
        return 0;
    }
    int splitPos = (int)(split - line);

    char* pathsStr = (char*)malloc(MAX_LEN);
    strncpy(pathsStr, line, splitPos + 1);
    pathsStr[splitPos + 1] = '\0';
    const char* respStr = line + splitPos + 2;

    int pathsSize, responseTimesSize, returnSize = 0;
    char** paths = parseStringList(pathsStr, &pathsSize);
    int* responseTimes = parseIntList(respStr, &responseTimesSize);

    int** result = mergeLogs(paths, pathsSize, responseTimes, responseTimesSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("[%d,%d,%d]", result[i][0], result[i][1], result[i][2]);
        if (i < returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < pathsSize; i++) free(paths[i]);
    free(paths);
    free(responseTimes);
    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);
    free(pathsStr);
    free(line);

    return 0;
}
