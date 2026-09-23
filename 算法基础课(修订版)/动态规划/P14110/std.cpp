#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;  // 输入序列的长度
    vector<int> a(n), dp(n, 1);  // a数组存储序列，dp数组存储以每个元素为结尾的最长上升子序列的长度，初始化为1

    // 读取输入的序列
    for (int i = 0; i < n; i++) {
        cin >> a[i];  // 逐个输入序列中的元素
    }

    // 动态规划部分
    // dp[i] 表示以 a[i] 为结尾的最长上升子序列的长度
    for (int i = 1; i < n; i++) {  // 遍历每一个元素，计算以当前元素为结尾的最长上升子序列
        for (int j = 0; j < i; j++) {  // 遍历当前元素之前的所有元素
            if (a[i] > a[j]) {  // 如果当前元素 a[i] 大于前面元素 a[j]
                dp[i] = max(dp[i], dp[j] + 1);  // 更新 dp[i]，选择增加当前元素的最长子序列长度
            }
        }
    }

    // 输出最长上升子序列的长度
    cout << *max_element(dp.begin(), dp.end()) << endl;  // 输出 dp 数组中的最大值，表示最长上升子序列的长度

    return 0; 
}
