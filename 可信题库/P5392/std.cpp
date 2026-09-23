#include <unordered_map>
using namespace std;

class FileLockBoard {
    unordered_map<int, int> own;

public:
    FileLockBoard() {}

    bool lock(int fileId, int ownerId) {
        if (own.count(fileId)) return false;
        own[fileId] = ownerId;
        return true;
    }

    bool unlock(int fileId, int ownerId) {
        auto it = own.find(fileId);
        if (it == own.end() || it->second != ownerId) return false;
        own.erase(it);
        return true;
    }

    int holder(int fileId) {
        auto it = own.find(fileId);
        return it == own.end() ? -1 : it->second;
    }

    int lockedCount() { return (int)own.size(); }
};
