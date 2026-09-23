#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LEN 4000000
#define MAX_N 200000
static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_N * sizeof(int)); *outCount = 0; int i = 0;
    while (s[i] && s[i] != '[') i++; if (!s[i]) return res; i++;
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        int sign = 1; if (s[i] == '-') { sign = -1; i++; }
        long long v = 0; int have = 0;
        while (s[i] >= '0' && s[i] <= '9') { v = v * 10 + (s[i] - '0'); have = 1; i++; }
        if (have) res[(*outCount)++] = (int)(sign * v); else i++;
    }
    return res;
}
static int** parseInt2D(const char* s, int* outRows, int** outColSizes) {
    int** rows = (int**)malloc(MAX_N * sizeof(int*));
    int* colSizes = (int*)malloc(MAX_N * sizeof(int));
    *outRows = 0; int i = 0;
    while (s[i] && s[i] != '[') i++;
    if (!s[i]) { *outColSizes = colSizes; return rows; }
    i++;
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        if (s[i] != '[') { i++; continue; }
        i++;
        int* row = (int*)malloc(8 * sizeof(int)); int cnt = 0, cap = 8;
        while (s[i]) {
            while (s[i] == ' ' || s[i] == ',') i++;
            if (s[i] == ']' || !s[i]) { if (s[i] == ']') i++; break; }
            int sign = 1; if (s[i] == '-') { sign = -1; i++; }
            long long v = 0; int have = 0;
            while (s[i] >= '0' && s[i] <= '9') { v = v * 10 + (s[i] - '0'); have = 1; i++; }
            if (have) {
                if (cnt >= cap) { cap *= 2; row = (int*)realloc(row, cap * sizeof(int)); }
                row[cnt++] = (int)(sign * v);
            } else i++;
        }
        rows[*outRows] = row; colSizes[*outRows] = cnt; (*outRows)++;
    }
    *outColSizes = colSizes; return rows;
}

int maxMaintenanceScore(int** windows, int windowsSize, int* windowsColSize);
int main() {
    char* l1=(char*)malloc(MAX_LEN);
    if (!fgets(l1, MAX_LEN, stdin)) return 0;
    trim_nl(l1);
    int rows=0; int* col=NULL; int** a=parseInt2D(l1,&rows,&col);
    printf("%d\n", maxMaintenanceScore(a, rows, col));
    for(int i=0;i<rows;i++) free(a[i]); free(a); free(col); free(l1); return 0;
}
