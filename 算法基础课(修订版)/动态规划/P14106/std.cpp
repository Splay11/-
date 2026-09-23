#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;  // 输入楼梯的级数

    // D 数组，D[i] 表示到达第 i 级台阶的方法数
    int D[n + 1];
    
    // 初始化
    D[1] = 1;  // 第 1 级台阶的方法数为 1
    D[2] = 2;  // 第 2 级台阶的方法数为 2

    // 递推
    for (int i = 3; i <= n; i++) {
        D[i] = D[i - 1] + D[i - 2];  // 根据递推公式
    }

    // 输出结果
    cout << D[n] << endl;

    return 0;
}
