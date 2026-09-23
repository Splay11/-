#include <iostream>
#include <vector>
using namespace std;

// 在全是正整数的数组里，找总和 >= target 的最短连续段长度；没有则返回 0
int minSubarrayLen(const vector<int>& nums, long long target) {
    int n = (int)nums.size();
    long long s = 0;
    int left = 0;
    // 用 n+1 当「还没找到」的哨兵，保证任何合法长度都会把它更新掉
    int ans = n + 1;
    for (int right = 0; right < n; right++) {
        // 右端点纳入窗口
        s += nums[right];
        // 元素都是正的，窗口和只会随左端点右移而变小，可以一直收缩
        while (s >= target) {
            int length = right - left + 1;
            if (length < ans) {
                ans = length;
            }
            s -= nums[left];
            left++;
        }
    }
    // 从头到尾都凑不够 target，就没有合法子数组
    if (ans == n + 1) {
        return 0;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << minSubarrayLen(nums, target) << '\n';
    return 0;
}
