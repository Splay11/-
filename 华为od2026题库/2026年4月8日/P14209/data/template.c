#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int getErrorCount(char* rules);

int main() {
    char buffer[100000];
    if (!fgets(buffer, sizeof(buffer), stdin))
        return 0;
    int len = strlen(buffer);
    while (len > 0 && (buffer[len - 1] == '\n' || buffer[len - 1] == '\r'))
        buffer[--len] = '\0';
    int result = getErrorCount(buffer);
    printf("%d\n", result);
    return 0;
}
