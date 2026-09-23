#include <stdbool.h>
#include <stdlib.h>

typedef struct PickupDesk PickupDesk;

struct PickupDesk {
    int unused;
};

PickupDesk* pickupDeskCreate(void) {
    return (PickupDesk*)calloc(1, sizeof(PickupDesk));
}

void pickupDeskFree(PickupDesk* obj) {
    free(obj);
}

bool pickupDeskOrder(PickupDesk* obj, int ticketId) {
    (void)obj;
    (void)ticketId;
    return false;
}

int pickupDeskServe(PickupDesk* obj) {
    (void)obj;
    return -1;
}

int pickupDeskWaiting(PickupDesk* obj) {
    (void)obj;
    return 0;
}
