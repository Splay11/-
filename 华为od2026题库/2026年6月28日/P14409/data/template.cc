#include "foo.cc"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

static vector<int> parseIntList(const string& s) {
    vector<int> res;
    size_t i = 0;
    while (i < s.size() && (s[i] == ' ' || s[i] == '\t')) ++i;
    if (i >= s.size() || s[i] != '[') return res;
    ++i;
    while (i < s.size()) {
        while (i < s.size() && (s[i] == ' ' || s[i] == '\t' || s[i] == ',')) {
            if (s[i] == ']') return res;
            ++i;
        }
        if (i >= s.size() || s[i] == ']') break;
        size_t j = i;
        while (j < s.size() && (isdigit(static_cast<unsigned char>(s[j])) || s[j] == '-')) ++j;
        res.push_back(stoi(s.substr(i, j - i)));
        i = j;
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);
    size_t comma = line.find(',');
    if (comma == string::npos) return 1;
    int n = stoi(line.substr(0, comma));
    vector<int> nums = parseIntList(line.substr(comma + 1));
    if (static_cast<int>(nums.size()) != n) return 1;
    Solution solution;
    cout << solution.minSplitRangeSum(nums) << endl;
    return 0;
}
