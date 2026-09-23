#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; cin >> n;
        string s;
        // 读第一个串，初始化最小频次
        cin >> s;
        array<int,26> mn{}; // 默认全 0
        for (char c : s) mn[c - 'a']++;

        // 合并其余 n-1 个串的最小频次
        for (int i = 1; i < n; ++i) {
            cin >> s;
            array<int,26> cnt{}; // 清零
            for (char c : s) cnt[c - 'a']++;
            for (int j = 0; j < 26; ++j) mn[j] = min(mn[j], cnt[j]);
        }

        // 构造答案（按字典序最小）
        string ans;
        for (int j = 0; j < 26; ++j) ans.append(mn[j], char('a' + j));
        if (ans.empty()) cout << -1 << '\n';
        else cout << ans << '\n';
    }
    return 0;
}
