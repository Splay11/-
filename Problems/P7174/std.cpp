#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <utility>
using namespace std;

// 哈希表存前缀到银行；每个卡号从长到短试前缀，第一次命中即最长匹配
vector<string> solve(const vector<pair<string, string>>& prefixes,
                     const vector<string>& cards) {
    unordered_map<string, string> mp;
    mp.reserve(prefixes.size() * 2 + 1);
    for (int i = 0; i < (int)prefixes.size(); i++) {
        mp[prefixes[i].first] = prefixes[i].second;
    }
    vector<string> answers;
    answers.reserve(cards.size());
    for (int i = 0; i < (int)cards.size(); i++) {
        const string& card = cards[i];
        string ans = "UNKNOWN";
        int upper = (int)card.size();
        if (upper > 20) {
            upper = 20;
        }
        // 从长到短，保证取到最长前缀，而不是输入顺序里的第一条
        for (int L = upper; L >= 1; L--) {
            string pref = card.substr(0, L);
            unordered_map<string, string>::iterator it = mp.find(pref);
            if (it != mp.end()) {
                ans = it->second;
                break;
            }
        }
        answers.push_back(ans);
    }
    return answers;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<string, string>> prefixes(n);
    for (int i = 0; i < n; i++) {
        cin >> prefixes[i].first >> prefixes[i].second;
    }
    int m;
    cin >> m;
    vector<string> cards(m);
    for (int i = 0; i < m; i++) {
        cin >> cards[i];
    }
    vector<string> answers = solve(prefixes, cards);
    for (int i = 0; i < (int)answers.size(); i++) {
        cout << answers[i] << '\n';
    }
    return 0;
}
