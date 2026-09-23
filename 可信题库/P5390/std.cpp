#include <string>
using namespace std;

class Solution {
public:
    string reviseMarks(string s) {
        int i0 = -1, i1 = -1;
        int n = (int)s.size();
        for (int i = 0; i < n; i++) {
            if (s[i] == '0' && i0 < 0) i0 = i;
            if (s[i] == '1' && i1 < 0) i1 = i;
            if (i0 >= 0 && i1 >= 0) break;
        }
        string ans;
        ans.reserve(n);
        for (int i = 0; i < n; i++) {
            if (i != i0 && i != i1) ans.push_back(s[i]);
        }
        return ans;
    }
};
