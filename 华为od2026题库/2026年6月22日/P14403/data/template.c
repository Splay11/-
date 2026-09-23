#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 200000
#define MAX_TOKENS 5000

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

int* analyzeLogKeywords(char** logs, int logsSize, char** keywords, int keywordsSize, int* returnSize);

int main() {
    char input[MAX_LEN];
    if (!fgets(input, MAX_LEN, stdin)) return 0;
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';

    // Find the separating "],[" pattern between logs list and keywords list
    char* split = strstr(input, "],[");
    if (!split) return 0;
    int splitPos = (int)(split - input);

    char logsStr[MAX_LEN], keywordsStr[MAX_LEN];
    strncpy(logsStr, input, splitPos + 1);
    logsStr[splitPos + 1] = '\0';
    strcpy(keywordsStr, input + splitPos + 2);

    // Remove trailing commas or brackets
    len = strlen(keywordsStr);
    while (len > 0 && (keywordsStr[len - 1] == '\n' || keywordsStr[len - 1] == '\r')) keywordsStr[--len] = '\0';

    int logsSize, keywordsSize;
    char** logs = parseStringList(logsStr, &logsSize);
    char** keywords = parseStringList(keywordsStr, &keywordsSize);

    int returnSize = 0;
    int* result = analyzeLogKeywords(logs, logsSize, keywords, keywordsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", result[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < logsSize; i++) free(logs[i]);
    for (int i = 0; i < keywordsSize; i++) free(keywords[i]);
    free(logs);
    free(keywords);
    free(result);
    return 0;
}
