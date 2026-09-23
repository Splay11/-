#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 按层搭建三角栈道，求从 start 出发的无向欧拉回路
vector<int> solve(int h, int start) {
    int n = h * (h + 1) / 2;
    vector<vector<int> > g(n + 1);
    vector<int> eu, ev;

    // 加入一条无向栈道，两端都记下边号
    auto add = [&](int a, int b) {
        int eid = (int)eu.size();
        eu.push_back(a);
        ev.push_back(b);
        g[a].push_back(eid);
        g[b].push_back(eid);
    };

    for (int r = 2; r <= h; r++) {
        // base / prev 分别是本层、上一层「编号减一」的偏移
        int base = r * (r - 1) / 2;
        int prev = (r - 1) * (r - 2) / 2;
        for (int c = 1; c < r; c++) {
            int u = base + c;
            int v = base + c + 1;
            int w = prev + c;
            // 同层相邻，以及接到上一层同一台位的两条斜栈道
            add(u, v);
            add(u, w);
            add(v, w);
        }
    }

    int m = (int)eu.size();
    vector<char> used(m, 0);
    vector<int> ptr(n + 1, 0);
    vector<int> stack;
    vector<int> circ;
    stack.push_back(start);
    // Hierholzer：沿未用边走，走不通时把点弹入回路（得到逆序）
    while (!stack.empty()) {
        int u = stack.back();
        while (ptr[u] < (int)g[u].size() && used[g[u][ptr[u]]]) {
            ptr[u]++;
        }
        if (ptr[u] == (int)g[u].size()) {
            circ.push_back(u);
            stack.pop_back();
        } else {
            int eid = g[u][ptr[u]];
            ptr[u]++;
            used[eid] = 1;
            int a = eu[eid], b = ev[eid];
            stack.push_back(a == u ? b : a);
        }
    }
    reverse(circ.begin(), circ.end());
    return circ;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int k;
    cin >> k;
    for (int t = 0; t < k; t++) {
        int h, s;
        cin >> h >> s;
        vector<int> path = solve(h, s);
        for (int i = 0; i < (int)path.size(); i++) {
            if (i) cout << ' ';
            cout << path[i];
        }
        cout << "\n";
    }
    return 0;
}
