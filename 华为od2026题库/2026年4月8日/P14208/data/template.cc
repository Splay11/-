#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

using namespace std;

#include "foo.cc"

int main() {
    string line;
    if (!getline(cin, line)) return 0;

    // 预处理：将复杂格式字符替换为空格
    for (char &c : line) {
        if (c == '[' || c == ']' || c == ',' || c == '\"') {
            c = ' ';
        }
    }

    stringstream ss(line);
    int month;
    ss >> month;

    vector<string> allTokens;
    string temp;
    while (ss >> temp) {
        allTokens.push_back(temp);
    }

    int n = allTokens.size() / 2;
    vector<string> employees, birthdays;
    for (int i = 0; i < n; i++) employees.push_back(allTokens[i]);
    for (int i = 0; i < n; i++) birthdays.push_back(allTokens[n + i]);

    Solution solution;
    cout << solution.countBirthdayGifts(month, employees, birthdays);

    return 0;
}
