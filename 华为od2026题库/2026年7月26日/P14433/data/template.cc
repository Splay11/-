#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    // 解析 JSON 数组 [a,b,c,...]
    vector<int> nums;
    stringstream ss(line);
    int x;
    char ch;
    ss >> ch; // skip '['
    while (ss >> x) {
        nums.push_back(x);
        if (!(ss >> ch) || ch == ']') break;
    }

    Solution solution;
    vector<int> res = solution.sortArrayByParity(nums);

    // 输出 JSON 数组
    cout << "[";
    for (int i = 0; i < (int)res.size(); i++) {
        if (i > 0) cout << ",";
        cout << res[i];
    }
    cout << "]" << endl;
    return 0;
}
