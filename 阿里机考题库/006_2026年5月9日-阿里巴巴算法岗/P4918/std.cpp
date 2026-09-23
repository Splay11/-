#include <bits/stdc++.h>
using namespace std;

string solve(int L, const string& g) {
    // 统计 L 导向数量：前 cnt 个起点从左侧出界
    int cnt = 0;
    for (char c : g) if (c == 'L') ++cnt;
    return string(cnt, 'L') + string(L - cnt, 'R');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int L;
        string g;
        cin >> L >> g;
        cout << solve(L, g) << '\n';
    }
    return 0;
}
