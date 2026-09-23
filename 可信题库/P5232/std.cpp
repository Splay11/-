#include <algorithm>
#include <utility>
#include <vector>

using namespace std;

class MemMgmtSys {
    int n;
    vector<int> page;                 // -1 = free
    vector<pair<int, int>> info_map;  // sparse: use linear search; n tiny

    int findSlot(int size) {
        int i = 0;
        while (i < n) {
            if (page[i] != -1) {
                i++;
                continue;
            }
            int j = i;
            while (j < n && page[j] == -1) j++;
            if (j - i >= size) return i;
            i = j;
        }
        return -1;
    }

    int getSize(int pid) {
        for (int i = 0; i < n; i++)
            if (page[i] == pid) {
                int j = i;
                while (j < n && page[j] == pid) j++;
                return j - i;
            }
        return 0;
    }

    int getStart(int pid) {
        for (int i = 0; i < n; i++)
            if (page[i] == pid) return i;
        return -1;
    }

    void defrag() {
        vector<pair<int, int>> items;  // (size, pid)
        vector<char> seen(10001, 0);
        for (int i = 0; i < n; i++) {
            int pid = page[i];
            if (pid < 0 || seen[pid]) continue;
            seen[pid] = 1;
            items.push_back({getSize(pid), pid});
        }
        sort(items.begin(), items.end());
        fill(page.begin(), page.end(), -1);
        int used = 0;
        for (auto& e : items) used += e.first;
        int pos = n - used;
        for (auto& e : items) {
            int sz = e.first, pid = e.second;
            for (int k = 0; k < sz; k++) page[pos + k] = pid;
            pos += sz;
        }
    }

   public:
    MemMgmtSys(int num) : n(num), page(num, -1) {}

    int processMemAlloc(int processId, int size) {
        int st = findSlot(size);
        if (st < 0) {
            defrag();
            st = findSlot(size);
            if (st < 0) return -1;
        }
        for (int k = 0; k < size; k++) page[st + k] = processId;
        return st;
    }

    void processMemFree(int processId) {
        for (int i = 0; i < n; i++)
            if (page[i] == processId) page[i] = -1;
    }

    int processMemQuery(int processId) { return getStart(processId); }
};
