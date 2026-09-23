#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 10005

int lengthOfLongestSubstring(char* story);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    if (len >= 2 && line[0] == '"' && line[len - 1] == '"') {
        line[len - 1] = '\0';
        memmove(line, line + 1, len - 1);
    }

    int result = lengthOfLongestSubstring(line);
    printf("%d\n", result);
    return 0;
}
