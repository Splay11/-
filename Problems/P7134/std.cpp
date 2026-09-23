#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

const int MAX_ID = 50000;

// 从 kill 出发走完整棵子树，把所有会被杀掉的进程收集起来再排序
// 用栈做 DFS，n 可以到 5e4，链状树递归会爆
vector<int> solve(const vector<int>& pids, const vector<int>& ppids, int kill) {
    vector<vector<int>> children(MAX_ID + 1);
    for (int i = 0; i < (int)pids.size(); i++) {
        // 父进程为 0 的是根，没有人再指向它的父亲
        if (ppids[i] != 0) {
            children[ppids[i]].push_back(pids[i]);
        }
    }
    vector<int> killed;
    vector<int> stack;
    stack.push_back(kill);
    while (!stack.empty()) {
        int u = stack.back();
        stack.pop_back();
        killed.push_back(u);
        // 杀掉 u 时，它的所有孩子也会被杀掉
        for (int i = 0; i < (int)children[u].size(); i++) {
            stack.push_back(children[u][i]);
        }
    }
    // 题面要求按进程 ID 从小到大输出
    sort(killed.begin(), killed.end());
    return killed;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, kill;
    cin >> n >> kill;
    vector<int> pids(n), ppids(n);
    for (int i = 0; i < n; i++) {
        cin >> pids[i];
    }
    for (int i = 0; i < n; i++) {
        cin >> ppids[i];
    }
    vector<int> ans = solve(pids, ppids, kill);
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
