#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000
#define MAX_TOKENS 10000

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
        } else if (c == '-' ) {
            num = 0;
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

static int** parseInt2DList(const char* s, int* outRows, int* outCols) {
    int** res = (int**)malloc(MAX_TOKENS * sizeof(int*));
    *outRows = 0;
    *outCols = 2;
    int row[2];
    int idx = 0;
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c >= '0' && c <= '9')) {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                row[idx++] = num;
                num = 0;
                inNum = false;
                if (idx == 2) {
                    res[*outRows] = (int*)malloc(2 * sizeof(int));
                    res[*outRows][0] = row[0];
                    res[*outRows][1] = row[1];
                    (*outRows)++;
                    idx = 0;
                }
            }
        }
    }
    return res;
}

int maxZoneImbalance(int* loads, int loadsSize, int** edges, int edgesSize, int* edgesColSize);

int main() {
    char input[MAX_LEN];
    fgets(input, MAX_LEN, stdin);
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';

    // Find the split between loads and edges
    const char* split = strstr(input, "],[[");
    if (!split) {
        split = strstr(input, "],[]");
    }

    char loadsStr[MAX_LEN];
    char edgesStr[MAX_LEN];
    if (split) {
        int pos = (int)(split - input) + 1;
        strncpy(loadsStr, input, pos);
        loadsStr[pos] = '\0';
        strcpy(edgesStr, input + pos);
    } else {
        strcpy(loadsStr, input);
        edgesStr[0] = '\0';
    }

    int loadsSize;
    int* loads = parseIntList(loadsStr, &loadsSize);

    int edgesSize;
    int edgesColSize;
    int** edges = parseInt2DList(edgesStr, &edgesSize, &edgesColSize);

    int result = maxZoneImbalance(loads, loadsSize, edges, edgesSize, &edgesColSize);
    printf("%d\n", result);

    free(loads);
    for (int i = 0; i < edgesSize; i++) free(edges[i]);
    free(edges);
    return 0;
}
