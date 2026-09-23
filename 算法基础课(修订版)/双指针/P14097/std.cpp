#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);

    // 输入序列 a 和 b
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    for (int i = 0; i < m; i++) {
        cin >> b[i];
    }

    int i = 0, j = 0;
    // 使用双指针判断子序列
    while (i < n && j < m) {
        if (a[i] == b[j]) {
            i++;  // 找到匹配的元素，移动 a 的指针
        }
        j++;  // 无论是否匹配，b 的指针都要移动
    }

    // 如果 i 达到 n，说明 a 是 b 的子序列
    if (i == n) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }

    return 0;
}
