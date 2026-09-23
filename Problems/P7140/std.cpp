#include <iostream>
#include <string>
using namespace std;

bool isDigits(const string& s, int l, int r) {
    // [l, r) 是否全是数字且非空
    if (l >= r) {
        return false;
    }
    for (int i = l; i < r; i++) {
        if (s[i] < '0' || s[i] > '9') {
            return false;
        }
    }
    return true;
}

// 整数：可选正负号，后面至少一位数字
bool isInteger(const string& s) {
    if (s.empty()) {
        return false;
    }
    int i = 0;
    if (s[0] == '+' || s[0] == '-') {
        i = 1;
    }
    return isDigits(s, i, (int)s.size());
}

// 小数：可选正负号，后面是 digits. / digits.digits / .digits
bool isDecimal(const string& s) {
    if (s.empty()) {
        return false;
    }
    int i = 0;
    if (s[0] == '+' || s[0] == '-') {
        i = 1;
    }
    int dot = -1;
    for (int j = i; j < (int)s.size(); j++) {
        if (s[j] == '.') {
            if (dot != -1) {
                return false;
            }
            dot = j;
        }
    }
    if (dot == -1) {
        return false;
    }
    bool left = isDigits(s, i, dot);
    bool right = isDigits(s, dot + 1, (int)s.size());
    // 小数点两侧不能都没有数字
    return left || right;
}

// 有效数字 =（整数或小数）后面可以跟一个指数 e/E + 整数
bool valid(const string& s) {
    int epos = -1;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == 'e' || s[i] == 'E') {
            if (epos != -1) {
                return false;
            }
            epos = i;
        }
    }
    if (epos == -1) {
        return isInteger(s) || isDecimal(s);
    }
    string left = s.substr(0, epos);
    string right = s.substr(epos + 1);
    if (left.empty() || right.empty()) {
        return false;
    }
    return (isInteger(left) || isDecimal(left)) && isInteger(right);
}

string solve(const string& s) {
    return valid(s) ? "true" : "false";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
