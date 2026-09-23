#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "foo.c"

#define BUFMAX 20000000
#define NMAX 100005
#define MMAX 100005

static char gbuf[BUFMAX];

static char* readAll(void) {
    size_t n = fread(gbuf, 1, BUFMAX - 1, stdin);
    gbuf[n] = '\0';
    while (n > 0 && (gbuf[n - 1] == '\n' || gbuf[n - 1] == '\r')) gbuf[--n] = '\0';
    return gbuf;
}

static int parseIntList(const char* s, int* out, int cap) {
    int n = 0;
    const char* p = s;
    while (*p && *p != '[') p++;
    if (*p == '[') p++;
    while (*p && *p != ']') {
        while (*p == ' ' || *p == ',') p++;
        if (!*p || *p == ']') break;
        int sign = 1;
        if (*p == '-') { sign = -1; p++; }
        long long v = 0;
        while (*p >= '0' && *p <= '9') { v = v * 10 + (*p - '0'); p++; }
        if (n < cap) out[n++] = (int)(sign * v);
    }
    return n;
}

static int parseTriples(const char* s, int* A, int* B, int* C, int cap) {
    int n = 0;
    const char* p = s;
    while (*p && *p != '[') p++;
    if (*p == '[') p++;
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (!*p || *p == ']') break;
        if (*p != '[') { p++; continue; }
        p++;
        int vals[3] = {0, 0, 0}, k = 0;
        while (*p && *p != ']' && k < 3) {
            while (*p == ' ' || *p == ',') p++;
            if (!*p || *p == ']') break;
            int sign = 1;
            if (*p == '-') { sign = -1; p++; }
            long long v = 0;
            while (*p >= '0' && *p <= '9') { v = v * 10 + (*p - '0'); p++; }
            vals[k++] = (int)(sign * v);
        }
        while (*p && *p != ']') p++;
        if (*p == ']') p++;
        if (n < cap) {
            A[n] = vals[0];
            B[n] = vals[1];
            C[n] = vals[2];
            n++;
        }
    }
    return n;
}

static int L[MMAX], R[MMAX], W[MMAX];

int main(void) {
    char* raw = readAll();
    char* nl = strchr(raw, '\n');
    int n = 0;
    if (nl) { *nl = '\0'; n = atoi(raw); raw = nl + 1; }
    else n = atoi(raw);
    int m = parseTriples(raw, L, R, W, MMAX);
    printf("%lld\n", maxLinkLoad(n, L, R, W, m));
    return 0;
}
