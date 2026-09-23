#include <iostream>
#include <vector>
#include <string>
#include <deque>
using namespace std;

#include "foo.cc"

static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int n = (int)s.size();
    int i = 0;
    while (i < n) {
        while (i < n && !(s[i] == '-' || (s[i] >= '0' && s[i] <= '9'))) i++;
        if (i >= n) break;
        int sign = 1;
        if (s[i] == '-') {
            sign = -1;
            i++;
        }
        int x = 0;
        while (i < n && s[i] >= '0' && s[i] <= '9') {
            x = x * 10 + (s[i] - '0');
            i++;
        }
        res.push_back(sign * x);
    }
    return res;
}

static int splitPos(const string& s) {
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '[') bracket++;
        else if (s[i] == ']') bracket--;
        else if (s[i] == ',' && bracket == 0) return i;
    }
    return -1;
}

int main() {
    string line;
    getline(cin, line);

    int p = splitPos(line);
    string aStr = line.substr(0, p);
    string bStr = line.substr(p + 1);

    vector<int> cardA = parseIntList(aStr);
    vector<int> cardB = parseIntList(bStr);

    Solution solution;
    cout << solution.catFishCardGame(cardA, cardB);
    return 0;
}
