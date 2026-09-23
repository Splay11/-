#include <iostream>
#include <vector>
using namespace std;

// Boyer-Moore 投票：抵消不同元素后，剩下的一定是多数元素（题目保证存在）
int majorityElement(const vector<int>& nums) {
    int cand = 0;
    int cnt = 0;
    for (int x : nums) {
        // 当前没有候选人，把这个数立为候选人
        if (cnt == 0) {
            cand = x;
            cnt = 1;
        } else if (x == cand) {
            // 碰到候选人，票数加一
            cnt++;
        } else {
            // 碰到其他数，互相抵消一票
            cnt--;
        }
    }
    // 题目保证多数元素一定存在，抵消结束后候选人就是答案
    return cand;
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
    cout << majorityElement(nums) << '\n';
    return 0;
}
