#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

int main() {
    int n;
    cin >> n;
    int res = 0;

    // 使用哈希表存储频率
    unordered_map<int, int> countLeft;
    unordered_map<int, int> countRight;

    // 读取数组
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    // 初始化 countRight
    for (int i = 0; i < n; i++) {
        countRight[a[i]]++;
    }

    // 遍历每个元素，计算符合条件的三元组数量
    for (int i = 0; i < n; i++) {
        int t = a[i] + 1;  // 计算 t = a[j] + 1
        res += countLeft[t] * countRight[t];

        // 更新 countLeft 和 countRight
        countLeft[a[i]]++;
        countRight[a[i]]--;
    }

    // 输出结果
    cout << res << endl;

    return 0;
}
