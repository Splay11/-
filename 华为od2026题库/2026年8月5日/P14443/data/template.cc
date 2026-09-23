#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

static int findTopLevelComma(const string& s) {
    bool inString = false;
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '"') {
            inString = !inString;
        } else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    int n = stoi(line.substr(0, comma));

    // 提取引号内的字符串：跳过逗号和开头引号
    string rest = line.substr(comma + 1);
    int startQuote = rest.find('"');
    int endQuote = rest.rfind('"');
    string channels = rest.substr(startQuote + 1, endQuote - startQuote - 1);

    Solution solution;
    cout << solution.mergeBroadcastChannels(n, channels) << endl;
    return 0;
}
