#include <iostream>
#include <vector>
using namespace std;

// 截图中的双指针：和等于 k 则左右都移动，和偏小则左移，和偏大则右移
int twoSum2(const vector<int>& nums, int k) {
    int left = 0;
    int right = (int)nums.size() - 1;
    int count = 0;
    // 数组有序且无重复，左右夹逼统计和为 k 的数对
    while (left < right) {
        long long current_sum = (long long)nums[left] + nums[right];
        if (current_sum == k) {
            // 找到一对，两侧都收一格；无重复所以不会再配同一对数
            count += 1;
            left += 1;
            right -= 1;
        } else if (current_sum < k) {
            // 当前和偏小，左端右移让 nums[left] 变大
            left += 1;
        } else {
            // 当前和偏大，右端左移让 nums[right] 变小
            right -= 1;
        }
    }
    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << twoSum2(nums, k) << "\n";
    return 0;
}
