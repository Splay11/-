#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

int main() {
    int n, Q;
    cin >> n >> Q;
    vector<int> a(n);
    unordered_map<int, vector<int>> positions;
    
    // 预处理：记录每个数的位置
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
        positions[a[i]].push_back(i + 1);  // 存储的是位置，位置从1开始
    }
    
    // 处理每个查询
    while (Q--) {
        int x, k;
        cin >> x >> k;
        
        // 如果x在数组中出现的次数少于k次，返回-1
        if (positions[x].size() < k) {
            cout << -1 << endl;
        } else {
            // 返回x的第k次出现的位置
            cout << positions[x][k - 1] << endl;
        }
    }
    
    return 0;
}
