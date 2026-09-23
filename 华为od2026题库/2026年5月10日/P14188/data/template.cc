#include<bits/stdc++.h>
using namespace std;
#include "foo.cc"
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string text, line;
    while (getline(cin, line)) {
        text += line;
    }

    for (char &ch : text) {
        if (ch == '[' || ch == ']' || ch == ',') {
            ch = ' ';
        }
    }

    stringstream ss(text);
    vector<int> nums;
    int x;
    while (ss >> x) {
        nums.push_back(x);
    }

    Solution solution;
    vector<int> ans = solution.longestBeautifulLanterns(nums);

    cout << "[" << ans[0] << "," << ans[1] << "]\n";
    return 0;
}