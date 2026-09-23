#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000

int** countKeys(char* s, int* returnSize);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    char *p = line;
    while (*p && (*p == ' ')) p++;
    if (*p == '"') {
        p++;
        char *q = strchr(p, '"');
        if (q) *q = '\0';
    }
    int returnSize = 0;
    int** res = countKeys(p, &returnSize);
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("[%d,%d]", res[i][0], res[i][1]);
        if (i != returnSize - 1) printf(",");
    }
    printf("]\n");
    for (int i = 0; i < returnSize; i++) free(res[i]);
    free(res);
    return 0;
}
