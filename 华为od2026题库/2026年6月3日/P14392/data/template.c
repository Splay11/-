#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000
#define MAX_TOKENS 2000

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    bool isNeg = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') {
            isNeg = true;
        } else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                res[*outCount] = isNeg ? -num : num;
                (*outCount)++;
                num = 0;
                inNum = false;
                isNeg = false;
            }
        }
    }
    if (inNum) {
        res[*outCount] = isNeg ? -num : num;
        (*outCount)++;
    }
    return res;
}

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    const char* comma2 = strrchr(line, ',');
    int targetId = atoi(comma2 + 1);

    char firstPart[MAX_LEN], secondPart[MAX_LEN];
    int commaPos = 0;
    int bracketCount = 0;
    bool foundSplit = false;
    for (int i = 0; line[i]; i++) {
        if (line[i] == '[') bracketCount++;
        if (line[i] == ']') bracketCount--;
        if (line[i] == ',' && bracketCount == 0) {
            commaPos = i;
            foundSplit = true;
            break;
        }
    }
    strncpy(firstPart, line, commaPos);
    firstPart[commaPos] = '\0';
    strcpy(secondPart, line + commaPos + 1);
    char* pTargetComma = strrchr(secondPart, ',');
    if (pTargetComma) *pTargetComma = '\0';

    int fileIdsSize, parentIdsSize;
    int* fileIds = parseIntList(firstPart, &fileIdsSize);
    int* parentIds = parseIntList(secondPart, &parentIdsSize);

    int returnSize = 0;
    int* res = getLoadedFileIds(fileIds, fileIdsSize, parentIds, parentIdsSize, targetId, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", res[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    free(fileIds);
    free(parentIds);
    free(res);
    return 0;
}
