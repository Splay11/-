#include <stdlib.h>

long long minCircleMerge(int* weights, int n) {
    if (n <= 1) return 0;
    if (n == 2) return (long long)weights[0] + weights[1];

    int m = 2 * n;
    int* a = (int*)malloc(sizeof(int) * m);
    for (int i = 0; i < n; i++) {
        a[i] = weights[i];
        a[i + n] = weights[i];
    }
    long long* pref = (long long*)calloc((unsigned)(m + 1), sizeof(long long));
    for (int i = 0; i < m; i++) pref[i + 1] = pref[i] + a[i];

    const long long INF = (1LL << 62);
    long long* dp = (long long*)calloc((unsigned)m * (unsigned)m, sizeof(long long));
    #define DP(i, j) dp[(long long)(i) * m + (j)]

    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < m; i++) {
            int j = i + len - 1;
            long long best = INF;
            for (int k = i; k < j; k++) {
                long long cur = DP(i, k) + DP(k + 1, j);
                if (cur < best) best = cur;
            }
            DP(i, j) = best + (pref[j + 1] - pref[i]);
        }
    }
    long long ans = INF;
    for (int i = 0; i < n; i++) {
        if (DP(i, i + n - 1) < ans) ans = DP(i, i + n - 1);
    }
    free(a);
    free(pref);
    free(dp);
    return ans;
    #undef DP
}
