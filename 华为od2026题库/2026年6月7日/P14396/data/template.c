#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(1000 * sizeof(int));
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

int maximumProfit(int* duration, int* deadline, int* profit, int n);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int firstComma = -1;
    int bracket1 = -1, bracket2 = -1, bracket3 = -1;
    int bracketCount = 0;
    for (int i = 0; i < len; i++) {
        if (line[i] == ',' && firstComma == -1) firstComma = i;
        if (line[i] == '[') {
            bracketCount++;
            if (bracketCount == 1) bracket1 = i;
            else if (bracketCount == 2) bracket2 = i;
            else if (bracketCount == 3) bracket3 = i;
        }
    }

    int n = atoi(line);
    char* p1 = strchr(line, '[');
    char* p2 = strchr(p1 + 1, '[');
    char* p3 = strchr(p2 + 1, '[');

    int count1, count2, count3;
    int* duration = parseIntList(p1, &count1);
    int* deadline = parseIntList(p2, &count2);
    int* profit = parseIntList(p3, &count3);

    int result = maximumProfit(duration, deadline, profit, n);
    printf("%d\n", result);

    free(duration);
    free(deadline);
    free(profit);
    return 0;
}
