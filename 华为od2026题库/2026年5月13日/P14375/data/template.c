#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 2000000
#define INIT_ROWS 1024

static char*** parse2DStringList(const char* s, int* outRowCount) {
    int resCap = INIT_ROWS;
    char*** res = (char***)malloc(resCap * sizeof(char**));
    *outRowCount = 0;
    int i = 0;
    while (s[i]) {
        while (s[i] && s[i] != '[') i++;
        if (!s[i]) break;
        i++;
        // 跳过空数组（如 "[]"）
        if (s[i] == ']') {
            i++;
            if (s[i] == ',') i++;
            continue;
        }
        char cur[1024];
        int curLen = 0;
        bool inString = false;
        int colCap = 16;
        char** row = (char**)malloc(colCap * sizeof(char*));
        int colCount = 0;
        for (; s[i]; i++) {
            char c = s[i];
            if (c == '"') {
                if (inString) {
                    cur[curLen] = '\0';
                    if (colCount >= colCap) {
                        colCap *= 2;
                        row = (char**)realloc(row, colCap * sizeof(char*));
                    }
                    row[colCount] = (char*)malloc(curLen + 1);
                    strcpy(row[colCount], cur);
                    colCount++;
                    curLen = 0;
                }
                inString = !inString;
            } else if (inString) {
                if (curLen < 1023) cur[curLen++] = c;
            } else if (c == ']') {
                break;
            }
        }
        if (colCount == 0) {
            free(row);
        } else {
            row = (char**)realloc(row, (colCount + 1) * sizeof(char*));
            row[colCount] = NULL;
            if (*outRowCount >= resCap) {
                resCap *= 2;
                res = (char***)realloc(res, resCap * sizeof(char**));
            }
            res[*outRowCount] = row;
            (*outRowCount)++;
        }
        while (s[i] && s[i] != '[' && s[i] != '\0') {
            if (s[i] == ']') break;
            i++;
        }
        if (!s[i]) break;
        if (s[i] == ']' && s[i+1] != ',') break;
    }
    return res;
}

int main() {
    char* input = (char*)malloc(MAX_LEN);
    if (!input) return 0;
    if (!fgets(input, MAX_LEN, stdin)) { free(input); return 0; }
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';

    char* p = input;
    char* firstComma = NULL;
    int bracketLevel = 0;
    for (int i = 0; input[i]; i++) {
        if (input[i] == '[') bracketLevel++;
        else if (input[i] == ']') bracketLevel--;
        else if (input[i] == ',' && bracketLevel == 0) {
            firstComma = &input[i];
            break;
        }
    }
    if (!firstComma) return 0;
    *firstComma = '\0';
    char* secondPart = firstComma + 1;

    char* secondComma = NULL;
    bracketLevel = 0;
    for (int i = 0; secondPart[i]; i++) {
        if (secondPart[i] == '[') bracketLevel++;
        else if (secondPart[i] == ']') bracketLevel--;
        else if (secondPart[i] == ',' && bracketLevel == 0) {
            secondComma = &secondPart[i];
            break;
        }
    }
    if (!secondComma) return 0;
    *secondComma = '\0';
    char* thirdPart = secondComma + 1;

    char* thirdComma = strchr(thirdPart, ',');
    if (!thirdComma) return 0;
    *thirdComma = '\0';
    char* fourthPart = thirdComma + 1;

    // 从 thirdPart 中提取 myId（去掉引号）
    char* q = thirdPart;
    while (*q == ' ' || *q == '\t' || *q == '"') q++;
    char myId[64];
    int idLen = 0;
    while (*q && *q != '"') {
        myId[idLen++] = *q;
        q++;
    }
    myId[idLen] = '\0';

    // 从 fourthPart 中提取 maxHop
    while (*fourthPart == ' ' || *fourthPart == '\t') fourthPart++;
    int maxHop = atoi(fourthPart);

    int nodesSize, relationsSize;
    char*** nodes = parse2DStringList(p, &nodesSize);
    char*** relations = parse2DStringList(secondPart, &relationsSize);

    int returnSize = 0;
    char*** result = queryFriends(nodes, nodesSize, relations, relationsSize, myId, maxHop, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("[");
        int j = 0;
        while (result[i][j]) {
            printf("\"%s\"", result[i][j]);
            if (result[i][j + 1]) printf(",");
            j++;
        }
        printf("]");
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < nodesSize; i++) {
        int j = 0;
        while (nodes[i][j]) { free(nodes[i][j]); j++; }
        free(nodes[i]);
    }
    free(nodes);
    for (int i = 0; i < relationsSize; i++) {
        int j = 0;
        while (relations[i][j]) { free(relations[i][j]); j++; }
        free(relations[i]);
    }
    free(relations);
    if (result) {
        for (int i = 0; i < returnSize; i++) {
            int j = 0;
            while (result[i][j]) { free(result[i][j]); j++; }
            free(result[i]);
        }
        free(result);
    }
    free(input);
    return 0;
}
