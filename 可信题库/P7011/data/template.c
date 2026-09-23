#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[512];
    certAuthority* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b, c;
        if (strcmp(line, "CertAuthority()") == 0) {
            if (obj) certAuthorityFree(obj);
            obj = certAuthorityCreate();
            printf("null\n");
        } else if (sscanf(line, "issue(%d, %d, %d)", &a, &b, &c) == 3
                   || sscanf(line, "issue(%d,%d,%d)", &a, &b, &c) == 3) {
            printf("%s\n", certAuthorityIssue(obj, a, b, c) ? "true" : "false");
        } else if (sscanf(line, "revoke(%d)", &a) == 1 && strncmp(line, "revoke(", 7) == 0) {
            printf("%s\n", certAuthorityRevoke(obj, a) ? "true" : "false");
        } else if (sscanf(line, "isValid(%d, %d)", &a, &b) == 2
                   || sscanf(line, "isValid(%d,%d)", &a, &b) == 2) {
            printf("%s\n", certAuthorityIsValid(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "ttl(%d, %d)", &a, &b) == 2
                   || sscanf(line, "ttl(%d,%d)", &a, &b) == 2) {
            printf("%d\n", certAuthorityTtl(obj, a, b));
        } else if (sscanf(line, "issuerOf(%d)", &a) == 1 && strncmp(line, "issuerOf(", 9) == 0) {
            printf("%d\n", certAuthorityIssuerOf(obj, a));
        } else if (sscanf(line, "rootOf(%d)", &a) == 1 && strncmp(line, "rootOf(", 7) == 0) {
            printf("%d\n", certAuthorityRootOf(obj, a));
        } else {
            return 1;
        }
    }
    if (obj) certAuthorityFree(obj);
    return 0;
}
