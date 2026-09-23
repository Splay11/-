#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m; // n: 左边物品数量, m: 右边物品数量
    cin >> n >> m; // 输入物品数量

    vector<int> leftWeights(n); // 存储左边物品的重量
    vector<int> rightWeights(m); // 存储右边物品的重量

    // 输入左边物品的重量
    for (int i = 0; i < n; ++i) {
        cin >> leftWeights[i];
    }

    // 输入右边物品的重量
    for (int i = 0; i < m; ++i) {
        cin >> rightWeights[i];
    }

    // 计算左边总重量
    int leftTotal = 0;
    for (int weight : leftWeights) {
        leftTotal += weight;
    }

    // 计算右边总重量
    int rightTotal = 0;
    for (int weight : rightWeights) {
        rightTotal += weight;
    }

    // 比较两个天平的总重量并输出结果
    if (leftTotal == rightTotal) {
        cout << "Equal" << endl;
    } else {
        cout << "Not Equal" << endl;
    }

    return 0;
}
