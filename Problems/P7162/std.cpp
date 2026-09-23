#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

// 元素互不相同且不为 0。只从正数这边数，避免一对算两次
int solve(const vector<int>& nums) {
    unordered_set<int> s;
    for (int i = 0; i < (int)nums.size(); i++) {
        s.insert(nums[i]);
    }
    int ans = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (nums[i] > 0 && s.count(-nums[i])) {
            ans++;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << solve(nums) << '\n';
    return 0;
}
