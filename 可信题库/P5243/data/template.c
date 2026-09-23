#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 2000000
#define MAX_ROWS 200000

static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}

static int** parseInt2D(const char* s, int* outRows, int** outColSizes) {
    int** rows = (int**)malloc(MAX_ROWS * sizeof(int*));
    int* colSizes = (int*)malloc(MAX_ROWS * sizeof(int));
    *outRows = 0;
    int i = 0;
    while (s[i] && s[i] != '[') i++;
    if (!s[i]) { *outColSizes = colSizes; return rows; }
    i++; /* outer [ */
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        if (s[i] != '[') { i++; continue; }
        i++; /* inner [ */
        int* row = (int*)malloc(64 * sizeof(int));
        int cnt = 0, cap = 64;
        while (s[i]) {
            while (s[i] == ' ' || s[i] == ',') i++;
            if (s[i] == ']' || !s[i]) { if (s[i] == ']') i++; break; }
            int sign = 1;
            if (s[i] == '-') { sign = -1; i++; }
            long long v = 0;
            int have = 0;
            while (s[i] >= '0' && s[i] <= '9') {
                v = v * 10 + (s[i] - '0');
                have = 1;
                i++;
            }
            if (have) {
                if (cnt >= cap) {
                    cap *= 2;
                    row = (int*)realloc(row, cap * sizeof(int));
                }
                row[cnt++] = (int)(sign * v);
            } else i++;
        }
        rows[*outRows] = row;
        colSizes[*outRows] = cnt;
        (*outRows)++;
    }
    *outColSizes = colSizes;
    return rows;
}

static void freeInt2D(int** rows, int n) {
    for (int i = 0; i < n; i++) free(rows[i]);
    free(rows);
}

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(200000 * sizeof(int));
    *outCount = 0;
    int i = 0;
    while (s[i] && s[i] != '[') i++;
    if (!s[i]) return res;
    i++;
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        int sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        long long v = 0; int have = 0;
        while (s[i] >= '0' && s[i] <= '9') { v = v * 10 + (s[i] - '0'); have = 1; i++; }
        if (have) res[(*outCount)++] = (int)(sign * v); else i++;
    }
    return res;
}

int minRebuildTime(int n, int** deps, int depsSize, int* depsColSize,
                   int* buildTime, int buildTimeSize, int* changed, int changedSize);

int main() {
    char l0[64], l1[MAX_LEN], l2[MAX_LEN], l3[MAX_LEN];
    if (!fgets(l0, sizeof(l0), stdin)) return 0;
    if (!fgets(l1, MAX_LEN, stdin)) return 0;
    if (!fgets(l2, MAX_LEN, stdin)) return 0;
    if (!fgets(l3, MAX_LEN, stdin)) return 0;
    trim_nl(l0); trim_nl(l1); trim_nl(l2); trim_nl(l3);
    int n = atoi(l0);
    int depsSize = 0; int* depsCol = NULL;
    int** deps = parseInt2D(l1, &depsSize, &depsCol);
    int btSize = 0, chSize = 0;
    int* buildTime = parseIntList(l2, &btSize);
    int* changed = parseIntList(l3, &chSize);
    printf("%d\n", minRebuildTime(n, deps, depsSize, depsCol, buildTime, btSize, changed, chSize));
    freeInt2D(deps, depsSize);
    free(depsCol); free(buildTime); free(changed);
    return 0;
}
