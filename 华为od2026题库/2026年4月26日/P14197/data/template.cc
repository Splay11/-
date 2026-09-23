#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

static vector<int> parseIntArray(const string& s) {
    vector<int> res;
    int num = 0;
    int sign = 1;
    bool inNum = false;

    for (char c : s) {
        if (c == '-') {
            sign = -1;
            inNum = true;
            num = 0;
        } else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                res.push_back(sign * num);
                num = 0;
                sign = 1;
                inNum = false;
            }
        }
    }
    if (inNum) res.push_back(sign * num);
    return res;
}

static void printIntArray(const vector<int>& arr) {
    cout << "[";
    for (int i = 0; i < (int)arr.size(); i++) {
        if (i > 0) cout << ",";
        cout << arr[i];
    }
    cout << "]" << endl;
}

int main() {
    string line;
    getline(cin, line);

    vector<int> portRates = parseIntArray(line);
    Solution solution;
    vector<int> ans = solution.StatPortRates(portRates);
    printIntArray(ans);
    return 0;
}
