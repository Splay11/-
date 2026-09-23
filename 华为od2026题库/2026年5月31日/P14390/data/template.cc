#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <deque>
#include <climits>
using namespace std;

static int findTopLevelComma(const string& s) {
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '[') bracket++;
        else if (c == ']') bracket--;
        else if (c == ',' && bracket == 0) return i;
    }
    return -1;
}

static vector<int> parseIntArray(const string& s) {
    vector<int> nums;
    int i = 0;
    while (i < (int)s.size()) {
        while (i < (int)s.size() && !(s[i] == '-' || (s[i] >= '0' && s[i] <= '9'))) i++;
        if (i >= (int)s.size()) break;

        int sign = 1;
        if (s[i] == '-') {
            sign = -1;
            i++;
        }

        int val = 0;
        while (i < (int)s.size() && s[i] >= '0' && s[i] <= '9') {
            val = val * 10 + (s[i] - '0');
            i++;
        }

        nums.push_back(sign * val);
    }
    return nums;
}

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    vector<int> nums = parseIntArray(line.substr(0, comma));
    int k = atoi(line.substr(comma + 1).c_str());

    Solution solution;
    cout << solution.maxEnergyDivisibleByK(nums, (int)nums.size(), k) << endl;
    return 0;
}
