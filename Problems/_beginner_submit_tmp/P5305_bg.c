#include <stdlib.h>

typedef struct { int s, e, sc; } Seg;

static int cmp_end(const void* pa, const void* pb) {
    int ae = ((const Seg*)pa)->e, be = ((const Seg*)pb)->e;
    if (ae < be) return -1;
    if (ae > be) return 1;
    return 0;
}

int maxMaintenanceScore(int** windows, int windowsSize, int* windowsColSize) {
    (void)windowsColSize;
    Seg* a = (Seg*)malloc((windowsSize > 0 ? windowsSize : 1) * sizeof(Seg));
    int n = 0;
    for (int i = 0; i < windowsSize; i++) {
        if (windows[i][1] > windows[i][0]) {
            a[n].s = windows[i][0]; a[n].e = windows[i][1]; a[n].sc = windows[i][2]; n++;
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
