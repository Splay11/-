#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 3000000
#define MAX_N 100000

int MaxPlayers(int playerCount, int** playerTimeRange, int playerTimeRangeSize);

static int** parseIntervals(const char* s, int* outCount) {
    int** res = (int**)malloc(MAX_N * sizeof(int*));
    *outCount = 0;
    const char* p = s;
    while (*p) {
        if (*p == '[') {
            while (*p == '[') p++;
            char* end;
            int start = (int)strtol(p, &end, 10);
            int finish = (int)strtol(end + 1, NULL, 10);
            res[*outCount] = (int*)malloc(2 * sizeof(int));
            res[*outCount][0] = start;
            res[*outCount][1] = finish;
            (*outCount)++;
        } else {
            p++;
        }
    }
    return res;
}

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }

    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    // find comma between n and intervals
    int comma = 0;
    bool inBracket = false;
    for (int i = 0; i < len; i++) {
        if (line[i] == '[') inBracket = true;
        if (!inBracket && line[i] == ',') { comma = i; break; }
    }
    int playerCount = atoi(line);

    const char* rest = line + comma + 1;
    int rangeSize;
    int** ranges = parseIntervals(rest, &rangeSize);

    int result = MaxPlayers(playerCount, ranges, rangeSize);
    printf("%d\n", result);

    for (int i = 0; i < rangeSize; i++) free(ranges[i]);
    free(ranges);
    free(line);
    return 0;
}
