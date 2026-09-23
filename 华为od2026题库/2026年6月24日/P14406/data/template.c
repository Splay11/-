#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 1000000
#define MAX_TOKENS 200000

int countProfilePairs(int* profiles, int profilesSize, int diff);

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool neg = false;
    bool inNum = false;
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
                neg = false;
                inNum = false;
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
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    char* comma = strrchr(line, ',');
    int diff = atoi(comma + 1);

    char arrStr[MAX_LEN];
    strncpy(arrStr, line, comma - line);
    arrStr[comma - line] = '\0';

    int profilesSize;
    int* profiles = parseIntList(arrStr, &profilesSize);

    int result = countProfilePairs(profiles, profilesSize, diff);
    printf("%d\n", result);

    free(profiles);
    return 0;
}
