#include <algorithm>
#include <cctype>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
   public:
    static string normalize(const string& story) {
        size_t a = 0, b = story.size();
        while (a < b && story[a] == ' ') a++;
        while (b > a && story[b - 1] == ' ') b--;
        string s = story.substr(a, b - a);
        if (s.empty()) return "";
        string out;
        out.reserve(s.size());
        for (size_t i = 0; i < s.size();) {
            if (s[i] == ' ') {
                if (!out.empty()) out.push_back(' ');
                while (i < s.size() && s[i] == ' ') i++;
            } else {
                out.push_back(s[i++]);
            }
        }
        while (!out.empty() && out.back() == ' ') out.pop_back();
        return out;
    }

    int lengthOfLongestSubstring(string story) {
        string t = normalize(story);
        if (t.empty()) return 0;
        unordered_map<char, int> last;
        int left = 0, best = 0;
        for (int right = 0; right < (int)t.size(); right++) {
            char key = (char)tolower((unsigned char)t[right]);
            auto it = last.find(key);
            if (it != last.end() && it->second >= left) left = it->second + 1;
            last[key] = right;
            best = max(best, right - left + 1);
        }
        return best;
    }
};
