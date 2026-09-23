#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000
#define MAX_TOKENS 1000

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c >= '0' && c <= '9')) {
            num = num * 10 + (c - '0');
            inNum = true;
        } else if (inNum) {
            res[*outCount] = num;
            (*outCount)++;
            num = 0;
            inNum = false;
        }
    }
    if (inNum) {
        res[*outCount] = num;
        (*outCount)++;
    }
    return res;
}

int countValidPlans(int* timestamps, int timestampsSize, int minInterval);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    char* commaPos = strrchr(line, ',');
    int minInterval = atoi(commaPos + 1);

    char arrStr[MAX_LEN];
    strncpy(arrStr, line, commaPos - line);
    arrStr[commaPos - line] = '\0';

    int timestampsSize;
    int* timestamps = parseIntList(arrStr, &timestampsSize);

    int result = countValidPlans(timestamps, timestampsSize, minInterval);
    printf("%d\n", result);

    free(timestamps);
    return 0;
}
