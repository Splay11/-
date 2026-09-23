#include <bits/stdc++.h>
using namespace std;

// 自定义实现的lower_bound函数
// 功能：找到第一个不小于x的位置
int lower_bound_custom(const vector<int>& A, int x) {
    int left = 0, right = A.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (A[mid] < x) {
            left = mid + 1; // x在右半部分
        } else {
            right = mid - 1; // x在左半部分或当前位置
        }
    }
    return left; // 返回第一个不小于x的位置
}

// 自定义实现的upper_bound函数
// 功能：找到第一个大于x的位置
int upper_bound_custom(const vector<int>& A, int x) {
    int left = 0, right = A.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (A[mid] <= x) {
            left = mid + 1; // x在右半部分
        } else {
            right = mid - 1; // x在左半部分
        }
    }
    return left; // 返回第一个大于x的位置
}

int main() {
    int n, C;
    cin >> n; // 输入数组的大小n
    vector<int> A(n);
    for (int i = 0; i < n; ++i) {
        cin >> A[i]; // 输入数组A的元素
    }
    cin >> C; // 输入整数C
    sort(A.begin(), A.end()); // 对数组A进行排序，便于后续的二分查找

    long long sum = 0; // 用于存储满足条件的数对总数

    // 遍历数组中的每个元素
    for(int i = 0; i < A.size(); i++) {
        int x = A[i] + C; // 计算目标值x = A[i] + C
        // 使用自定义的upper_bound和lower_bound查找x的出现次数
        sum += upper_bound_custom(A, x) - lower_bound_custom(A, x);
        // 解释：
        // lower_bound_custom(A, x) 返回第一个不小于x的位置
        // upper_bound_custom(A, x) 返回第一个大于x的位置
        // 两者之差即为x在数组A中出现的次数
    }

    cout << sum; // 输出满足条件的数对总数
    return 0;
}
