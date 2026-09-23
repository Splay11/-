#include <iostream>
#include <vector>
using namespace std;

// 在严格升序数组里二分查找 target，找到返回下标，否则 -1
int solve(const vector<int>& nums, int target) {
    int left = 0;
    int right = (int)nums.size() - 1;
    while (left <= right) {
        // 用 left+(right-left)/2，避免 left+right 溢出
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        }
        if (nums[mid] < target) {
            // 中点比目标小，答案只可能在右半段
            left = mid + 1;
        } else {
            // 中点比目标大，答案只可能在左半段
            right = mid - 1;
        }
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << solve(nums, target) << '\n';
    return 0;
}
