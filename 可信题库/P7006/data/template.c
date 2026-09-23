#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[512];
    clusterPool* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (strcmp(line, "ClusterPool()") == 0) {
            if (obj) clusterPoolFree(obj);
            obj = clusterPoolCreate();
            printf("null\n");
        } else if (sscanf(line, "addNode(%d, %d)", &a, &b) == 2
                   || sscanf(line, "addNode(%d,%d)", &a, &b) == 2) {
            printf("%s\n", clusterPoolAddNode(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "removeNode(%d)", &a) == 1
                   && strncmp(line, "removeNode(", 11) == 0) {
            printf("%s\n", clusterPoolRemoveNode(obj, a) ? "true" : "false");
        } else if (sscanf(line, "submit(%d, %d)", &a, &b) == 2
                   || sscanf(line, "submit(%d,%d)", &a, &b) == 2) {
            printf("%d\n", clusterPoolSubmit(obj, a, b));
        } else if (sscanf(line, "kill(%d)", &a) == 1 && strncmp(line, "kill(", 5) == 0) {
            printf("%s\n", clusterPoolKill(obj, a) ? "true" : "false");
        } else if (sscanf(line, "usedOf(%d)", &a) == 1) {
            printf("%d\n", clusterPoolUsedOf(obj, a));
        } else if (sscanf(line, "freeOf(%d)", &a) == 1) {
            printf("%d\n", clusterPoolFreeOf(obj, a));
        } else if (sscanf(line, "jobNode(%d)", &a) == 1) {
            printf("%d\n", clusterPoolJobNode(obj, a));
        } else {
            return 1;
        }
    }
    if (obj) clusterPoolFree(obj);
    return 0;
}
