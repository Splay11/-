#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
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

int main() {
    string line;
    getline(cin, line);

    // 解析 R
    int c1 = findTopLevelComma(line);
    int R = stoi(line.substr(0, c1));

    // 解析 G
    string rest1 = line.substr(c1 + 1);
    int c2 = findTopLevelComma(rest1);
    int G = stoi(rest1.substr(0, c2));

    // 剩余部分: [E,S,W,N],[0,1,3,6]
    string rest2 = rest1.substr(c2 + 1);
    int split = rest2.find("],[");
    string dirsStr = rest2.substr(0, split + 1);   // [E,S,W,N]
    string timesStr = rest2.substr(split + 3);       // 0,1,3,6] (跳过 '],[')

    // 解析方向字符列表
    vector<char> directions;
    string cur;
    for (int i = 1; i < (int)dirsStr.size(); i++) {  // 跳过 '['
        char c = dirsStr[i];
        if (c == ',' || c == ']') {
            if (!cur.empty()) {
                directions.push_back(cur[0]);
                cur.clear();
            }
            if (c == ']') break;
        } else {
            cur += c;
        }
    }
    if (!cur.empty()) directions.push_back(cur[0]);

    // 解析到达时间列表
    vector<int> arrivalTimes;
    cur.clear();
    for (int i = 0; i < (int)timesStr.size(); i++) {
        char c = timesStr[i];
        if (c == ',' || c == ']') {
            if (!cur.empty()) {
                arrivalTimes.push_back(stoi(cur));
                cur.clear();
            }
            if (c == ']') break;
        } else {
            cur += c;
        }
    }
    if (!cur.empty()) arrivalTimes.push_back(stoi(cur));

    Solution solution;
    vector<int> result = solution.intersectionWaitingTime(R, G, directions, arrivalTimes);
    cout << "[" << result[0] << "," << result[1] << "]" << endl;
    return 0;
}
