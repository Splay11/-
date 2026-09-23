#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 2000000

static char gbuf[MAX_LEN];

int firstTasteLevel(char* note, int noteLen);

int main(void) {
    size_t nread = fread(gbuf, 1, MAX_LEN - 1, stdin);
    gbuf[nread] = '\0';
    while (nread > 0 && (gbuf[nread - 1] == '\n' || gbuf[nread - 1] == '\r')) gbuf[--nread] = '\0';
    char* s = gbuf;
    while (*s == ' ' || *s == '\t') s++;
    if (*s == '"') s++;
    size_t len = strlen(s);
    if (len > 0 && s[len - 1] == '"') s[--len] = '\0';
    printf("%d\n", firstTasteLevel(s, (int)strlen(s)));
    return 0;
}
