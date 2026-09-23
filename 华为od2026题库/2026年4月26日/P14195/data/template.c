#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 500000
#define MAX_TOKENS 1000

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char* cur = (char*)malloc(MAX_LEN);
    int curLen = 0;
    bool inStr = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '"') {
            if (inStr) {
                cur[curLen] = '\0';
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
            inStr = !inStr;
        } else if (inStr) {
            cur[curLen++] = c;
        }
    }
    free(cur);
    return res;
}

static char*** parseDeps(const char* s, int* outCount) {
    char*** res = (char***)malloc(MAX_TOKENS * sizeof(char**));
    *outCount = 0;
    int i = 0;
    // skip outer [
    while (s[i] && s[i] != '[') i++;
    if (s[i] == '[') i++;
    while (s[i]) {
        // 检测内层 [ 作为新 pair 的开始
        if (s[i] == '[') {
            i++; // skip [
            char** pair = (char**)malloc(MAX_TOKENS * sizeof(char*));
            int pairCnt = 0;
            char* cur = (char*)malloc(MAX_LEN);
            int curLen = 0;
            bool inStr = false;
            while (s[i] && !(s[i] == ']' && !inStr)) {
                char c = s[i];
                if (c == '"') {
                    if (inStr) {
                        cur[curLen] = '\0';
                        pair[pairCnt] = (char*)malloc(curLen + 1);
                        strcpy(pair[pairCnt], cur);
                        pairCnt++;
                        curLen = 0;
                    }
                    inStr = !inStr;
                } else if (inStr) {
                    cur[curLen++] = c;
                }
                i++;
            }
            free(cur);
            if (s[i] == ']') i++; // skip ]
            res[*outCount] = (char**)malloc(pairCnt * sizeof(char*));
            for (int k = 0; k < pairCnt; k++) {
                res[*outCount][k] = pair[k];
            }
            (*outCount)++;
            free(pair);
        } else {
            i++;
        }
    }
    return res;
}

char** allBuildOrders(char** modules, int modulesSize, char*** dependencies, int dependenciesSize, int* returnSize);

int main() {
    char* input = (char*)malloc(MAX_LEN);
    if (!fgets(input, MAX_LEN, stdin)) { free(input); return 0; }
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';
    char* comma = NULL;
    int bracketDepth = 0;
    bool inQuotes = false;
    for (int i = 0; i < len; i++) {
        if (input[i] == '"') inQuotes = !inQuotes;
        else if (!inQuotes) {
            if (input[i] == '[') bracketDepth++;
            else if (input[i] == ']') bracketDepth--;
            else if (input[i] == ',' && bracketDepth == 0) {
                comma = &input[i];
                break;
            }
        }
    }
    if (!comma) { free(input); return 0; }
    int modulesPartLen = (int)(comma - input);
    char* modulesPart = (char*)malloc(modulesPartLen + 1);
    strncpy(modulesPart, input, modulesPartLen);
    modulesPart[modulesPartLen] = '\0';
    const char* depsPart = comma + 1;
    while (*depsPart == ' ' || *depsPart == ',') depsPart++;

    int modulesSize;
    char** modules = parseStringList(modulesPart, &modulesSize);
    int depsSize;
    char*** deps = parseDeps(depsPart, &depsSize);

    int returnSize;
    char** result = allBuildOrders(modules, modulesSize, deps, depsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("\"%s\"", result[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < modulesSize; i++) free(modules[i]);
    free(modules);
    for (int i = 0; i < depsSize; i++) {
        for (int j = 0; j < 2; j++) free(deps[i][j]);
        free(deps[i]);
    }
    free(deps);
    if (result) {
        for (int i = 0; i < returnSize; i++) free(result[i]);
        free(result);
    }
    free(input);
    free(modulesPart);
    return 0;
}
