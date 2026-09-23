#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

// 每个值的出现次数必须能被 k 整除
bool solve(const vector<int>& nums, int k) {
    unordered_map<int, int> cnt;
    for (int i = 0; i < (int)nums.size(); i++) {
        cnt[nums[i]]++;
    }
    for (unordered_map<int, int>::iterator it = cnt.begin(); it != cnt.end(); ++it) {
        if (it->second % k != 0) {
            return false;
        }
    }
    return true;
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
    cout << (solve(nums, k) ? "true" : "false") << '\n';
    return 0;
}
