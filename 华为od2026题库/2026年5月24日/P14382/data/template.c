#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 10005

char* processExpression(char* inputStr);

int main() {
    char buf[MAX_LEN];
    if (!fgets(buf, MAX_LEN, stdin)) return 0;
    int len = strlen(buf);
    while (len > 0 && (buf[len - 1] == '\n' || buf[len - 1] == '\r'))
        buf[--len] = '\0';
    if (len >= 2 && buf[0] == '"' && buf[len - 1] == '"') {
        buf[len - 1] = '\0';
        memmove(buf, buf + 1, len - 1);
    }
    char* result = processExpression(buf);
    if (result)
        printf("%s\n", result);
    else
        printf("NA\n");
    return 0;
}
