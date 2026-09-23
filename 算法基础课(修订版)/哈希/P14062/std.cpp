#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

int count_pairs(int n, const vector<int>& p) {
    unordered_map<int, int> diff_count;  // 哈希表，记录 p_i - i 出现的次数
    int result = 0;

    for (int j = 0; j < n; ++j) {
        int diff = (j + 1) - p[j];  // 计算 j - p_j
        if (diff_count.find(-diff) != diff_count.end()) {  // 如果 -diff 已经出现过
            result += diff_count[-diff];  // 找到符合条件的 i
        }
        
        // 更新 diff_count
        diff_count[diff]++;
    }

    return result;
}

int main() {
    int n;
    cin >> n;  // 输入数组的大小 n
    vector<int> p(n);  // 创建数组 p

    // 输入数组 p 的元素
    for (int i = 0; i < n; ++i) {
        cin >> p[i];
    }

    // 调用函数并输出结果
    cout << count_pairs(n, p) << endl;

    return 0;
}
