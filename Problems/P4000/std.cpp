#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    int countBirthdayGifts(int month, vector<string>& employees, vector<string>& birthdays) {
        int ans = 0;
        for (const string& s : birthdays) {
            int m = stoi(s.substr(0, s.find('-')));
            if (m == month) {
                ++ans;
            }
        }
        return ans;
    }
};
