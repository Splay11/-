#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 10005
#define HCAP 20023

typedef struct {
    int cap;
    int lane[MAXN], laneSz;
    int wait[MAXN], waitSz;
    int histKind[MAXN];
    int histCar[MAXN];
    int histSz;
    int hkey[HCAP];
    char hloc[HCAP];
} ParkingLane;

static int hashProbe(ParkingLane* o, int key, int forInsert) {
    unsigned h = (unsigned)key % HCAP;
    int firstDel = -1;
    for (int t = 0; t < HCAP; t++) {
        int i = (int)((h + (unsigned)t) % HCAP);
        if (o->hloc[i] == 0) return forInsert ? (firstDel >= 0 ? firstDel : i) : -1;
        if (o->hloc[i] == 3) {
            if (firstDel < 0) firstDel = i;
            continue;
        }
        if (o->hkey[i] == key) return i;
    }
    return forInsert ? firstDel : -1;
}

static int getLoc(ParkingLane* o, int key) {
    int i = hashProbe(o, key, 0);
    return i < 0 ? 0 : (int)o->hloc[i];
}

static void setLoc(ParkingLane* o, int key, int loc) {
    if (loc == 0) {
        int i = hashProbe(o, key, 0);
        if (i >= 0) o->hloc[i] = 3;
        return;
    }
    int i = hashProbe(o, key, 1);
    o->hkey[i] = key;
    o->hloc[i] = (char)loc;
}

ParkingLane* parkingLaneCreate(int capacity) {
    ParkingLane* o = (ParkingLane*)calloc(1, sizeof(ParkingLane));
    o->cap = capacity;
    return o;
}

void parkingLaneFree(ParkingLane* obj) { free(obj); }

bool parkingLaneArrive(ParkingLane* obj, int carId) {
    if (getLoc(obj, carId) != 0) return false;
    if (obj->laneSz < obj->cap) {
        obj->lane[obj->laneSz++] = carId;
        setLoc(obj, carId, 1);
        obj->histKind[obj->histSz] = 0;
        obj->histCar[obj->histSz++] = carId;
    } else {
        obj->wait[obj->waitSz++] = carId;
        setLoc(obj, carId, 2);
        obj->histKind[obj->histSz] = 1;
        obj->histCar[obj->histSz++] = carId;
    }
    return true;
}

bool parkingLaneAdmit(ParkingLane* obj) {
    if (obj->waitSz == 0 || obj->laneSz >= obj->cap) return false;
    int carId = obj->wait[0];
    memmove(obj->wait, obj->wait + 1, (size_t)(obj->waitSz - 1) * sizeof(int));
    obj->waitSz--;
    setLoc(obj, carId, 0);
    obj->lane[obj->laneSz++] = carId;
    setLoc(obj, carId, 1);
    obj->histKind[obj->histSz] = 2;
    obj->histCar[obj->histSz++] = carId;
    return true;
}

int parkingLaneDepart(ParkingLane* obj, int carId) {
    if (getLoc(obj, carId) != 1) return -1;
    int temp[MAXN], tempSz = 0, moved = 0;
    while (obj->laneSz > 0 && obj->lane[obj->laneSz - 1] != carId) {
        temp[tempSz++] = obj->lane[--obj->laneSz];
        moved++;
    }
    obj->laneSz--;
    setLoc(obj, carId, 0);
    while (tempSz > 0) obj->lane[obj->laneSz++] = temp[--tempSz];
    obj->histKind[obj->histSz] = 3;
    obj->histCar[obj->histSz++] = carId;
    return moved;
}

bool parkingLaneUndo(ParkingLane* obj) {
    if (obj->histSz == 0) return false;
    int kind = obj->histKind[--obj->histSz];
    int carId = obj->histCar[obj->histSz];
    if (kind == 0) {
        if (obj->laneSz == 0 || obj->lane[obj->laneSz - 1] != carId) {
            obj->histSz++;
            return false;
        }
        obj->laneSz--;
        setLoc(obj, carId, 0);
        return true;
    }
    if (kind == 1) {
        int idx = -1;
        for (int i = 0; i < obj->waitSz; i++) if (obj->wait[i] == carId) { idx = i; break; }
        if (idx < 0) { obj->histSz++; return false; }
        memmove(obj->wait + idx, obj->wait + idx + 1, (size_t)(obj->waitSz - idx - 1) * sizeof(int));
        obj->waitSz--;
        setLoc(obj, carId, 0);
        return true;
    }
    if (kind == 2) {
        if (obj->laneSz == 0 || obj->lane[obj->laneSz - 1] != carId) {
            obj->histSz++;
            return false;
        }
        obj->laneSz--;
        setLoc(obj, carId, 0);
        memmove(obj->wait + 1, obj->wait, (size_t)obj->waitSz * sizeof(int));
        obj->wait[0] = carId;
        obj->waitSz++;
        setLoc(obj, carId, 2);
        return true;
    }
    if (getLoc(obj, carId) != 0 || obj->laneSz >= obj->cap) {
        obj->histSz++;
        return false;
    }
    obj->lane[obj->laneSz++] = carId;
    setLoc(obj, carId, 1);
    return true;
}

int parkingLaneFront(ParkingLane* obj) {
    return obj->laneSz ? obj->lane[obj->laneSz - 1] : -1;
}
int parkingLaneWaiting(ParkingLane* obj) { return obj->waitSz; }
int parkingLaneSize(ParkingLane* obj) { return obj->laneSz; }
