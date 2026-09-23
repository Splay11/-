#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 1000000

static int* parseIntArray(const char* s, int* outCount) {
    int* arr = (int*)malloc(MAX_LEN * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
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

int* longestBeautifulLanterns(int* nums, int numsSize, int* returnSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 1;
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int numsSize;
    int* nums = parseIntArray(line, &numsSize);

    int returnSize;
    int* res = longestBeautifulLanterns(nums, numsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", res[i]);
        if (i < returnSize - 1) printf(",");
    }
    printf("]\n");

    free(nums);
    free(res);
    free(line);
    return 0;
}
