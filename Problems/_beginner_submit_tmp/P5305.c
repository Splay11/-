#include <stdlib.h>

typedef struct { int s, e, sc; } Seg;

static int cmp_end(const void* pa, const void* pb) {
    int ae = ((const Seg*)pa)->e, be = ((const Seg*)pb)->e;
    if (ae < be) return -1;
    if (ae > be) return 1;
    return 0;
}

int maxSessionScore(int** sessions, int sessionsSize, int* sessionsColSize) {
    (void)sessionsColSize;
    Seg* a = (Seg*)malloc((sessionsSize > 0 ? sessionsSize : 1) * sizeof(Seg));
    int n = 0;
    for (int i = 0; i < sessionsSize; i++) {
        if (sessions[i][1] > sessions[i][0]) {
            a[n].s = sessions[i][0]; a[n].e = sessions[i][1]; a[n].sc = sessions[i][2]; n++;
        }
    }
    if (n == 0) { free(a); return 0; }
    qsort(a, n, sizeof(Seg), cmp_end);
    int* dp = (int*)calloc(n + 1, sizeof(int));
    for (int i = 1; i <= n; i++) {
        int s = a[i - 1].s, sc = a[i - 1].sc;
        int lo = 0, hi = i - 2, p = -1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (a[mid].e <= s) { p = mid; lo = mid + 1; }
            else hi = mid - 1;
        }
        int take = sc + (p >= 0 ? dp[p + 1] : 0);
        dp[i] = dp[i - 1] > take ? dp[i - 1] : take;
    }
    int ans = dp[n];
    free(a); free(dp);
    return ans;
}
