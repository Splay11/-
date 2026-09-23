#include <iostream>
#include <vector>

using namespace std;

const int MOD = 1e9 + 7;
vector<vector<int>> adj;
vector<char> colors;
int result = 0;

vector<bool> dfs(int node, int parent) {
    // 标记当前子树是否包含红色和黑色
    bool hasRed = false, hasBlack = false;
    if (colors[node] == 'R') hasRed = true;
    else hasBlack = true;

    for (int neighbor : adj[node]) {
        if (neighbor != parent) {
            vector<bool> child = dfs(neighbor, node);
            if(child[0]){
                hasRed = true;
            }
            if(child[1]){
                hasBlack = true;
            }
        }
    }
    // 如果当前子树既有红色又有黑色节点，则满足条件
    if (hasRed && hasBlack) {
        result++;
    }

    return {hasRed, hasBlack};
}

int main() {
    int n;
    cin >> n;
    colors.resize(n);
    adj.resize(n);
    
    for (int i = 0; i < n; i++) {
        cin >> colors[i];
    }
    
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u-1].push_back(v-1);
        adj[v-1].push_back(u-1);
    }

    dfs(0, -1);
    cout << result << endl;
    return 0;
}
