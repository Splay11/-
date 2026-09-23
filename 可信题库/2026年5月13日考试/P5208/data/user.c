#include <stdlib.h>

typedef struct GCSystem GCSystem;

struct GCSystem {
    int unused;
};

GCSystem* gCSystemCreate(int youngSize) {
    (void)youngSize;
    return (GCSystem*)calloc(1, sizeof(GCSystem));
}

void gCSystemFree(GCSystem* obj) {
    free(obj);
}

void gCSystemCreateObject(GCSystem* obj, int objectId) {
    (void)obj;
    (void)objectId;
}

void gCSystemMarkObjects(GCSystem* obj, int* objectIds, int objectIdsSize) {
    (void)obj;
    (void)objectIds;
    (void)objectIdsSize;
}

void gCSystemManualGC(GCSystem* obj, int generation) {
    (void)obj;
    (void)generation;
}

int* gCSystemGetLiveObjects(GCSystem* obj, int generation, int* returnSize) {
    (void)obj;
    (void)generation;
    *returnSize = 0;
    return NULL;
}
