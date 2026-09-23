#include <algorithm>
#include <cctype>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

static string toLower(const string& s) {
  string t = s;
  for (char& c : t) c = static_cast<char>(tolower(static_cast<unsigned char>(c)));
  return t;
}

static bool isDelim(char c) {
  return isspace(static_cast<unsigned char>(c)) || c == ',' || c == '.' ||
         c == '!' || c == '?' || c == ';' || c == ':';
}

static vector<string> tokenize(const string& log) {
  vector<string> words;
  string cur;
  for (char c : log) {
    if (isDelim(c)) {
      if (!cur.empty()) {
        words.push_back(toLower(cur));
        cur.clear();
      }
    } else {
      cur += c;
    }
  }
  if (!cur.empty()) words.push_back(toLower(cur));
  return words;
}

class Solution {
 public:
  vector<int> analyzeLogKeywords(vector<string>& logs, vector<string>& keywords) {
    int m = static_cast<int>(keywords.size());
    vector<string> kws;
    kws.reserve(m);
    for (auto& k : keywords) kws.push_back(toLower(k));
    vector<vector<string>> tokenized;
    tokenized.reserve(logs.size());
    for (auto& log : logs) tokenized.push_back(tokenize(log));
    vector<int> counts(m, 0);
    for (auto& words : tokenized) {
      for (int ki = 0; ki < m; ki++) {
        for (auto& w : words) {
          if (w == kws[ki]) counts[ki]++;
        }
      }
    }
    vector<vector<bool>> present;
    present.reserve(tokenized.size());
    for (auto& words : tokenized) {
      unordered_set<string> wordSet(words.begin(), words.end());
      vector<bool> row(m, false);
      for (int ki = 0; ki < m; ki++) {
        row[ki] = wordSet.count(kws[ki]) > 0;
      }
      present.push_back(std::move(row));
    }
    vector<int> pairs;
    for (int i = 0; i < m; i++) {
      for (int j = i + 1; j < m; j++) {
        int co = 0;
        for (auto& row : present) {
          if (row[i] && row[j]) co++;
        }
        if (co >= 2) {
          pairs.push_back(i);
          pairs.push_back(j);
        }
      }
    }
    counts.insert(counts.end(), pairs.begin(), pairs.end());
    return counts;
  }
};
