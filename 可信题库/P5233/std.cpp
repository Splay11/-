#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

class Solution {
   public:
    int countSimilarGroups(vector<string>& uriReqs) {
        int n = (int)uriReqs.size();
        vector<vector<string>> segs(n);
        for (int i = 0; i < n; i++) {
            string s = uriReqs[i].substr(1);
            string cur;
            for (char c : s) {
                if (c == '/') {
                    segs[i].push_back(cur);
                    cur.clear();
                } else
                    cur.push_back(c);
            }
            segs[i].push_back(cur);
        }
        unordered_set<int> remaining;
        for (int i = 0; i < n; i++) remaining.insert(i);
        int groups = 0;
        while (true) {
            unordered_map<string, vector<int>> mp;
            for (int i : remaining) {
                string key;
                for (size_t L = 0; L < segs[i].size(); L++) {
                    if (L) key.push_back('\x1f');
                    key += segs[i][L];
                    mp[key].push_back(i);
                }
            }
            int bestL = 0;
            string bestKey;
            for (auto& e : mp) {
                if ((int)e.second.size() < 2) continue;
                int L = 1;
                for (char c : e.first)
                    if (c == '\x1f') L++;
                if (L > bestL) {
                    bestL = L;
                    bestKey = e.first;
                }
            }
            if (bestL == 0) break;
            for (int i : mp[bestKey]) remaining.erase(i);
            groups++;
        }
        return groups;
    }
};
