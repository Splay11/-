#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[256];
    ParkingLot* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int n, a, b, c;
        if (sscanf(line, "ParkingLot(%d)", &n) == 1) {
            if (obj) parkingLotFree(obj);
            obj = parkingLotCreate(n);
            printf("null\n");
        } else if (sscanf(line, "reserve(%d, %d, %d)", &a, &b, &c) == 3) {
            printf("%d\n", parkingLotReserve(obj, a, b, c));
        } else if (sscanf(line, "cancel(%d)", &a) == 1 && strstr(line, "cancel(") == line) {
            printf("%s\n", parkingLotCancel(obj, a) ? "true" : "false");
        } else if (sscanf(line, "spotOf(%d)", &a) == 1) {
            printf("%d\n", parkingLotSpotOf(obj, a));
        } else if (sscanf(line, "busyCount(%d)", &a) == 1) {
            printf("%d\n", parkingLotBusyCount(obj, a));
        } else {
            return 1;
        }
    }
    if (obj) parkingLotFree(obj);
    return 0;
}
