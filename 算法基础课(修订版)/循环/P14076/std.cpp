#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    
    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        l--; // 转换为0开始的索引
        r--;
        
        int max_value = arr[l];
        vector<int> max_indices;

        // 找到最大值和下标
        for (int i = l; i <= r; ++i) {
            if (arr[i] > max_value) {
                max_value = arr[i];
                max_indices.clear(); // 清空之前的下标
                max_indices.push_back(i + 1); // 记录当前最大值下标（转为1开始）
            } else if (arr[i] == max_value) {
                max_indices.push_back(i + 1); // 记录当前最大值下标
            }
        }
        
        // 输出结果
        cout << max_value << endl;
        for (size_t i = 0; i < max_indices.size(); ++i) {
            cout << max_indices[i] << (i == max_indices.size() - 1 ? "" : " ");
        }
        cout << endl;
    }
    
    return 0;
}
