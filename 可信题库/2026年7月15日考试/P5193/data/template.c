#include "foo.c"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void skipSpace(const char** p) {
    while (**p && isspace((unsigned char)**p)) (*p)++;
}

static char** parseStringArray(const char* s, int* outSize) {
    const char* p = s;
    skipSpace(&p);
    if (*p != '[') exit(1);
    p++;
    int cap = 16;
    char** out = (char**)malloc((size_t)cap * sizeof(char*));
    int n = 0;
    while (1) {
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != '"') exit(1);
        p++;
        const char* start = p;
        while (*p && *p != '"') p++;
        if (*p != '"') exit(1);
        size_t len = (size_t)(p - start);
        char* cur = (char*)malloc(len + 1);
        memcpy(cur, start, len);
        cur[len] = '\0';
        p++;
        if (n >= cap) {
            cap *= 2;
            out = (char**)realloc(out, (size_t)cap * sizeof(char*));
        }
        out[n++] = cur;
        skipSpace(&p);
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != ',') exit(1);
        p++;
    }
    *outSize = n;
    return out;
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

    int charMatrixSize = 0;
    char** charMatrix = parseStringArray(line1, &charMatrixSize);
    int wordsSize = 0;
    char** words = parseStringArray(line2, &wordsSize);

    int ans = countMatchedWords(charMatrix, charMatrixSize, words, wordsSize);
    printf("%d\n", ans);

    for (int i = 0; i < charMatrixSize; i++) free(charMatrix[i]);
    free(charMatrix);
    for (int i = 0; i < wordsSize; i++) free(words[i]);
    free(words);
    free(line1);
    free(line2);
    return 0;
}
