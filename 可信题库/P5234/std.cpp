#include <algorithm>
#include <cctype>
#include <string>

using namespace std;

class Solution {
   public:
    string sortLetter(string lettersStr) {
        sort(lettersStr.begin(), lettersStr.end());
        string out;
        out.reserve(lettersStr.size());
        for (char c : lettersStr) {
            int pos = tolower((unsigned char)c) - 'a' + 1;
            int np = (pos * pos) % 26 + 1;
            char ch = char('A' + np - 1);
            out.push_back(isupper((unsigned char)c) ? (char)tolower(ch)
                                                    : (char)toupper(ch));
        }
        return out;
    }
};
