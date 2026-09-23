#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[256];
    TTLCache* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b, c;
        if (sscanf(line, "TTLCache(%d)", &a) == 1) {
            if (obj) tTLCacheFree(obj);
            obj = tTLCacheCreate(a);
            printf("null\n");
        } else if (sscanf(line, "put(%d, %d, %d)", &a, &b, &c) == 3) {
            tTLCachePut(obj, a, b, c);
            printf("null\n");
        } else if (sscanf(line, "get(%d, %d)", &a, &b) == 2) {
            printf("%d\n", tTLCacheGet(obj, a, b));
        } else if (sscanf(line, "purge(%d)", &a) == 1) {
            printf("%d\n", tTLCachePurge(obj, a));
        } else if (strcmp(line, "size()") == 0) {
            printf("%d\n", tTLCacheSize(obj));
        } else {
            return 1;
        }
    }
    if (obj) tTLCacheFree(obj);
    return 0;
}
