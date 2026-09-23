#include <iostream>
#include <vector>

using namespace std;
const int MOD = 1e9 + 7;

vector<vector<int>> adj; // 邻接表存储树结构
vector<int> ops;         // 运算类型数组

// 计算节点值
long long cc(long long a, long long b, int t) {
    return (t == 0) ? (a + b) % MOD : (a * b) % MOD;
}

// 递归计算节点 u 的权值
long long cal(int u) {
    if (adj[u].size() == 2) {
        return cc(cal(adj[u][0]), cal(adj[u][1]), ops[u]);
    }
    return 1; // 叶子节点权值固定为 1
}

int main() {
    int num;
    cin >> num;

    adj.resize(num);
    ops.resize(num);

    // 读取父子关系
    for (int i = 1; i < num; i++) {
        int parent;
        cin >> parent;
        adj[parent - 1].push_back(i);
    }

    // 读取运算类型
    for (int i = 0; i < num; i++) {
        cin >> ops[i];
    }

    // 计算并输出根节点权值
    cout << cal(0) << endl;

    return 0;
}
