#include <stdlib.h>
#include <string.h>

enum { CAP = 262144 };

static int* key_t;
static int* val_t;
static char* used_t;

static int hget(int key) {
    unsigned h = (unsigned)key * 2654435761u;
    for (int i = 0; i < CAP; i++) {
        unsigned idx = (h + i) & (CAP - 1);
        if (!used_t[idx]) return 0;
        if (key_t[idx] == key) return val_t[idx];
    }
    return 0;
}

static void hadd(int key, int dlt, int* oldv) {
    unsigned h = (unsigned)key * 2654435761u;
    for (int i = 0; i < CAP; i++) {
        unsigned idx = (h + i) & (CAP - 1);
        if (!used_t[idx]) {
            used_t[idx] = 1;
            key_t[idx] = key;
            *oldv = 0;
            val_t[idx] = dlt;
            return;
        }
        if (key_t[idx] == key) {
            *oldv = val_t[idx];
            val_t[idx] += dlt;
            return;
        }
    }
}

int longestAuditWindow(int* events, int eventsSize, int k) {
    if (k <= 0 || eventsSize <= 0) return 0;
    key_t = (int*)malloc(CAP * sizeof(int));
    val_t = (int*)calloc(CAP, sizeof(int));
    used_t = (char*)calloc(CAP, 1);
    int distinct = 0, left = 0, ans = 0;
    for (int right = 0; right < eventsSize; right++) {
        int oldv;
        hadd(events[right], 1, &oldv);
        if (oldv == 0) distinct++;
        while (distinct > k) {
            int ov;
            hadd(events[left], -1, &ov);
            if (ov == 1) distinct--;
            left++;
        }
        if (right - left + 1 > ans) ans = right - left + 1;
    }
    free(key_t); free(val_t); free(used_t);
    return ans;
}
