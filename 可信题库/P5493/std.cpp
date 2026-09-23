#include <unordered_map>
#include <vector>
using namespace std;

class FileLogger {
  struct LogChunk {
    int mid, idx, sz;
    LogChunk(int m, int i) : mid(m), idx(i), sz(0) {}
  };
  int cap, quota;
  vector<LogChunk*> files;
  unordered_map<int, LogChunk*> cur;
  unordered_map<int, int> seq;

  int usedSum() {
    int s = 0;
    for (auto* f : files) s += f->sz;
    return s;
  }

  void dropOldest() {
    LogChunk* f = files.front();
    files.erase(files.begin());
    if (cur.count(f->mid) && cur[f->mid] == f) cur.erase(f->mid);
    delete f;
  }

 public:
  FileLogger(int fileCap, int totalCap) : cap(fileCap), quota(totalCap) {}
  ~FileLogger() {
    for (auto* f : files) delete f;
  }

  int totalSize() { return usedSum(); }

  int putLog(int mid, int nbytes) {
    while (usedSum() + nbytes > quota) dropOldest();
    LogChunk* now = cur.count(mid) ? cur[mid] : nullptr;
    if (!now || now->sz + nbytes > cap) {
      int nxt = seq[mid] + 1;
      seq[mid] = nxt;
      now = new LogChunk(mid, nxt);
      files.push_back(now);
      cur[mid] = now;
    }
    now->sz += nbytes;
    return now->sz;
  }

  vector<vector<int>> listFiles() {
    vector<vector<int>> ans;
    for (auto* f : files) ans.push_back({f->mid, f->idx, f->sz});
    return ans;
  }
};
