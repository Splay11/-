#include <bits/stdc++.h>
using namespace std;

vector<int> build(int m) {
    // 1..m 总和为偶数才可能有解：m mod 4 为 0 或 3
    if (m % 4 == 1 || m % 4 == 2) return {};
    vector<int> w;
    int start;
    if (m % 4 == 3) {
        w = {1, 2, -3};
        start = 4;
    } else {
        start = 1;
    }
    // 四元组 x,-(x+1),-(x+2),x+3 和为 0
    for (int x = start; x <= m; x += 4) {
        w.push_back(x);
        w.push_back(-(x + 1));
        w.push_back(-(x + 2));
        w.push_back(x + 3);
    }
    return w;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<int> w = build(m);
        if (w.empty()) {
            cout << -1 << '\n';
        } else {
            for (int i = 0; i < m; ++i) {
                if (i) cout << ' ';
                cout << w[i];
            }
            cout << '\n';
        }
    }
    return 0;
}
