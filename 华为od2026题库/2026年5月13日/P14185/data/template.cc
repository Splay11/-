#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string data;
    string line;

    while (getline(cin, line)) {
        if (!data.empty()) {
            data.push_back(' ');
        }
        data += line;
    }

    for (char &ch : data) {
        if (ch == '"' || ch == ',') {
            ch = ' ';
        }
    }

    string inputStr = "";
    int inputDivisor = 0;

    stringstream ss(data);
    ss >> inputStr;
    if (!(ss >> inputDivisor)) {
        inputDivisor = 0;
    }

    Solution solution;
    int result = solution.getMaxDivisibleNumber(inputStr, inputDivisor);
    cout << result << '\n';

    return 0;
}
