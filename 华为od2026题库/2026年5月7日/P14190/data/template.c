#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2000000

long long minProcessTime(int* goodProceeTime, int goodProceeTimeSize, int optimize);

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_LEN * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-' || (c >= '0' && c <= '9')) {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                res[*outCount] = num;
                (*outCount)++;
                num = 0;
                inNum = false;
            }
        }
    }
    if (inNum) {
        res[*outCount] = num;
        (*outCount)++;
    }
    return res;
}

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 0;
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    char* numsStr = (char*)malloc(MAX_LEN);
    int bracketEnd = 0;
    for (int i = 0; i < len; i++) {
        if (line[i] == ']') {
            bracketEnd = i;
            break;
        }
    }
    strncpy(numsStr, line, bracketEnd + 1);
    numsStr[bracketEnd + 1] = '\0';
    int goodProceeTimeSize;
    int* goodProceeTime = parseIntList(numsStr, &goodProceeTimeSize);

    const char* rest = line + bracketEnd + 1;
    while (*rest == ',' || *rest == ' ' || *rest == '\t')
        rest++;
    int optimize = atoi(rest);

    long long result = minProcessTime(goodProceeTime, goodProceeTimeSize, optimize);
    printf("%lld\n", result);
    free(line);
    free(numsStr);
    free(goodProceeTime);
    return 0;
}
