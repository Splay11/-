#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

static int* parseIntArray(const char* s, int* outCount) {
    int* arr = (int*)malloc(MAX_LEN * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false, neg = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') {
            neg = true;
        } else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                arr[*outCount] = neg ? -num : num;
                (*outCount)++;
                num = 0;
                inNum = false;
                neg = false;
            }
        }
    }
    if (inNum) {
        arr[*outCount] = neg ? -num : num;
        (*outCount)++;
    }
    return arr;
}

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int typeSize;
    int* type = parseIntArray(line, &typeSize);

    int result = longestValidSkillChain(type, typeSize);
    printf("%d\n", result);

    free(type);
    return 0;
}
