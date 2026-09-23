#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    // 输入整数 n
    cin >> n;

    vector<int> a(n);
    // 输入 n 个整数到数组 a 中
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    // 输出数组 a 的所有元素，空格分隔
    for (int i = 0; i < n; i++) {
        cout << a[i];
        if (i != n - 1) cout << " "; // 避免最后一个元素后有空格
    }

    return 0;
}
