#include "foo.c"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[4096];
    PickupDesk* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a;
        if (strcmp(line, "PickupDesk()") == 0) {
            if (obj) pickupDeskFree(obj);
            obj = pickupDeskCreate();
            printf("null\n");
        } else if (sscanf(line, "order(%d)", &a) == 1) {
            printf("%s\n", pickupDeskOrder(obj, a) ? "true" : "false");
        } else if (strcmp(line, "serve()") == 0) {
            printf("%d\n", pickupDeskServe(obj));
        } else if (strcmp(line, "waiting()") == 0) {
            printf("%d\n", pickupDeskWaiting(obj));
        } else {
            return 1;
        }
    }
    if (obj) pickupDeskFree(obj);
    return 0;
}
