#include <string>
#include <vector>

using namespace std;

class Solution {
   public:
    string packFields(vector<int>& sectionWidth, vector<int>& sectionValues) {
        unsigned long long acc = 0;
        int total = 0;
        for (size_t i = 0; i < sectionWidth.size(); i++) {
            int w = sectionWidth[i];
            acc = (acc << w) | (unsigned long long)sectionValues[i];
            total += w;
        }
        int pad = (8 - total % 8) % 8;
        acc <<= pad;
        total += pad;
        int nbytes = total / 8;
        static const char* HEX = "0123456789ABCDEF";
        string ans(nbytes * 2, '0');
        for (int i = nbytes - 1; i >= 0; i--) {
            unsigned char b = (unsigned char)(acc & 0xFF);
            acc >>= 8;
            ans[i * 2] = HEX[b >> 4];
            ans[i * 2 + 1] = HEX[b & 0xF];
        }
        return ans;
    }
};
