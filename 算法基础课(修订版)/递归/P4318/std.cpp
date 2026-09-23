#include <bits/stdc++.h>
using namespace std;

void dfs(const vector<int>& a, int start, int target, vector<int>& path, vector<vector<int>>& ans) {
    if (target == 0) {
        ans.push_back(path);
        return;
    }
    for (int i = start; i < (int)a.size(); ++i) {
        if (i > start && a[i] == a[i - 1]) continue;    // 同层去重
        if (a[i] > target) break;                        // 剪枝
        path.push_back(a[i]);
        dfs(a, i + 1, target - a[i], path, ans);        // 每个数只能用一次
        path.pop_back();
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    int target; cin >> target;

    sort(a.begin(), a.end());
    vector<vector<int>> ans;
    vector<int> path;
    dfs(a, 0, target, path, ans);

    sort(ans.begin(), ans.end()); // 按字典序升序输出
    if (ans.empty()) {
        cout << "\n";
        return 0;
    }
    for (auto& v : ans) {
        for (int i = 0; i < (int)v.size(); ++i) {
            if (i) cout << ' ';
            cout << v[i];
        }
        cout << '\n';
    }
    return 0;
}
