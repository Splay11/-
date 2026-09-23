#include <iostream>
using namespace std;

// 递归函数，计算从 (i, j) 到 (n - 1, n - 1) 的路径数
int uniquePaths(int i, int j, int n) {
    // 如果到达右下角，则路径数为1
    if (i == n - 1 && j == n - 1) {
        return 1;
    }

    int paths = 0;
    
    // 向下走
    if (i < n - 1) {
        paths += uniquePaths(i + 1, j, n);
    }
    
    // 向右走
    if (j < n - 1) {
        paths += uniquePaths(i, j + 1, n);
    }
    
    return paths;
}

int main() {
    int n;
    cin >> n;  // 输入网格的大小
    cout << uniquePaths(0, 0, n) << endl;  // 从 (0, 0) 出发
    return 0;
}
