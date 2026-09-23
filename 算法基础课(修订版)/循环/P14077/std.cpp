#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int n, m;
    cin >> n >> m;  // 输入矩阵的行和列
    vector<vector<int>> matrix(n, vector<int>(m));
    
    // 输入矩阵元素
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> matrix[i][j];
        }
    }
    
    int q;
    cin >> q;  // 输入查询次数
    
    while (q--) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;  // 输入查询的坐标
        
        // 转换为 0-indexed
        x1--; y1--; x2--; y2--;
        
        int max_val = matrix[x1][y1];  // 初始化最大值
        
        // 遍历子矩阵寻找最大值
        for (int i = x1; i <= x2; i++) {
            for (int j = y1; j <= y2; j++) {
                max_val = max(max_val, matrix[i][j]);
            }
        }
        
        cout << max_val << endl;  // 输出结果
    }
    
    return 0;
}
