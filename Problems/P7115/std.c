#include <stdio.h>

#define N 2005

long long dp[N][N];
long long pre[N];
int a[N];

// 当前行动者从 a[0..n-1] 能拿到的最大得分
long long first_score(int n) {
    int i, j, length;
    // pre[k] 为前 k 个数的和，用来 O(1) 求区间和
    pre[0] = 0;
    for (i = 0; i < n; i++) {
        pre[i + 1] = pre[i] + a[i];
    }
    // dp[i][j]：轮到当前玩家时，从下标 i..j 能拿到的最大得分
    for (i = 0; i < n; i++) {
        dp[i][i] = a[i];
    }
    // 按区间长度从小到大填表
    for (length = 2; length <= n; length++) {
        for (i = 0; i + length - 1 < n; i++) {
            j = i + length - 1;
            long long tot = pre[j + 1] - pre[i];
            // 取左端则对手得 dp[i+1][j]；取右端则对手得 dp[i][j-1]
            // 当前得分 = 区间和 - 对手得分，应让对手拿到的更少
            long long opp = dp[i + 1][j] < dp[i][j - 1] ? dp[i + 1][j] : dp[i][j - 1];
            dp[i][j] = tot - opp;
        }
    }
    return dp[0][n - 1];
}

int main(void) {
    int n, i;
    scanf("%d", &n);
    for (i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }
    printf("%lld\n", first_score(n));
    return 0;
}
