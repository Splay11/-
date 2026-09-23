#include <iostream>
#include <unordered_set>
using namespace std;

int main() {
    int n;
    cin >> n; // 读取序列长度
    int a[n];
    
    // 读取序列
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    unordered_set<int> seen; // 用于记录窗口中的元素
    int left = 0; // 左指针
    int maxLength = 0; // 最长无重复子数组的长度

    // 遍历数组
    for (int right = 0; right < n; right++) {
        // 如果当前元素在窗口中已经存在，收缩窗口
        while (seen.count(a[right])) {
            seen.erase(a[left]);
            left++;
        }

        // 加入当前元素
        seen.insert(a[right]);
        
        // 更新最大长度
        maxLength = max(maxLength, right - left + 1);
    }

    // 输出结果
    cout << maxLength << endl;

    return 0;
}
