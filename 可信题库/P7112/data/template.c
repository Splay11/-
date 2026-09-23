#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[512];
    shardLeaseManager* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b, c, d;
        if (sscanf(line, "ShardLeaseManager(%d, %d)", &a, &b) == 2
            || sscanf(line, "ShardLeaseManager(%d,%d)", &a, &b) == 2) {
            if (obj) shardLeaseManagerFree(obj);
            obj = shardLeaseManagerCreate(a, b);
            printf("null\n");
        } else if (sscanf(line, "acquire(%d, %d, %d, %d)", &a, &b, &c, &d) == 4
                   || sscanf(line, "acquire(%d,%d,%d,%d)", &a, &b, &c, &d) == 4) {
            printf("%s\n", shardLeaseManagerAcquire(obj, a, b, c, d) ? "true" : "false");
        } else if (sscanf(line, "renew(%d, %d, %d, %d)", &a, &b, &c, &d) == 4
                   || sscanf(line, "renew(%d,%d,%d,%d)", &a, &b, &c, &d) == 4) {
            printf("%s\n", shardLeaseManagerRenew(obj, a, b, c, d) ? "true" : "false");
        } else if (sscanf(line, "release(%d, %d, %d)", &a, &b, &c) == 3
                   || sscanf(line, "release(%d,%d,%d)", &a, &b, &c) == 3) {
            printf("%s\n", shardLeaseManagerRelease(obj, a, b, c) ? "true" : "false");
        } else if (sscanf(line, "owner(%d, %d)", &a, &b) == 2
                   || sscanf(line, "owner(%d,%d)", &a, &b) == 2) {
            printf("%d\n", shardLeaseManagerOwner(obj, a, b));
        } else if (sscanf(line, "heldCount(%d, %d)", &a, &b) == 2
                   || sscanf(line, "heldCount(%d,%d)", &a, &b) == 2) {
            printf("%d\n", shardLeaseManagerHeldCount(obj, a, b));
        } else {
            return 1;
        }
    }
    if (obj) shardLeaseManagerFree(obj);
    return 0;
}
