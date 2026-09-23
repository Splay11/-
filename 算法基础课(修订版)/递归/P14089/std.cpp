#include <iostream>
using namespace std;

// 递归函数计算斐波那契数列
int fibonacci(int n) {
    if (n == 0) return 0; // 斐波那契数列的第0项
    if (n == 1) return 1; // 斐波那契数列的第1项
    return fibonacci(n - 1) + fibonacci(n - 2); // 递归计算F(n)
}

int main() {
    int n;
    cin >> n; // 输入整数n
    cout << fibonacci(n) << endl; // 输出斐波那契数列的第n项
    return 0;
}
