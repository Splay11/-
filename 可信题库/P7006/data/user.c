#include <stdbool.h>
#include <stdlib.h>

typedef struct clusterPool clusterPool;

struct clusterPool {
    int unused;
};

clusterPool* clusterPoolCreate(void) {
    return (clusterPool*)calloc(1, sizeof(clusterPool));
}

void clusterPoolFree(clusterPool* obj) {
    free(obj);
}

bool clusterPoolAddNode(clusterPool* obj, int nodeId, int capacity) {
    (void)obj;
    (void)nodeId;
    (void)capacity;
    return false;
}

bool clusterPoolRemoveNode(clusterPool* obj, int nodeId) {
    (void)obj;
    (void)nodeId;
    return false;
}

int clusterPoolSubmit(clusterPool* obj, int jobId, int size) {
    (void)obj;
    (void)jobId;
    (void)size;
    return -1;
}

bool clusterPoolKill(clusterPool* obj, int jobId) {
    (void)obj;
    (void)jobId;
    return false;
}

int clusterPoolUsedOf(clusterPool* obj, int nodeId) {
    (void)obj;
    (void)nodeId;
    return -1;
}

int clusterPoolFreeOf(clusterPool* obj, int nodeId) {
    (void)obj;
    (void)nodeId;
    return -1;
}

int clusterPoolJobNode(clusterPool* obj, int jobId) {
    (void)obj;
    (void)jobId;
    return -1;
}
