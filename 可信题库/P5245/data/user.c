#include <stdbool.h>
#include <stdlib.h>

typedef struct TTLCache TTLCache;

struct TTLCache {
    int unused;
};

TTLCache* tTLCacheCreate(int capacity) {
    (void)capacity;
    return (TTLCache*)calloc(1, sizeof(TTLCache));
}

void tTLCacheFree(TTLCache* obj) {
    free(obj);
}

void tTLCachePut(TTLCache* obj, int key, int value, int expireAt) {
    (void)obj;
    (void)key;
    (void)value;
    (void)expireAt;
}

int tTLCacheGet(TTLCache* obj, int key, int now) {
    (void)obj;
    (void)key;
    (void)now;
    return -1;
}

int tTLCachePurge(TTLCache* obj, int now) {
    (void)obj;
    (void)now;
    return 0;
}

int tTLCacheSize(TTLCache* obj) {
    (void)obj;
    return 0;
}
