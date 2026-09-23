#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[256];
    ParkingLane* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;
        int a;
        if (sscanf(line, "ParkingLane(%d)", &a) == 1) {
            if (obj) parkingLaneFree(obj);
            obj = parkingLaneCreate(a);
            printf("null\n");
        } else if (sscanf(line, "arrive(%d)", &a) == 1) {
            printf(parkingLaneArrive(obj, a) ? "true\n" : "false\n");
        } else if (strcmp(line, "admit()") == 0) {
            printf(parkingLaneAdmit(obj) ? "true\n" : "false\n");
        } else if (sscanf(line, "depart(%d)", &a) == 1) {
            printf("%d\n", parkingLaneDepart(obj, a));
        } else if (strcmp(line, "undo()") == 0) {
            printf(parkingLaneUndo(obj) ? "true\n" : "false\n");
        } else if (strcmp(line, "front()") == 0) {
            printf("%d\n", parkingLaneFront(obj));
        } else if (strcmp(line, "waiting()") == 0) {
            printf("%d\n", parkingLaneWaiting(obj));
        } else if (strcmp(line, "size()") == 0) {
            printf("%d\n", parkingLaneSize(obj));
        } else return 1;
    }
    if (obj) parkingLaneFree(obj);
    return 0;
}
