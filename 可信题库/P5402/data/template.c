#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 8000000
#define MAX_N 305

static char gbuf[MAX_LEN];
static char trows[MAX_N][MAX_N + 1];
static char srows[MAX_N][MAX_N + 1];
static char* tptr[MAX_N];
static char* sptr[MAX_N];

static void skip_ws(const char* s, int* i) {
    while (s[*i] && isspace((unsigned char)s[*i])) (*i)++;
}

static int parseBoard(const char* s, char rows[MAX_N][MAX_N + 1], char** ptr, int* outM, int* outN) {
    int i = 0;
    skip_ws(s, &i);
    if (s[i++] != '[') return 0;
    int m = 0, n = -1;
    while (s[i]) {
        skip_ws(s, &i);
        if (s[i] == ']') break;
        if (s[i] == ',') { i++; continue; }
        if (s[i++] != '[') return 0;
        int col = 0;
        while (s[i]) {
            skip_ws(s, &i);
            if (s[i] == ']') { i++; break; }
            if (s[i] == ',') { i++; continue; }
            if (s[i] != '"') return 0;
            i++;
            if (!s[i]) return 0;
            rows[m][col++] = s[i++];
            if (s[i] != '"') return 0;
            i++;
        }
        rows[m][col] = '\0';
        if (n < 0) n = col;
        m++;
        if (m >= MAX_N) break;
    }
    for (int r = 0; r < m; r++) ptr[r] = rows[r];
    *outM = m;
    *outN = n < 0 ? 0 : n;
    return 1;
}

int main(void) {
    size_t nread = fread(gbuf, 1, MAX_LEN - 1, stdin);
    gbuf[nread] = '\0';
    char* nl = strchr(gbuf, '\n');
    char* line2 = "[]";
    if (nl) {
        *nl = '\0';
        line2 = nl + 1;
        size_t wl = strlen(line2);
        while (wl > 0 && (line2[wl - 1] == '\n' || line2[wl - 1] == '\r')) line2[--wl] = '\0';
    }
    int tm = 0, tn = 0, sm = 0, sn = 0;
    if (!parseBoard(gbuf, trows, tptr, &tm, &tn)) return 1;
    if (!parseBoard(line2, srows, sptr, &sm, &sn)) return 1;
    int out[2];
    findStampPos(tptr, tm, tn, sptr, sm, sn, out);
    printf("[%d, %d]\n", out[0], out[1]);
    return 0;
}
