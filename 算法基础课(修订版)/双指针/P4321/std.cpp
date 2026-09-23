#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    string s;
    cin >> s;

    // 矛盾矩阵
    bool conflict[26][26] = {false};
    for (int i = 0; i < m; ++i) {
        char a, b;
        cin >> a >> b;
        int ia = a - 'A', ib = b - 'A';
        if (ia != ib) {
            conflict[ia][ib] = true;
            conflict[ib][ia] = true;
        }
    }

    vector<int> last(26, -1); // 最近出现位置
    long long ans = 0;
    int l = 0;

    for (int r = 0; r < n; ++r) {
        int c = s[r] - 'A';
        // 推进 l，排除与 c 冲突的字母在窗口内
        for (int x = 0; x < 26; ++x) {
            if (conflict[c][x] && last[x] >= l) {
                l = last[x] + 1;
            }
        }
        // 以 r 结尾的和谐子串数量
        ans += (r - l + 1);
        // 更新 c 的最近位置
        last[c] = r;
    }

    cout << ans << "\n";
    return 0;
}
