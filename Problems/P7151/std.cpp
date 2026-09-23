#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

// 次数从大到小；次数相同则字典序从小到大
bool cmp(const pair<string, int>& a, const pair<string, int>& b) {
    if (a.second != b.second) {
        return a.second > b.second;
    }
    return a.first < b.first;
}

vector<string> solve(const vector<string>& words, int k) {
    map<string, int> cnt;
    for (int i = 0; i < (int)words.size(); i++) {
        cnt[words[i]]++;
    }
    vector<pair<string, int> > items;
    for (map<string, int>::iterator it = cnt.begin(); it != cnt.end(); ++it) {
        items.push_back(make_pair(it->first, it->second));
    }
    sort(items.begin(), items.end(), cmp);
    vector<string> ans;
    for (int i = 0; i < k; i++) {
        ans.push_back(items[i].first);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<string> words(n);
    for (int i = 0; i < n; i++) {
        cin >> words[i];
    }
    vector<string> ans = solve(words, k);
    for (int i = 0; i < k; i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
