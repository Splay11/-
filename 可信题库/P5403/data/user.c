#include <stdbool.h>
#include <stdlib.h>

typedef struct MicQueue MicQueue;

struct MicQueue {
    int unused;
};

MicQueue* micQueueCreate(void) {
    return (MicQueue*)calloc(1, sizeof(MicQueue));
}

void micQueueFree(MicQueue* obj) {
    free(obj);
}

bool micQueueEnroll(MicQueue* obj, int songId, int heat) {
    (void)obj;
    (void)songId;
    (void)heat;
    return false;
}

int micQueueNextPlay(MicQueue* obj) {
    (void)obj;
    return -1;
}

bool micQueueBoost(MicQueue* obj, int songId, int addHeat) {
    (void)obj;
    (void)songId;
    (void)addHeat;
    return false;
}

bool micQueueCancel(MicQueue* obj, int songId) {
    (void)obj;
    (void)songId;
    return false;
}

int micQueueWaiting(MicQueue* obj) {
    (void)obj;
    return 0;
}
