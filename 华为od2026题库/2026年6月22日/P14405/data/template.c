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
    char numBuf[100];
    int numLen = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c == '-' || (c >= '0' && c <= '9'))) {
            numBuf[numLen++] = c;
            inNum = true;
        } else {
            if (inNum) {
                numBuf[numLen] = '\0';
                res[*outCount] = atoi(numBuf);
                (*outCount)++;
                numLen = 0;
                inNum = false;
            }
        }
    }
    if (inNum) {
        numBuf[numLen] = '\0';
        res[*outCount] = atoi(numBuf);
        (*outCount)++;
    }
    return res;
}

int minimumLatency(int* nums, int numsSize, int k);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    char numsStr[MAX_LEN];
    int k;
    const char* commaPos = strrchr(line, ',');
    if (commaPos) {
        k = atoi(commaPos + 1);
        int arrayLen = (int)(commaPos - line);
        strncpy(numsStr, line, arrayLen);
        numsStr[arrayLen] = '\0';
    } else {
        numsStr[0] = '\0';
        k = 0;
    }

    int numsSize;
    int* nums = parseIntList(numsStr, &numsSize);

    int result = minimumLatency(nums, numsSize, k);
    printf("%d\n", result);

    free(nums);
    return 0;
}
