#include <stdio.h>
#include <stdlib.h>

#define INF 1000000000
#define MAXK 16
#define MAXN 25

int grid[MAXN][MAXN];
int pr[MAXK], pc[MAXK];
int distv[MAXK][MAXK];
int dp[1 << MAXK][MAXK];

// 把非 0 格子当成城市，用状压 DP 求从中心出发并返回的最短回路
int min_steps(int n, int m) {
    int sr = n / 2, sc = m / 2;
    int k = 0;
    int i, j, a, b, mask;
    // 点 0 固定为中心，其余点为中心以外的非 0 格子
    pr[k] = sr;
    pc[k] = sc;
    k++;
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            if (grid[i][j] != 0 && (i != sr || j != sc)) {
                pr[k] = i;
                pc[k] = j;
                k++;
            }
        }
    }
    if (k == 1) {
        return 0;
    }
    for (a = 0; a < k; a++) {
        for (b = 0; b < k; b++) {
            distv[a][b] = abs(pr[a] - pr[b]) + abs(pc[a] - pc[b]);
        }
    }
    int full = 1 << k;
    for (mask = 0; mask < full; mask++) {
        for (i = 0; i < k; i++) {
            dp[mask][i] = INF;
        }
    }
    dp[1][0] = 0;
    for (mask = 0; mask < full; mask++) {
        for (i = 0; i < k; i++) {
            if (((mask >> i) & 1) == 0 || dp[mask][i] >= INF) {
                continue;
            }
            for (j = 0; j < k; j++) {
                if ((mask >> j) & 1) {
                    continue;
                }
                int nxt = mask | (1 << j);
                int cand = dp[mask][i] + distv[i][j];
                if (cand < dp[nxt][j]) {
                    dp[nxt][j] = cand;
                }
            }
        }
    }
    int end = full - 1;
    int ans = INF;
    // 访问完全部点后，还要走回中心
    for (i = 0; i < k; i++) {
        int cand = dp[end][i] + distv[i][0];
        if (cand < ans) {
            ans = cand;
        }
    }
    return ans;
}

int main(void) {
    int n, m, i, j;
    scanf("%d %d", &n, &m);
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            scanf("%d", &grid[i][j]);
        }
    }
    printf("%d\n", min_steps(n, m));
    return 0;
}
