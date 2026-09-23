#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;

struct PairHash {
    size_t operator()(const pair<int, int>& p) const {
        return (size_t)p.first * 31u + (size_t)p.second;
    }
};

class Solution {
   public:
    string hasFiveInRow(vector<vector<int>>& blackChessPoses) {
        unordered_set<pair<int, int>, PairHash> s;
        for (auto& p : blackChessPoses) s.insert({p[0], p[1]});
        const int dirs[4][2] = {{1, 0}, {0, 1}, {1, 1}, {1, -1}};
        for (const auto& pt : s) {
            int x = pt.first, y = pt.second;
            for (auto& d : dirs) {
                int dx = d[0], dy = d[1];
                if (s.count({x - dx, y - dy})) continue;
                int cnt = 0, cx = x, cy = y;
                while (s.count({cx, cy})) {
                    if (++cnt >= 5) return "YES";
                    cx += dx;
                    cy += dy;
                }
            }
        }
        return "NO";
    }
};
