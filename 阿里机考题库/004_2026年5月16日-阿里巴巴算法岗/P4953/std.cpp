#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
const int MAXN = 200000 + 5;

long long pw2[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 预处理 2^k
    pw2[0] = 1;
    for (int i = 1; i < MAXN; ++i) pw2[i] = pw2[i - 1] * 2 % MOD;

    int q;
    cin >> q;
    while (q--) {
        int m;
        string z;
        cin >> m >> z;
        bool seen[26] = {};
        int kind = 0, diff = 0;
        for (char c : z) {
            int id = c - 'a';
            if (!seen[id]) {
                seen[id] = true;
                ++kind;
            }
        }
        for (int i = 0; i + 1 < m; ++i) {
            if (z[i] != z[i + 1]) ++diff;
        }
        // 失灵字母只能是未出现过的；每种贡献 2^(diff+2)
        long long ans = (26 - kind) * pw2[diff + 2] % MOD;
        cout << ans << '\n';
    }
    return 0;
}
