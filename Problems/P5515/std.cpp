#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int S;
    cin >> S;
    // dp[s]：当前已打若干枪得到总分 s 的方案数
    vector<long long> dp(S + 1, 0);
    dp[0] = 1;
    for (int shot = 0; shot < 10; shot++) {
        vector<long long> ndp(S + 1, 0);
        for (int s = 0; s <= S; s++) {
            if (dp[s] == 0) continue;
            for (int v = 0; v <= 10; v++) {
                if (s + v <= S) ndp[s + v] += dp[s];
            }
        }
        dp.swap(ndp);
    }
    cout << dp[S] << "\n";
    return 0;
}
