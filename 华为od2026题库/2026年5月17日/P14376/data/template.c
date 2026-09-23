#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char ip[256];
    if (fgets(ip, sizeof(ip), stdin) == NULL) {
        return 0;
    }
    int len = strlen(ip);
    while (len > 0 && (ip[len - 1] == '\n' || ip[len - 1] == '\r')) {
        ip[--len] = '\0';
    }
    char* res = classifyIPv4(ip);
    printf("%s\n", res);
    return 0;
}
