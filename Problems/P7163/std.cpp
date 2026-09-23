#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <utility>
using namespace std;

// 按出现次数从高到低排，次数相同按字符 ASCII；同一字符必须连在一起
string solve(const string& s) {
    int cnt[256] = {0};
    for (int i = 0; i < (int)s.size(); i++) {
        cnt[(unsigned char)s[i]]++;
    }
    vector<pair<int, char> > items;
    for (int c = 0; c < 256; c++) {
        if (cnt[c] > 0) {
            items.push_back(make_pair(-cnt[c], (char)c));
        }
    }
    // first 是次数的相反数，这样 sort 后次数高的在前；second 是字符
    sort(items.begin(), items.end());
    string ans;
    ans.reserve(s.size());
    for (int i = 0; i < (int)items.size(); i++) {
        int times = -items[i].first;
        char ch = items[i].second;
        ans.append(times, ch);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
