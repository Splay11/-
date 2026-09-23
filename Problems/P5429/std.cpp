#include <iostream>
#include <vector>
using namespace std;

// 按编号升序回溯，枚举长度为 t 的无冲突组合
void dfs(int start, int m, int t, int g, int lo, int hi,
         const vector<int>& w, vector<int>& chosen, int total,
         int& count, vector<vector<int>>& top) {
    // 已经取满 t 个：只检查负荷和
    if ((int)chosen.size() == t) {
        if (lo <= total && total <= hi) {
            count++;
            if ((int)top.size() < 3) {
                top.push_back(chosen);
            }
        }
        return;
    }
    int remain = t - (int)chosen.size();
    // 从 start 起枚举下一个编号；编号必须递增，保证字典序
    for (int i = start; i <= m; i++) {
        // 剩下位置不够凑满 t 个，后面更大的 i 更不够
        if (m - i + 1 < remain) {
            break;
        }
        chosen.push_back(i);
        // 下一个合法起点至少是 i+g+1，这样相邻差一定大于 g
        dfs(i + g + 1, m, t, g, lo, hi, w, chosen, total + w[i - 1], count, top);
        chosen.pop_back();
    }
}

pair<int, vector<vector<int>>> collectSchemes(int m, int t, int g, int lo, int hi,
                                               const vector<int>& w) {
    int count = 0;
    vector<vector<int>> top;
    vector<int> chosen;
    dfs(1, m, t, g, lo, hi, w, chosen, 0, count, top);
    return {count, top};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, t, g, lo, hi;
    cin >> m >> t >> g >> lo >> hi;
    vector<int> w(m);
    for (int i = 0; i < m; i++) {
        cin >> w[i];
    }
    auto result = collectSchemes(m, t, g, lo, hi, w);
    cout << result.first << '\n';
    for (const auto& scheme : result.second) {
        for (int i = 0; i < (int)scheme.size(); i++) {
            if (i) {
                cout << ' ';
            }
            cout << scheme[i];
        }
        cout << '\n';
    }
    return 0;
}
