#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 20000

int main() {
    char input[MAX_LEN];
    if (!fgets(input, MAX_LEN, stdin)) return 0;
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r'))
        input[--len] = '\0';

    // Trim spaces
    while (len > 0 && input[0] == ' ') {
        memmove(input, input + 1, len);
        len--;
    }

    if (len == 0) {
        printf("\n");
        return 0;
    }

    // parse format: "8F-3T-1G-2n",4
    char snStr[MAX_LEN];
    int m = 0;
    char *comma = strrchr(input, ',');
    if (comma == NULL) {
        printf("\n");
        return 0;
    }
    *comma = '\0';
    m = atoi(comma + 1);
    // remove leading and trailing quotes for sn
    char *s = input;
    while (*s == ' ') s++;
    int sLen = strlen(s);
    while (sLen > 0 && (s[sLen - 1] == ' ')) s[--sLen] = '\0';
    if (sLen >= 2 && s[0] == '"' && s[sLen - 1] == '"') {
        strncpy(snStr, s + 1, sLen - 2);
        snStr[sLen - 2] = '\0';
    } else {
        strncpy(snStr, s, MAX_LEN - 1);
        snStr[MAX_LEN - 1] = '\0';
    }

    char* result = rearrangeSN(snStr, m);
    if (result == NULL) {
        printf("\n");
        return 0;
    }
    printf("%s\n", result);
    free(result);
    return 0;
}
