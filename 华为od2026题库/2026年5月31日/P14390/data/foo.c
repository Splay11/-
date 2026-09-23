#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

long long maxEnergyDivisibleByK(int* nums, int n, int k) {
    int poolCap = 4 * n + k + 10;
    int* pos = (int*)malloc(poolCap * sizeof(int));
    long long* val = (long long*)malloc(poolCap * sizeof(long long));
    int* nxt = (int*)malloc(poolCap * sizeof(int));
    int* prv = (int*)malloc(poolCap * sizeof(int));
    int* head = (int*)malloc(k * sizeof(int));
    int* tail = (int*)malloc(k * sizeof(int));
    int poolIdx = 0;

    for (int j = 0; j < k; j++) {
        head[j] = -1;
        tail[j] = -1;
    }

    pos[poolIdx] = 0;
    val[poolIdx] = 0;
    nxt[poolIdx] = -1;
    prv[poolIdx] = -1;
    head[0] = poolIdx;
    tail[0] = poolIdx;
    poolIdx++;

    long long prefix = 0;
    long long ans = LLONG_MIN;
    int found = 0;

    for (int r = 1; r <= 2 * n; r++) {
        prefix += nums[(r - 1) % n];
        int mod = (int)(prefix % k);
        if (mod < 0) mod += k;

        while (head[mod] != -1 && pos[head[mod]] < r - n) {
            head[mod] = nxt[head[mod]];
            if (head[mod] != -1) prv[head[mod]] = -1;
            else tail[mod] = -1;
        }

        if (head[mod] != -1) {
            long long cand = prefix - val[head[mod]];
            if (cand > ans) ans = cand;
            found = 1;
        }

        while (tail[mod] != -1 && val[tail[mod]] >= prefix) {
            tail[mod] = prv[tail[mod]];
            if (tail[mod] != -1) nxt[tail[mod]] = -1;
            else head[mod] = -1;
        }

        pos[poolIdx] = r;
        val[poolIdx] = prefix;
        nxt[poolIdx] = -1;
        prv[poolIdx] = tail[mod];
        if (tail[mod] != -1) nxt[tail[mod]] = poolIdx;
        else head[mod] = poolIdx;
        tail[mod] = poolIdx;
        poolIdx++;
    }

    free(pos);
    free(val);
    free(nxt);
    free(prv);
    free(head);
    free(tail);

    return found ? ans : 0;
}
