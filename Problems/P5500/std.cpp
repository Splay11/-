#include <bits/stdc++.h>
using namespace std;

// 从后往前双指针合并，避免覆盖 nums1 前部有效元素
void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (i >= 0 && j >= 0) {
        if (nums1[i] >= nums2[j]) {
            nums1[k--] = nums1[i--];
        } else {
            nums1[k--] = nums2[j--];
        }
    }
    while (j >= 0) {
        nums1[k--] = nums2[j--];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<int> nums1(m + n);
    for (int i = 0; i < m + n; ++i) {
        cin >> nums1[i];
    }
    vector<int> nums2(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums2[i];
    }
    merge(nums1, m, nums2, n);
    for (int i = 0; i < m + n; ++i) {
        if (i) {
            cout << ' ';
        }
        cout << nums1[i];
    }
    cout << "\n";
    return 0;
}
