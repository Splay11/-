#include <iostream>
#include <string>
#include <vector>
using namespace std;

// 每个字母取在所有串中出现次数的最小值，再按字典序展开
vector<char> solve(const vector<string>& words) {
    int min_cnt[26];
    for (int i = 0; i < 26; i++) {
        min_cnt[i] = 1000000000;
    }
    for (int t = 0; t < (int)words.size(); t++) {
        int cnt[26] = {0};
        const string& w = words[t];
        for (int i = 0; i < (int)w.size(); i++) {
            cnt[w[i] - 'a']++;
        }
        for (int i = 0; i < 26; i++) {
            if (cnt[i] < min_cnt[i]) {
                min_cnt[i] = cnt[i];
            }
        }
    }
    vector<char> chars;
    for (int i = 0; i < 26; i++) {
        // 按 a..z 顺序重复输出 min 次
        for (int k = 0; k < min_cnt[i]; k++) {
            chars.push_back(char('a' + i));
        }
    }
    return chars;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> words(n);
    for (int i = 0; i < n; i++) {
        cin >> words[i];
    }
    vector<char> chars = solve(words);
    cout << (int)chars.size() << '\n';
    // 没有公共字符时只输出 0，不再打第二行
    if (!chars.empty()) {
        for (int i = 0; i < (int)chars.size(); i++) {
            if (i) {
                cout << ' ';
            }
            cout << chars[i];
        }
        cout << '\n';
    }
    return 0;
}
