#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    int unused;
} parcelSlots;

parcelSlots* parcelSlotsCreate(int n) {
    (void)n;
    return (parcelSlots*)calloc(1, sizeof(parcelSlots));
}

void parcelSlotsFree(parcelSlots* obj) {
    free(obj);
}

bool parcelSlotsPut(parcelSlots* obj, int i, int w) {
    (void)obj;
    (void)i;
    (void)w;
    return false;
}

int parcelSlotsTake(parcelSlots* obj, int i) {
    (void)obj;
    (void)i;
    return 0;
}

bool parcelSlotsMoveRight(parcelSlots* obj, int i) {
    (void)obj;
    (void)i;
    return false;
}

int parcelSlotsOccupied(parcelSlots* obj) {
    (void)obj;
    return 0;
}
