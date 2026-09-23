#include <cmath>
#include <string>
#include <vector>

using namespace std;

class Solution {
  static double weighted(long long amount, long long start, long long end, long long qs, long long qe) {
    if (start > qe || end < qs) return 0.0;
    long long duration = end - start;
    if (duration == 0) {
      if (qs <= start && start <= qe) return (double)amount;
      return 0.0;
    }
    long long os = max(start, qs);
    long long oe = min(end, qe);
    if (os > oe) return 0.0;
    long long overlap = oe - os;
    return (double)amount * (double)overlap / (double)duration;
  }

  static int roundToI32(double x) {
    long long val;
    if (x >= 0)
      val = (long long)floor(x + 0.5);
    else
      val = (long long)ceil(x - 0.5);
    if (val > 2147483647LL) return 2147483647;
    if (val < -2147483648LL) return -2147483648;
    return (int)val;
  }

 public:
  int queryNetEnergy(vector<string>& commands) {
    const string& query = commands.back();
    vector<string> qparts;
    size_t start = 0;
    for (size_t i = 0; i <= query.size(); i++) {
      if (i == query.size() || query[i] == ',') {
        qparts.push_back(query.substr(start, i - start));
        start = i + 1;
      }
    }
    string versionStr = qparts[1];
    long long qs = stoll(qparts[2]);
    long long qe = stoll(qparts[3]);
    bool useAll = (versionStr == "A");
    int maxVersion = useAll ? 1000000000 : stoi(versionStr);

    double total = 0.0;
    int version = 0;
    for (size_t i = 0; i + 1 < commands.size(); i++) {
      version++;
      if (version > maxVersion) break;
      const string& cmd = commands[i];
      vector<string> parts;
      start = 0;
      for (size_t j = 0; j <= cmd.size(); j++) {
        if (j == cmd.size() || cmd[j] == ',') {
          parts.push_back(cmd.substr(start, j - start));
          start = j + 1;
        }
      }
      if (parts[0] == "AddProductionRecord") {
        long long amount = stoll(parts[2]);
        long long s = stoll(parts[3]);
        long long e = stoll(parts[4]);
        total += weighted(amount, s, e, qs, qe);
      } else if (parts[0] == "AddConsumptionRecord") {
        long long amount = stoll(parts[1]);
        long long s = stoll(parts[2]);
        long long e = stoll(parts[3]);
        total -= weighted(amount, s, e, qs, qe);
      }
    }
    return roundToI32(total);
  }
};
