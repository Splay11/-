#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;

    // 顶层逗号分隔 n 与乘客列表
    int comma = (int)line.find(',');
    int n = stoi(line.substr(0, comma));

    string rest = line.substr(comma + 1);

    // 提取所有整数并按顺序两两配对为 [起点,终点]
    vector<int> nums;
    int num = 0;
    bool have = false;
    for (char c : rest) {
        if (isdigit((unsigned char)c)) {
            num = num * 10 + (c - '0');
            have = true;
        } else if (have) {
            nums.push_back(num);
            num = 0;
            have = false;
        }
    }
    if (have) nums.push_back(num);

    vector<vector<int>> passengers;
    for (size_t i = 0; i + 1 < nums.size(); i += 2) {
        passengers.push_back({nums[i], nums[i + 1]});
    }

    Solution solution;
    cout << solution.maxRideProfit(n, passengers) << endl;
    return 0;
}
