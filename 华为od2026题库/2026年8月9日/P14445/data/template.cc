#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

static vector<int> parseIntArray(const string& s) {
    vector<int> res;
    int num = 0;
    bool hasNum = false;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            hasNum = true;
        } else if (hasNum) {
            res.push_back(num);
            num = 0;
            hasNum = false;
        }
    }
    if (hasNum) res.push_back(num);
    return res;
}

int main() {
    string line;
    getline(cin, line);

    int firstComma = line.find(',');
    int priceRecords = stoi(line.substr(0, firstComma));

    string rest = line.substr(firstComma + 1);
    int secondComma = rest.find(',');
    int hours = stoi(rest.substr(0, secondComma));

    string arrStr = rest.substr(secondComma + 1);
    vector<int> priceArray = parseIntArray(arrStr);

    Solution solution;
    cout << solution.findBestChargingTime(priceRecords, hours, priceArray) << endl;
    return 0;
}
