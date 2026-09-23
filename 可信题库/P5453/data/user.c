#include <stdbool.h>
#include <stdlib.h>

typedef struct ParkingLane ParkingLane;
struct ParkingLane { int unused; };

ParkingLane* parkingLaneCreate(int capacity) {
    (void)capacity;
    return (ParkingLane*)calloc(1, sizeof(ParkingLane));
}
void parkingLaneFree(ParkingLane* obj) { free(obj); }
bool parkingLaneArrive(ParkingLane* obj, int carId) { (void)obj;(void)carId; return false; }
bool parkingLaneAdmit(ParkingLane* obj) { (void)obj; return false; }
int parkingLaneDepart(ParkingLane* obj, int carId) { (void)obj;(void)carId; return -1; }
bool parkingLaneUndo(ParkingLane* obj) { (void)obj; return false; }
int parkingLaneFront(ParkingLane* obj) { (void)obj; return -1; }
int parkingLaneWaiting(ParkingLane* obj) { (void)obj; return 0; }
int parkingLaneSize(ParkingLane* obj) { (void)obj; return 0; }
