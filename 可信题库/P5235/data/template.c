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

char* hasFiveInRow(int** blackChessPoses, int blackChessPosesSize, int* blackChessPosesColSize);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    trim_nl(line);
    int rows = 0;
    int* colSizes = NULL;
    int** pos = parseInt2D(line, &rows, &colSizes);
    char* ans = hasFiveInRow(pos, rows, colSizes);
    printf("\"%s\"\n", ans ? ans : "");
    freeInt2D(pos, rows);
    free(colSizes);
    free(ans);
    return 0;
}
