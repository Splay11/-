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

static int* parseArray1d(const char* s, int* outSize) {
    const char* p = s;
    skipSpace(&p);
    if (*p != '[') exit(1);
    p++;
    int cap = 8;
    int* vals = (int*)malloc((size_t)cap * sizeof(int));
    int n = 0;
    while (1) {
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (n >= cap) {
            cap *= 2;
            vals = (int*)realloc(vals, (size_t)cap * sizeof(int));
        }
        vals[n++] = readInt(&p);
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != ',') exit(1);
        p++;
    }
    *outSize = n;
    return vals;
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

int main(void) {
    char* line1 = (char*)malloc(1 << 20);
    char* line2 = (char*)malloc(1 << 20);
    if (!fgets(line1, 1 << 20, stdin)) {
        free(line1);
        free(line2);
        return 0;
    }
    if (!fgets(line2, 1 << 20, stdin)) {
        free(line1);
        free(line2);
        return 0;
    }

    int rectsSize = 0;
    int* rectsColSize = NULL;
    int** rects = parseArray2d(line1, &rectsSize, &rectsColSize);
    int queryRectSize = 0;
    int* queryRect = parseArray1d(line2, &queryRectSize);

    int returnSize = 0;
    int* ans = queryVisibleRects(rects, rectsSize, rectsColSize, queryRect, queryRectSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(", ");
        printf("%d", ans[i]);
    }
    printf("]\n");

    for (int i = 0; i < rectsSize; i++) free(rects[i]);
    free(rects);
    free(rectsColSize);
    free(queryRect);
    free(ans);
    free(line1);
    free(line2);
    return 0;
}
