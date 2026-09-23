#include <iostream>
#include <string>
#include <vector>
using namespace std;

const int MOD = 1000000007;

/**
 * 相邻不同串计数 — 逐位 DP
 * f[c]: 以字符 c 结尾的合法前缀方案数
 * 转移: nf[c] = (total - f[c]) % MOD
 */
int solve_one(int m, const string& pat) {
    vector<long long> f(26, 0);

    // 第一位初始化
    if (pat[0] == '?') {
        for (int c = 0; c < 26; ++c) f[c] = 1;
    } else {
        f[pat[0] - 'a'] = 1;
    }

    long long total = 0;  // 当前前缀的 f 之和
    for (int c = 0; c < 26; ++c) total += f[c];
    total %= MOD;

    for (int i = 1; i < m; ++i) {
        vector<long long> nf(26, 0);  // 新一位的 dp 数组
        if (pat[i] == '?') {
            for (int c = 0; c < 26; ++c)
                nf[c] = (total - f[c] + MOD) % MOD;
        } else {
            int c = pat[i] - 'a';
            nf[c] = (total - f[c] + MOD) % MOD;
        }

        f.swap(nf);
        total = 0;
        for (int c = 0; c < 26; ++c) total += f[c];
        total %= MOD;
        if (total == 0) break;  // 无法继续
    }

    return (int)total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int m;
        string pat;
        cin >> m >> pat;
        cout << solve_one(m, pat) << '\n';
    }
    return 0;
}
