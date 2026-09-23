#include <iostream>
#include <vector>
using namespace std;

const int MAX_ID = 2000;

// 从 start 出发走完整棵下属树，把沿途每人的重要度加起来
// 用栈做 DFS，避免链状组织把递归撑爆
int solve(const vector<int>& importance, const vector<vector<int>>& children, int start) {
    int total = 0;
    vector<int> stack;
    stack.push_back(start);
    while (!stack.empty()) {
        int u = stack.back();
        stack.pop_back();
        total += importance[u];
        // 把直属下属压栈，之后会继续走到间接下属
        for (int i = 0; i < (int)children[u].size(); i++) {
            stack.push_back(children[u][i]);
        }
    }
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, qid;
    cin >> n >> qid;
    // 下标直接当员工 ID 用，题目保证 1..2000
    vector<int> importance(MAX_ID + 1, 0);
    vector<vector<int>> children(MAX_ID + 1);
    for (int i = 0; i < n; i++) {
        int eid, imp, m;
        cin >> eid >> imp >> m;
        importance[eid] = imp;
        // m=0 时不会再读下属 id
        children[eid].resize(m);
        for (int j = 0; j < m; j++) {
            cin >> children[eid][j];
        }
    }
    cout << solve(importance, children, qid) << '\n';
    return 0;
}
