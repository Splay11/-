#include <stdbool.h>
#include <stdlib.h>

typedef struct ParkingLot ParkingLot;

struct ParkingLot {
    int unused;
};

ParkingLot* parkingLotCreate(int n) {
    (void)n;
    return (ParkingLot*)calloc(1, sizeof(ParkingLot));
}

void parkingLotFree(ParkingLot* obj) {
    free(obj);
}

int parkingLotReserve(ParkingLot* obj, int carId, int start, int end) {
    (void)obj;
    (void)carId;
    (void)start;
    (void)end;
    return -1;
}

bool parkingLotCancel(ParkingLot* obj, int carId) {
    (void)obj;
    (void)carId;
    return false;
}

int parkingLotSpotOf(ParkingLot* obj, int carId) {
    (void)obj;
    (void)carId;
    return -1;
}

int parkingLotBusyCount(ParkingLot* obj, int time) {
    (void)obj;
    (void)time;
    return 0;
}
