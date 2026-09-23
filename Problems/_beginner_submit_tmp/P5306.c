#include <stdbool.h>
#include <stdlib.h>

typedef struct { int rid, node, last; int used; } Lease;
typedef struct {
    int ttl;
    Lease* a;
    int cap;
} LeaseManager;

static Lease* find(LeaseManager* obj, int rid) {
    for (int i = 0; i < obj->cap; i++)
        if (obj->a[i].used && obj->a[i].rid == rid) return &obj->a[i];
    return NULL;
}

static Lease* alloc_slot(LeaseManager* obj) {
    for (int i = 0; i < obj->cap; i++) if (!obj->a[i].used) return &obj->a[i];
    int ncap = obj->cap ? obj->cap * 2 : 16;
    obj->a = (Lease*)realloc(obj->a, ncap * sizeof(Lease));
    for (int i = obj->cap; i < ncap; i++) obj->a[i].used = 0;
    Lease* p = &obj->a[obj->cap];
    obj->cap = ncap;
    return p;
}

static bool alive_one(LeaseManager* obj, Lease* e, int time) {
    return e && e->used && time < (long long)e->last + obj->ttl;
}

LeaseManager* leaseManagerCreate(int ttl) {
    LeaseManager* obj = (LeaseManager*)calloc(1, sizeof(LeaseManager));
    obj->ttl = ttl;
    return obj;
}

void leaseManagerFree(LeaseManager* obj) {
    if (!obj) return;
    free(obj->a);
    free(obj);
}

bool leaseManagerAcquire(LeaseManager* obj, int resourceId, int nodeId, int time) {
    Lease* e = find(obj, resourceId);
    if (alive_one(obj, e, time) && e->node != nodeId) return false;
    if (!e) { e = alloc_slot(obj); e->rid = resourceId; e->used = 1; }
    e->node = nodeId; e->last = time; e->used = 1;
    return true;
}

bool leaseManagerRenew(LeaseManager* obj, int resourceId, int nodeId, int time) {
    Lease* e = find(obj, resourceId);
    if (!alive_one(obj, e, time) || e->node != nodeId) return false;
    e->last = time;
    return true;
}

bool leaseManagerRelease(LeaseManager* obj, int resourceId, int nodeId) {
    Lease* e = find(obj, resourceId);
    if (!e || !e->used || e->node != nodeId) return false;
    e->used = 0;
    return true;
}

int leaseManagerHolder(LeaseManager* obj, int resourceId, int time) {
    Lease* e = find(obj, resourceId);
    if (!alive_one(obj, e, time)) return -1;
    return e->node;
}

int leaseManagerAliveCount(LeaseManager* obj, int time) {
    int cnt = 0;
    for (int i = 0; i < obj->cap; i++)
        if (alive_one(obj, &obj->a[i], time)) cnt++;
    return cnt;
}
