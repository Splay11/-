#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> d(n + 1);
    for (int i = 1; i <= n; i++) cin >> d[i];

    // dp[i][j]：中序区间最高加分；rt[i][j]：最优根（平分取更左）
    vector<vector<long long>> dp(n + 2, vector<long long>(n + 2, 0));
    vector<vector<int>> rt(n + 2, vector<int>(n + 2, 0));
    for (int i = 1; i <= n; i++) {
        dp[i][i] = d[i];
        rt[i][i] = i;
        dp[i][i - 1] = 1;
    }
    dp[n + 1][n] = 1;

    for (int len = 2; len <= n; len++) {
        for (int i = 1; i + len - 1 <= n; i++) {
            int j = i + len - 1;
            long long best = -1;
            int bestR = i;
            for (int k = i; k <= j; k++) {
                long long left = (k > i) ? dp[i][k - 1] : 1;
                long long right = (k < j) ? dp[k + 1][j] : 1;
                long long score = left * right + d[k];
                if (score > best) {
                    best = score;
                    bestR = k;
                }
            }
            dp[i][j] = best;
            rt[i][j] = bestR;
        }
    }

    vector<int> seq;
    // 递归展开前序
    auto dfs = [&](auto&& self, int i, int j) -> void {
        if (i > j) return;
        int r = rt[i][j];
        seq.push_back(r);
        self(self, i, r - 1);
        self(self, r + 1, j);
    };
    dfs(dfs, 1, n);

    cout << dp[1][n] << '\n';
    for (size_t i = 0; i < seq.size(); i++) {
        if (i) cout << ' ';
        cout << seq[i];
    }
    cout << '\n';
    return 0;
}
