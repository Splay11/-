#include <string>

using namespace std;

class Solution {
 public:
  int countOpenSyllables(string s) {
    auto isVowel = [](char ch) {
      return ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u';
    };
    auto isConsonant = [&](char ch) {
      return ch >= 'a' && ch <= 'z' && !isVowel(ch);
    };

    string text;
    string word;
    bool first = true;
    auto flush = [&]() {
      if (!first) text.push_back(' ');
      first = false;
      bool pure = !word.empty();
      for (char ch : word) {
        if (ch < 'a' || ch > 'z') {
          pure = false;
          break;
        }
      }
      if (pure) {
        for (int i = (int)word.size() - 1; i >= 0; --i) text.push_back(word[i]);
      } else {
        text += word;
      }
      word.clear();
    };

    for (char ch : s) {
      if (ch == ' ')
        flush();
      else
        word.push_back(ch);
    }
    flush();

    int ans = 0;
    for (int i = 0; i + 3 < (int)text.size(); ++i) {
      char a = text[i], b = text[i + 1], c = text[i + 2], d = text[i + 3];
      if (isConsonant(a) && isVowel(b) && isConsonant(c) && c != 'r' && d == 'e') ans++;
    }
    return ans;
  }
};
