#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

int* findMaintenanceWindow(int n, int w, int* scores, int* returnSize);

static int* parseIntList(const char* s, int* outCount) {
    *outCount = 0;
    int* arr = (int*)malloc(MAX_LEN * sizeof(int));
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c >= '0' && c <= '9')) {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                arr[*outCount] = num;
                (*outCount)++;
                num = 0;
                inNum = false;
            }
        }
    }
    if (inNum) {
        arr[*outCount] = num;
        (*outCount)++;
    }
    return arr;
}

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // Parse n, w before the array
    int comma1 = -1, comma2 = -1;
    bool inBracket = false;
    for (int i = 0; i < len; i++) {
        if (line[i] == '[') { inBracket = true; break; }
        if (line[i] == ',') {
            if (comma1 == -1) comma1 = i;
            else if (comma2 == -1) comma2 = i;
        }
    }
    if (comma2 == -1) comma2 = comma1 + 1;

    char numStr1[50], numStr2[50];
    strncpy(numStr1, line, comma1);
    numStr1[comma1] = '\0';
    int n = atoi(numStr1);

    strncpy(numStr2, line + comma1 + 1, comma2 - comma1 - 1);
    numStr2[comma2 - comma1 - 1] = '\0';
    int w = atoi(numStr2);

    const char* arrStr = strchr(line, '[');
    int arrSize;
    int* scores = parseIntList(arrStr, &arrSize);

    int returnSize = 0;
    int* result = findMaintenanceWindow(n, w, scores, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", result[i]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");

    free(scores);
    free(result);
    return 0;
}
