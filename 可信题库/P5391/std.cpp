#include <vector>
using namespace std;

class Solution {
public:
    bool canPassBooks(vector<int>& desks) {
        long long s = 0;
        for (int i = 0; i < (int)desks.size(); i++) {
            s += desks[i];
            long long k = i + 1;
            if (s < k * (k + 1) / 2) return false;
        }
        return true;
    }
};
