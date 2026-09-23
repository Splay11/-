#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> countKeys(string s) {
        unordered_map<char, int> cnt;
        int i = 0, n = s.size();

        while (i < n) {
            if (i + 1 < n && s[i] == 'u' && s[i + 1] == 'u') {
                cnt['j']++;
                i += 2;
            } else if (i + 1 < n && s[i] == 't' && s[i + 1] == 't') {
                cnt['b']++;
                i += 2;
            } else {
                cnt[s[i]]++;
                i++;
            }
        }

        vector<pair<char, int>> arr;
        for (auto &p : cnt) arr.push_back(p);

        sort(arr.begin(), arr.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
            if (a.second != b.second) return a.second > b.second;
            return a.first < b.first;
        });

        vector<vector<int>> ans;
        for (auto &p : arr) {
            ans.push_back({encode(p.first), p.second});
        }
        return ans;
    }

private:
    int encode(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        return c - 'a' + 10;
    }
};
