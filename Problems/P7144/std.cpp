#include <iostream>
#include <string>
using namespace std;

bool is_vowel(char c) {
    // 只有 a e i o u，y 不算
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
}

// 扫一遍连续元音段，更长才更新，平局保留先出现的
string solve(const string& s) {
    string best;
    int n = (int)s.size();
    int i = 0;
    while (i < n) {
        if (!is_vowel(s[i])) {
            i++;
            continue;
        }
        int j = i;
        while (j < n && is_vowel(s[j])) {
            j++;
        }
        // 严格更长才换，避免平局取到后面那段
        if (j - i > (int)best.size()) {
            best = s.substr(i, j - i);
        }
        i = j;
    }
    if (best.empty()) {
        return "-1";
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 不含空格，整串就是 s
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
