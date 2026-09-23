#include <iostream>
#include <vector>

using namespace std;

// 手写二分查找函数
bool binarySearch(const vector<int>& A, int x) {
    int left = 0, right = A.size() - 1;
    
    while (left <= right) {
        int mid = (left + right) / 2; // 防止溢出

        if (A[mid] == x) {
            return true; // 找到元素
        } else if (A[mid] < x) {
            left = mid + 1; // 查找右半部分
        } else {
            right = mid - 1; // 查找左半部分
        }
    }

    return false; // 没有找到元素
}

int main() {
    int n, Q;
    cin >> n >> Q;
    
    vector<int> A(n);
    for (int i = 0; i < n; ++i) {
        cin >> A[i];
    }

    // 对每个查询进行二分查找
    while (Q--) {
        int x;
        cin >> x;
        
        // 使用手写的二分查找函数
        if (binarySearch(A, x)) {
            cout << "YES" << endl;
        } else {
            cout << "NO" << endl;
        }
    }
    
    return 0;
}
