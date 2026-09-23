#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int minDistinctAfterSwap(char* resA, char* resB);

int main() {
    char line[400010];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';
    char *p1 = strchr(line, '"');
    if (!p1) return 0;
    char *p2 = strchr(p1 + 1, '"');
    if (!p2) return 0;
    int lenA = p2 - p1 - 1;
    char *resA = (char*)malloc(lenA + 1);
    strncpy(resA, p1 + 1, lenA);
    resA[lenA] = '\0';
    char *p3 = strchr(p2 + 1, '"');
    while (p3 && *(p3 - 1) == '\\') p3 = strchr(p3 + 1, '"');
    if (!p3) return 0;
    char *p4 = strchr(p3 + 1, '"');
    if (!p4) return 0;
    int lenB = p4 - p3 - 1;
    char *resB = (char*)malloc(lenB + 1);
    strncpy(resB, p3 + 1, lenB);
    resB[lenB] = '\0';
    int ans = minDistinctAfterSwap(resA, resB);
    printf("%d\n", ans);
    free(resA);
    free(resB);
    return 0;
}
