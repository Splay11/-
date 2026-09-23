#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#define MAX_LEN 30000000
#define MAX_PACKETS 1000000

int** processPackets(int n, int k, char** packets, int packetsSize, int* returnSize);

static char* my_strndup(const char* s, int n) {
    char* p = (char*)malloc(n + 1);
    if (!p) return NULL;
    memcpy(p, s, n);
    p[n] = '\0';
    return p;
}

static char** parsePacketList(const char* s, int* outCount) {
    char** res = (char**)malloc(MAX_PACKETS * sizeof(char*));
    *outCount = 0;
    char cur[64];
    int curLen = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c == '[' && s[i+1] != '[')) {
            curLen = 0;
            inNum = true;
        } else if (c == ']') {
            if (inNum) {
                cur[curLen] = '\0';
                res[*outCount] = (char*)malloc(curLen + 1);
                strcpy(res[*outCount], cur);
                (*outCount)++;
                curLen = 0;
            }
            inNum = false;
        } else if (inNum) {
            cur[curLen++] = (c == ',') ? ':' : c;
        }
    }
    return res;
}

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 1;
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 1; }
    int len = strlen(line);
    while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = '\0';

    int n = 0, k = 0;
    int i = 0;
    // parse n
    while (i < len && line[i] != ',') { i++; }
    n = atoi(my_strndup(line, i));
    int startK = i + 1;
    i++;
    while (i < len && line[i] != ',') { i++; }
    k = atoi(my_strndup(line + startK, i - startK));
    const char* listStart = line + i + 1;

    int packetsSize = 0;
    char** packets = parsePacketList(listStart, &packetsSize);

    int returnSize = 0;
    int** result = processPackets(n, k, packets, packetsSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("[");
        int subLen = 0;
        if (result[i]) {
            while (result[i][subLen] != 0) subLen++;
        }
        for (int j = 0; j < subLen; j++) {
            printf("%d", result[i][j]);
            if (j + 1 < subLen) printf(",");
        }
        printf("]");
        if (i + 1 < returnSize) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < packetsSize; i++) free(packets[i]);
    free(packets);
    for (int i = 0; i < returnSize; i++) free(result[i]);
    free(result);
    free(line);
    return 0;
}
