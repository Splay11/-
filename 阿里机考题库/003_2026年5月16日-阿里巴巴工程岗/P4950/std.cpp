#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<int> g(m + 1);
        for (int i = 1; i <= m; ++i) cin >> g[i];
        const long long INF = 1e18;
        vector<long long> dis(m + 1, INF);
        dis[1] = 0;
        deque<int> dq;
        dq.push_back(1);
        while (!dq.empty()) {
            int x = dq.front();
            dq.pop_front();
            int y = g[x];
            if (dis[y] > dis[x]) { // 传送花费 0
                dis[y] = dis[x];
                dq.push_front(y);
            }
            if (x < m && dis[x + 1] > dis[x] + 1) { // 右移花费 1
                dis[x + 1] = dis[x] + 1;
                dq.push_back(x + 1);
            }
        }
        cout << dis[m] << '\n';
    }
    return 0;
}
