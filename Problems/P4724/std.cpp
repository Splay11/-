#include <algorithm>
#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    vector<string> findMaxOccupiedPaths(string target, vector<string>& files, vector<int>& sizes) {
        bool exists = false;
        for (const string& p : files) {
            if (p == target || (p.size() > target.size() && p.compare(0, target.size(), target) == 0 && p[target.size()] == '/')) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            return {};
        }
        unordered_map<string, int64_t> agg;
        const string pref = target + "/";
        for (size_t i = 0; i < files.size(); ++i) {
            const string& p = files[i];
            if (p == target) {
                continue;
            }
            if (p.size() <= target.size() || p.compare(0, target.size(), target) != 0 || p[target.size()] != '/') {
                continue;
            }
            string rel = p.substr(target.size() + 1);
            size_t slash = rel.find('/');
            string child;
            if (slash == string::npos) {
                child = p;
            } else {
                child = target + "/" + rel.substr(0, slash);
            }
            agg[child] += static_cast<int64_t>(sizes[i]);
        }
        if (agg.empty()) {
            return {};
        }
        int64_t mx = 0;
        for (const auto& kv : agg) {
            mx = max(mx, kv.second);
        }
        vector<string> ans;
        for (const auto& kv : agg) {
            if (kv.second == mx) {
                ans.push_back(kv.first);
            }
        }
        sort(ans.begin(), ans.end());
        return ans;
    }
};
