#include <stdbool.h>
#include <stdlib.h>

typedef struct shardLeaseManager shardLeaseManager;

struct shardLeaseManager {
    int unused;
};

shardLeaseManager* shardLeaseManagerCreate(int shardCount, int maxHold) {
    (void)shardCount;
    (void)maxHold;
    return (shardLeaseManager*)calloc(1, sizeof(shardLeaseManager));
}

void shardLeaseManagerFree(shardLeaseManager* obj) {
    free(obj);
}

bool shardLeaseManagerAcquire(shardLeaseManager* obj, int clientId, int shardId, int now, int ttl) {
    (void)obj; (void)clientId; (void)shardId; (void)now; (void)ttl;
    return false;
}

bool shardLeaseManagerRenew(shardLeaseManager* obj, int clientId, int shardId, int now, int ttl) {
    (void)obj; (void)clientId; (void)shardId; (void)now; (void)ttl;
    return false;
}

bool shardLeaseManagerRelease(shardLeaseManager* obj, int clientId, int shardId, int now) {
    (void)obj; (void)clientId; (void)shardId; (void)now;
    return false;
}

int shardLeaseManagerOwner(shardLeaseManager* obj, int shardId, int now) {
    (void)obj; (void)shardId; (void)now;
    return -1;
}

int shardLeaseManagerHeldCount(shardLeaseManager* obj, int clientId, int now) {
    (void)obj; (void)clientId; (void)now;
    return -1;
}
