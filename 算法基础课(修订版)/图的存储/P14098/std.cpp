#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n; // 顶点数
    cin >> n;
    vector<vector<int>> adjA(n + 1), adjB(n + 1);
    
    // 读取并转换图 A
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            int val;
            cin >> val;
            if (val == 1) adjA[i].push_back(j);
        }
    }
    
    // 读取图 B
    for (int i = 0; i < n; i++) {
        int node, k;
        cin >> node >> k;
        adjB[node].resize(k);
        for (int j = 0; j < k; j++) {
            cin >> adjB[node][j];
        }
    }
    
    // 对邻接表排序
    for (int i = 1; i <= n; i++) {
        sort(adjA[i].begin(), adjA[i].end());
        sort(adjB[i].begin(), adjB[i].end());
    }
    
    // 比较邻接表
    bool same = true;
    for (int i = 1; i <= n; i++) {
        if (adjA[i] != adjB[i]) {
            same = false;
            break;
        }
    }
    
    cout << (same ? "YES" : "NO") << endl;
    return 0;
}
