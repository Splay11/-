#include <iostream>
#include <vector>
using namespace std;

// 回溯枚举分配方案，按字典序生成
void dfs(int remain, int idx, int n, vector<int>& path, vector<vector<int>>& schemes) {
    if (idx == n - 1) {
        // 最后一人拿走全部剩余
        path.push_back(remain);
        schemes.push_back(path);
        path.pop_back();
        return;
    }
    // 当前人从少到多拿，保证字典序
    for (int x = 0; x <= remain; x++) {
        path.push_back(x);
        dfs(remain - x, idx + 1, n, path, schemes);
        path.pop_back();
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<vector<int>> schemes;
    vector<int> path;
    dfs(m, 0, n, path, schemes);
    for (auto& s : schemes) {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << s[i];
        }
        cout << '\n';
    }
    cout << schemes.size() << '\n';
    return 0;
}
