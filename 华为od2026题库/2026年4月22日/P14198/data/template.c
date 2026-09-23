#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 500000
#define MAX_TOKENS 10000

static char** parseStringList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_TOKENS * sizeof(char*));
    *outCount = 0;
    char* cur = (char*)malloc(MAX_LEN);
    int curLen = 0;
    bool inString = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '"') {
            if (inString) {
                cur[curLen] = '\0';
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
            inString = !inString;
        } else if (inString) {
            cur[curLen++] = c;
        }
    }
    free(cur);
    return res;
}

char* getClassMonitor(char** names, int namesSize, char** ballotTickets, int ballotTicketsSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    char* split = strstr(line, "],[");
    if (!split) { free(line); return 0; }
    int pos = (int)(split - line);
    char* namesStr = (char*)malloc(pos + 2);
    strncpy(namesStr, line, pos + 1);
    namesStr[pos + 1] = '\0';
    char* ballotsStr = line + pos + 2;

    int namesSize, ballotsSize;
    char** names = parseStringList(namesStr, &namesSize);
    char** ballots = parseStringList(ballotsStr, &ballotsSize);

    char* result = getClassMonitor(names, namesSize, ballots, ballotsSize);
    printf("\"%s\"\n", result);

    for (int i = 0; i < namesSize; i++) free(names[i]);
    for (int i = 0; i < ballotsSize; i++) free(ballots[i]);
    free(names);
    free(ballots);
    free(namesStr);
    free(line);
    return 0;
}
