#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

int* warehouseInventory(int* items, int itemsSize, int* returnSize);

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(1000 * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    bool neg = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') {
            neg = true;
        } else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                res[*outCount] = neg ? -num : num;
                (*outCount)++;
                num = 0;
                inNum = false;
                neg = false;
            }
        }
    }
    if (inNum) {
        res[*outCount] = neg ? -num : num;
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

    int itemsSize;
    int* items = parseIntList(line, &itemsSize);

    int returnSize;
    int* result = warehouseInventory(items, itemsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("%d", result[i]);
    }
    printf("]\n");

    free(items);
    free(result);
    return 0;
}
