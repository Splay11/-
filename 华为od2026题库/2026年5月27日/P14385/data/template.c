#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 2000000
#define INIT_TOKENS 256

static char** parseStringList(const char* s, int* outCount) {
    int cap = INIT_TOKENS;
    char** res = (char**)malloc(cap * sizeof(char*));
    *outCount = 0;
    char cur[1024];
    int curLen = 0;
    bool inString = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '"') {
            if (inString) {
                cur[curLen] = '\0';
                if (*outCount >= cap) {
                    cap *= 2;
                    res = (char**)realloc(res, cap * sizeof(char*));
                }
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
            inString = !inString;
        } else if (inString) {
            if (curLen < 1023) cur[curLen++] = c;
        }
    }
    return res;
}

char* electMonitor(char** students, int studentsSize, char** votes, int votesSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 0;
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // find the delimiter between two lists
    char* split = strstr(line, "],[");
    if (!split) { free(line); return 0; }
    int splitPos = (int)(split - line);

    // split in place: null-terminate the first list
    line[splitPos + 1] = '\0';
    const char* studentsStr = line;
    const char* votesStr = line + splitPos + 2;

    int studentsSize, votesSize;
    char** students = parseStringList(studentsStr, &studentsSize);
    char** votes = parseStringList(votesStr, &votesSize);

    char* result = electMonitor(students, studentsSize, votes, votesSize);
    printf("\"%s\"\n", result);

    for (int i = 0; i < studentsSize; i++) free(students[i]);
    for (int i = 0; i < votesSize; i++) free(votes[i]);
    free(students);
    free(votes);
    free(line);
    return 0;
}
