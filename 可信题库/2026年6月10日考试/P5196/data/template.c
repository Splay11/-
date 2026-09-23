#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 4096

static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}

char* parsePacketHeader(char* header);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    trim_nl(line);
    char* ans = parsePacketHeader(line);
    printf("%s\n", ans ? ans : "");
    free(ans);
    return 0;
}
