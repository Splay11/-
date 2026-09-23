#include <iostream>
#include <vector>
using namespace std;

// 求两个数组最长公共子数组（必须连续）的长度
int longestCommonSubarray(const vector<int>& a, const vector<int>& b) {
    int n = (int)a.size();
    int m = (int)b.size();
    // dp[i][j]：以 a[i-1]、b[j-1] 结尾的公共子数组最长能有多长
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i - 1] == b[j - 1]) {
                // 当前这一对相等，长度就是左上角那格再加 1
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > ans) {
                    ans = dp[i][j];
                }
            }
            // 不相等时 dp[i][j] 保持 0：公共子数组在这里断开
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    for (int i = 0; i < m; i++) {
        cin >> b[i];
    }
    cout << longestCommonSubarray(a, b) << '\n';
    return 0;
}
