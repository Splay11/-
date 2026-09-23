#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 10000
#define MAX_GUARDS 1000

// 解析 [(x1,y1),(x2,y2)] 形式为二维数组
static int** parseGuards(const char* s, int* guardsSize, int** guardsColSize) {
    int** res = (int**)malloc(MAX_GUARDS * sizeof(int*));
    *guardsSize = 0;
    const char* p = s;
    while (*p) {
        if (*p == '(') {
            p++;
            int x, y;
            sscanf(p, "%d,%d", &x, &y);
            res[*guardsSize] = (int*)malloc(2 * sizeof(int));
            res[*guardsSize][0] = x;
            res[*guardsSize][1] = y;
            (*guardsSize)++;
        }
        p++;
    }
    *guardsColSize = (int*)malloc((*guardsSize) * sizeof(int));
    for (int i = 0; i < *guardsSize; i++) (*guardsColSize)[i] = 2;
    return res;
}

int* countShortestPaths(int n, int** guards, int guardsSize, int* guardsColSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';
    char* comma = strchr(line, ',');
    if (!comma) return 0;
    *comma = '\0';
    int n = atoi(line);
    char* guardsStr = comma + 1;
    while (*guardsStr == ' ') guardsStr++;
    int guardsSize;
    int* guardsColSize;
    int** guards = parseGuards(guardsStr, &guardsSize, &guardsColSize);

    int returnSize = 0;
    int* res = countShortestPaths(n, guards, guardsSize, guardsColSize, &returnSize);

    printf("[%d,%d]\n", res[0], res[1]);

    for (int i = 0; i < guardsSize; i++) free(guards[i]);
    free(guards);
    free(guardsColSize);
    free(res);
    return 0;
}
