#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 从输入字符串中提取所有非负整数
static vector<int> parseNumbers(const string& s) {
    vector<int> nums;
    for (int i = 0; i < (int)s.size(); ) {
        if (s[i] >= '0' && s[i] <= '9') {
            long long val = 0;
            while (i < (int)s.size() && s[i] >= '0' && s[i] <= '9') {
                val = val * 10 + (s[i] - '0');
                i++;
            }
            nums.push_back((int)val);
        } else {
            i++;
        }
    }
    return nums;
}

int main() {
    string line;
    getline(cin, line);
    if (line.empty()) return 0;

    vector<int> nums = parseNumbers(line);
    int playerCount = nums[0];
    vector<vector<int> > playerTimeRange(playerCount, vector<int>(2));

    // 第一个数字是 n，后面每两个数字组成一个区间
    int idx = 1;
    for (int i = 0; i < playerCount; i++) {
        playerTimeRange[i][0] = nums[idx++];
        playerTimeRange[i][1] = nums[idx++];
    }

    Solution solution;
    cout << solution.MaxPlayers(playerCount, playerTimeRange) << endl;
    return 0;
}
