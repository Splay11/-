#include "foo.c"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

static int** parseArray2d(const char* s, int* outRows, int** outColSizes) {
    const char* p = s;
    skipSpace(&p);
    if (*p != '[') exit(1);
    p++;
    int cap = 8;
    int** rows = (int**)malloc((size_t)cap * sizeof(int*));
    int* colSizes = (int*)malloc((size_t)cap * sizeof(int));
    int n = 0;
    while (1) {
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != '[') exit(1);
        p++;
        int innerCap = 4;
        int* row = (int*)malloc((size_t)innerCap * sizeof(int));
        int m = 0;
        while (1) {
            skipSpace(&p);
            if (*p == ']') {
                p++;
                break;
            }
            if (m >= innerCap) {
                innerCap *= 2;
                row = (int*)realloc(row, (size_t)innerCap * sizeof(int));
            }
            row[m++] = readInt(&p);
            skipSpace(&p);
            if (*p == ']') {
                p++;
                break;
            }
            if (*p != ',') exit(1);
            p++;
        }
        if (n >= cap) {
            cap *= 2;
            rows = (int**)realloc(rows, (size_t)cap * sizeof(int*));
            colSizes = (int*)realloc(colSizes, (size_t)cap * sizeof(int));
        }
        rows[n] = row;
        colSizes[n] = m;
        n++;
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != ',') exit(1);
        p++;
    }
    *outRows = n;
    *outColSizes = colSizes;
    return rows;
}

static char* parseQuoted(const char* s) {
    const char* p = s;
    skipSpace(&p);
    size_t len = strlen(p);
    while (len > 0 && (p[len - 1] == '\n' || p[len - 1] == '\r' || isspace((unsigned char)p[len - 1])))
        len--;
    if (len >= 2 && p[0] == '"' && p[len - 1] == '"') {
        char* out = (char*)malloc(len - 1);
        memcpy(out, p + 1, len - 2);
        out[len - 2] = '\0';
        return out;
    }
    char* out = (char*)malloc(len + 1);
    memcpy(out, p, len);
    out[len] = '\0';
    return out;
}

int main(void) {
    char* line1 = (char*)malloc(1 << 20);
    char* line2 = (char*)malloc(1 << 10);
    if (!fgets(line1, 1 << 20, stdin)) {
        free(line1);
        free(line2);
        return 0;
    }
    if (!fgets(line2, 1 << 10, stdin)) {
        free(line1);
        free(line2);
        return 0;
    }

    int cardsSize = 0;
    int* cardsColSize = NULL;
    int** cards = parseArray2d(line1, &cardsSize, &cardsColSize);
    char* alignment = parseQuoted(line2);

    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** ans = alignCards(cards, cardsSize, cardsColSize, alignment, &returnSize, &returnColumnSizes);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(", ");
        printf("[");
        for (int j = 0; j < returnColumnSizes[i]; j++) {
            if (j) printf(", ");
            printf("%d", ans[i][j]);
        }
        printf("]");
    }
    printf("]\n");

    for (int i = 0; i < cardsSize; i++) free(cards[i]);
    free(cards);
    free(cardsColSize);
    free(alignment);
    if (ans) {
        for (int i = 0; i < returnSize; i++) free(ans[i]);
        free(ans);
    }
    free(returnColumnSizes);
    free(line1);
    free(line2);
    return 0;
}
