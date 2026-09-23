#include <iostream>
#include <string>
#include <vector>
using namespace std;

int distinctCount(const string& s) {
    vector<int> seen(26, 0);
    int tot = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        int idx = s[i] - 'a';
        if (!seen[idx]) {
            seen[idx] = 1;
            tot++;
        }
    }
    return tot;
}

bool canSplit(const string& s, int m, int limit) {
    // 每段不同字母不超过 limit 时，最少要拆成几段；能拆得更碎就不会更差
    int n = (int)s.size();
    int pieces = 0;
    int i = 0;
    while (i < n) {
        pieces++;
        if (pieces > m) {
            return false;
        }
        vector<int> cnt(26, 0);
        int kinds = 0;
        int j = i;
        // 从 i 尽量往右延伸，直到再加一个字母会超过上限
        while (j < n) {
            int idx = s[j] - 'a';
            if (cnt[idx] == 0) {
                if (kinds == limit) {
                    break;
                }
                kinds++;
            }
            cnt[idx]++;
            j++;
        }
        if (j == i) {
            return false;
        }
        i = j;
    }
    return true;
}

int minInterference(const string& s, int m) {
    // 干扰度越大越容易拆进 m 段，二分最小可行上限
    int left = 1;
    int right = distinctCount(s);
    while (left < right) {
        int mid = (left + right) / 2;
        if (canSplit(s, m, mid)) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    return left;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行 n、m，第二行报文
    int n, m;
    cin >> n >> m;
    string s;
    cin >> s;
    if ((int)s.size() > n) {
        s = s.substr(0, n);
    }
    cout << minInterference(s, m) << "\n";
    return 0;
}
