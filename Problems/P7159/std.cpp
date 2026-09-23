#include <iostream>
#include <vector>
using namespace std;

// 正数数组上的滑动窗口：找总和 >= target 的最短连续段
int solve(const vector<int>& nums, int target) {
    int n = (int)nums.size();
    int left = 0;
    long long s = 0;
    int ans = n + 1;
    for (int right = 0; right < n; right++) {
        s += nums[right];
        // 窗口和已经达标，左端能缩就缩，得到更短的合法段
        while (s >= (long long)target) {
            int length = right - left + 1;
            if (length < ans) {
                ans = length;
            }
            s -= nums[left];
            left++;
        }
    }
    // 从未出现合法窗口
    if (ans == n + 1) {
        return 0;
    }
    return ans;
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
