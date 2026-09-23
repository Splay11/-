#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

static vector<int> extractNumbers(const string& s) {
    vector<int> nums;
    int n = (int)s.size();
    for (int i = 0; i < n; i++) {
        if (isdigit((unsigned char)s[i])) {
            int x = 0;
            while (i < n && isdigit((unsigned char)s[i])) {
                x = x * 10 + (s[i] - '0');
                i++;
            }
            nums.push_back(x);
        }
    }
    return nums;
}

int main() {
    string line, all;
    while (getline(cin, line)) {
        if (!all.empty()) all += " ";
        all += line;
    }

    vector<int> nums = extractNumbers(all);
    int N = nums[0];
    int T = nums[1];

    int m = ((int)nums.size() - 2) / 2;
    vector<int> accuracy, latency;
    for (int i = 0; i < m; i++) accuracy.push_back(nums[2 + i]);
    for (int i = 0; i < m; i++) latency.push_back(nums[2 + m + i]);

    Solution solution;
    cout << solution.maxTotalAccuracy(N, T, accuracy, latency);
    return 0;
}
