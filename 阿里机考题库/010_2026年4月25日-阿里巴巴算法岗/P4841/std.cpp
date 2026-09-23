#include <bits/stdc++.h>
using namespace std;

long long solveOne(int cnt, long long seed, vector<int>& modSet) {
    int mn = *min_element(modSet.begin(), modSet.end());
    int maxMod = *max_element(modSet.begin(), modSet.end());

    // 种子已小于最小模数，后续折减均不改变当前值
    if (seed < mn) return seed;

    // 去重模数，减少转移枚举
    vector<int> mods;
    vector<int> exist(maxMod + 1, 0);
    for (int v : modSet) {
        if (!exist[v]) {
            exist[v] = 1;
            mods.push_back(v);
        }
    }

    vector<int> vis(maxMod + 1, 0);
    queue<int> q;

    // 第一次有效折减：seed mod order_i
    for (int a : mods) {
        if (a <= seed) {
            int r = (int)(seed % a);
            if (!vis[r]) {
                vis[r] = 1;
                q.push(r);
            }
        }
    }

    // BFS 枚举所有可达的 cur
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        for (int a : mods) {
            if (a <= cur) {
                int nxt = cur % a;
                if (!vis[nxt]) {
                    vis[nxt] = 1;
                    q.push(nxt);
                }
            }
        }
    }

    // 最终余值必须严格小于 mn
    int ans = 0;
    for (int i = 0; i < mn; i++) {
        if (vis[i]) ans = i;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int cnt;
        long long seed;
        cin >> cnt >> seed;

        vector<int> modSet(cnt);
        for (int i = 0; i < cnt; i++) cin >> modSet[i];

        cout << solveOne(cnt, seed, modSet) << '\n';
    }

    return 0;
}
