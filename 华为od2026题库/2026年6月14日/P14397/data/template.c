#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 1005

char* processString(char* s);

int main() {
    char s[MAX_LEN];
    if (!fgets(s, MAX_LEN, stdin)) return 0;
    int len = strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r'))
        s[--len] = '\0';
    if (len >= 2 && s[0] == '"' && s[len - 1] == '"') {
        s[len - 1] = '\0';
        memmove(s, s + 1, len - 1);
    }
    char* res = processString(s);
    printf("\"%s\"\n", res);
    free(res);
    return 0;
}
