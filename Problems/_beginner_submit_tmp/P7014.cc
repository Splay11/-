#include <vector>
using namespace std;

class Solution {
public:
    int bestRelay(vector<vector<int>>& relays, int budget) {
        int best_id = -1;
        int best_lat = 0;
        bool found = false;
        for (auto& r : relays) {
            int rid = r[0], lat = r[1], price = r[2];
            if (price > budget) {
                continue;
            }
            // 更低时延优先；时延相同取更小编号
            if (!found || lat < best_lat || (lat == best_lat && rid < best_id)) {
                best_id = rid;
                best_lat = lat;
                found = true;
            }
        }
        return best_id;
    }
};
