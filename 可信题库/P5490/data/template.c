#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[512];
    parcelSlots* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (sscanf(line, "ParcelSlots(%d)", &a) == 1 && strncmp(line, "ParcelSlots(", 12) == 0) {
            if (obj) parcelSlotsFree(obj);
            obj = parcelSlotsCreate(a);
            printf("null\n");
        } else if (sscanf(line, "put(%d, %d)", &a, &b) == 2
                   || sscanf(line, "put(%d,%d)", &a, &b) == 2) {
            printf("%s\n", parcelSlotsPut(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "take(%d)", &a) == 1 && strncmp(line, "take(", 5) == 0) {
            printf("%d\n", parcelSlotsTake(obj, a));
        } else if (sscanf(line, "moveRight(%d)", &a) == 1 && strncmp(line, "moveRight(", 10) == 0) {
            printf("%s\n", parcelSlotsMoveRight(obj, a) ? "true" : "false");
        } else if (strcmp(line, "occupied()") == 0) {
            printf("%d\n", parcelSlotsOccupied(obj));
        } else {
            return 1;
        }
    }
    if (obj) parcelSlotsFree(obj);
    return 0;
}
