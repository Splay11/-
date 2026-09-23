#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 2000

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    char s[MAX_LEN];
    int n = 0;
    char *comma = strchr(line, ',');
    if (!comma) return 0;
    *comma = '\0';
    n = atoi(comma + 1);

    // remove leading and trailing quotes of s
    int start = 0, end = strlen(line) - 1;
    if (line[start] == '"') start++;
    if (end >= 0 && line[end] == '"') end--;
    int j = 0;
    for (int i = start; i <= end; i++) s[j++] = line[i];
    s[j] = '\0';

    char* result = processChunks(s, n);
    printf("\"%s\"\n", result);
    free(result);
    return 0;
}
