#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>
using namespace std;

// 扫描空格与字母段，累加单词长度并计数
string solve(const string& s) {
    long long total = 0;
    int cnt = 0;
    int n = (int)s.size();
    int i = 0;
    while (i < n) {
        // 跳过一个或多个空格
        while (i < n && s[i] == ' ') {
            i++;
        }
        if (i >= n) {
            break;
        }
        int j = i;
        // 连续字母构成一个单词
        while (j < n && s[j] != ' ') {
            j++;
        }
        total += (j - i);
        cnt++;
        i = j;
    }
    // 用固定两位小数格式化，避免输出 3.7 或缺前导
    ostringstream oss;
    oss << fixed << setprecision(2) << (double)total / cnt;
    return oss.str();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 句子含空格，必须整行读入，不能用 cin >>
    string s;
    getline(cin, s);
    cout << solve(s) << '\n';
    return 0;
}
