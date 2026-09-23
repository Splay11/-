#include <stdio.h>

#define N 2005

long long dp[N][N];
int a[N];

// 删完数组 a[l..r] 的最小代价（下标从 0 开始）
long long min_cost(int n) {
    int i, j, length;
    // 长度为 1：当前长度是 1，代价就是元素本身
    for (i = 0; i < n; i++) {
        dp[i][i] = a[i];
    }
    // 按区间长度从小到大填表，保证转移时子区间已经算好
    for (length = 2; length <= n; length++) {
        for (i = 0; i + length - 1 < n; i++) {
            j = i + length - 1;
            // 先删左端 a[i]，代价为当前长度 * a[i]，再加上删完剩余区间的最优代价
            long long left = (long long)length * a[i] + dp[i + 1][j];
            // 先删右端 a[j]，同理
            long long right = (long long)length * a[j] + dp[i][j - 1];
            dp[i][j] = left < right ? left : right;
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
    printf("%lld\n", min_cost(n));
    return 0;
}
