#include <algorithm>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

// 按质量排序后，把热度能互相罩住的稿件并到同一连通块；块内可任意重排
int findp(vector<int>& parent, int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

void unite(vector<int>& parent, vector<int>& rankv, vector<int>& min_h, int x, int y) {
    x = findp(parent, x);
    y = findp(parent, y);
    if (x == y) {
        return;
    }
    if (rankv[x] < rankv[y]) {
        int tmp = x;
        x = y;
        y = tmp;
    }
    parent[y] = x;
    if (min_h[y] < min_h[x]) {
        min_h[x] = min_h[y];
    }
    if (rankv[x] == rankv[y]) {
        rankv[x]++;
    }
}

bool can_match(const vector<int>& p, const vector<int>& h, const vector<int>& t) {
    int m = (int)p.size();
    vector<int> parent(m), rankv(m, 0), min_h = h;
    for (int i = 0; i < m; i++) {
        parent[i] = i;
    }
    vector<int> order(m);
    for (int i = 0; i < m; i++) {
        order[i] = i;
    }
    // 质量升序，质量相同则热度升序
    sort(order.begin(), order.end(), [&](int i, int j) {
        if (p[i] != p[j]) {
            return p[i] < p[j];
        }
        return h[i] < h[j];
    });
    priority_queue<pair<int, int>, vector<pair<int, int> >, greater<pair<int, int> > > heap;
    for (int k = 0; k < m; k++) {
        int i = order[k];
        while (!heap.empty() && heap.top().first <= h[i]) {
            pair<int, int> cur = heap.top();
            heap.pop();
            int x = findp(parent, cur.second);
            if (min_h[x] != cur.first) {
                continue;
            }
            unite(parent, rankv, min_h, i, x);
        }
        int r = findp(parent, i);
        heap.push(make_pair(min_h[r], r));
    }
    vector<vector<int> > have(m), need(m);
    for (int i = 0; i < m; i++) {
        int r = findp(parent, i);
        have[r].push_back(h[i]);
        need[r].push_back(t[i]);
    }
    for (int r = 0; r < m; r++) {
        if (have[r].empty()) {
            continue;
        }
        sort(have[r].begin(), have[r].end());
        sort(need[r].begin(), need[r].end());
        if (have[r] != need[r]) {
            return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<int> p(m), h(m), t(m);
        for (int i = 0; i < m; i++) {
            cin >> p[i] >> h[i];
        }
        for (int i = 0; i < m; i++) {
            cin >> t[i];
        }
        cout << (can_match(p, h, t) ? "YES" : "NO") << '\n';
    }
    return 0;
}
