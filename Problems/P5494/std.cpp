#include <iostream>
#include <vector>
using namespace std;

// 除数越大，向上取整之和越小；超过阈值就可以提前结束
bool canDivide(const vector<int>& nums, int divisor, int threshold) {
    long long total = 0;
    for (size_t i = 0; i < nums.size(); i++) {
        total += (nums[i] + divisor - 1LL) / divisor;
        if (total > threshold) {
            return false;
        }
    }
    return true;
}

// 答案具有单调性，在 [1, max(nums)] 上二分最小可行除数
int smallestDivisor(const vector<int>& nums, int threshold) {
    int left = 1;
    int right = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        if (nums[i] > right) {
            right = nums[i];
        }
    }
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (canDivide(nums, mid, threshold)) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    return left;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行 n 与阈值，第二行 n 个数
    int n, threshold;
    cin >> n >> threshold;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << smallestDivisor(nums, threshold) << "\n";
    return 0;
}
