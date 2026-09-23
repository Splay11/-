#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

char* sort(char* sortResolutions);

int main() {
    char input[MAX_LEN];
    if (!fgets(input, MAX_LEN, stdin)) return 0;
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) {
        input[--len] = '\0';
    }

    char* res = sort(input);
    if (res) {
        printf("\"%s\"\n", res);
        free(res);
    }
    return 0;
}
