#include "foo.c"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char* readAll(void) {
    size_t cap = 4096, len = 0;
    char* buf = (char*)malloc(cap);
    int c;
    while ((c = getchar()) != EOF) {
        if (len + 1 >= cap) {
            cap *= 2;
            buf = (char*)realloc(buf, cap);
        }
        buf[len++] = (char)c;
    }
    buf[len] = '\0';
    while (len > 0 && isspace((unsigned char)buf[len - 1])) buf[--len] = '\0';
    return buf;
}

static void skipSpace(const char** p) {
    while (**p && isspace((unsigned char)**p)) (*p)++;
}

static int readInt(const char** p) {
    skipSpace(p);
    int sign = 1;
    if (**p == '-') {
        sign = -1;
        (*p)++;
    }
    if (!isdigit((unsigned char)**p)) exit(1);
    int v = 0;
    while (isdigit((unsigned char)**p)) {
        v = v * 10 + (**p - '0');
        (*p)++;
    }
    return sign * v;
}

static char* readQuoted(const char** p) {
    skipSpace(p);
    if (**p != '"') exit(1);
    (*p)++;
    size_t cap = 32, len = 0;
    char* out = (char*)malloc(cap);
    while (**p && **p != '"') {
        char ch;
        if (**p == '\\' && *(*p + 1)) {
            ch = *(*p + 1);
            (*p) += 2;
        } else {
            ch = **p;
            (*p)++;
        }
        if (len + 1 >= cap) {
            cap *= 2;
            out = (char*)realloc(out, cap);
        }
        out[len++] = ch;
    }
    if (**p != '"') exit(1);
    (*p)++;
    out[len] = '\0';
    return out;
}

static Cell* parseTable(const char* s, int* outSize) {
    const char* p = s;
    skipSpace(&p);
    if (*p != '[') exit(1);
    p++;
    int cap = 8;
    Cell* table = (Cell*)malloc((size_t)cap * sizeof(Cell));
    int n = 0;
    while (1) {
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != '[') exit(1);
        p++;
        int r = readInt(&p);
        skipSpace(&p);
        if (*p != ',') exit(1);
        p++;
        int c = readInt(&p);
        skipSpace(&p);
        if (*p != ',') exit(1);
        p++;
        char* content = readQuoted(&p);
        skipSpace(&p);
        if (*p != ']') exit(1);
        p++;
        if (n >= cap) {
            cap *= 2;
            table = (Cell*)realloc(table, (size_t)cap * sizeof(Cell));
        }
        table[n].rowNum = r;
        table[n].colNum = c;
        table[n].content = content;
        n++;
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != ',') exit(1);
        p++;
    }
    *outSize = n;
    return table;
}

int main(void) {
    char* all = readAll();
    if (!all || !all[0]) {
        free(all);
        return 0;
    }
    int tableSize = 0;
    Cell* table = parseTable(all, &tableSize);
    int returnSize = 0;
    char** ans = transformTable(table, tableSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(",");
        printf("\"");
        for (char* q = ans[i]; *q; q++) {
            if (*q == '\\' || *q == '"') putchar('\\');
            putchar(*q);
        }
        printf("\"");
    }
    printf("]\n");

    for (int i = 0; i < tableSize; i++) free(table[i].content);
    free(table);
    if (ans) {
        for (int i = 0; i < returnSize; i++) free(ans[i]);
        free(ans);
    }
    free(all);
    return 0;
}
