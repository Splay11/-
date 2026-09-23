class FileLockBoard {
public:
    FileLockBoard() {}
    bool lock(int fileId, int ownerId) {
        (void)fileId;
        (void)ownerId;
        return false;
    }
    bool unlock(int fileId, int ownerId) {
        (void)fileId;
        (void)ownerId;
        return false;
    }
    int holder(int fileId) {
        (void)fileId;
        return -1;
    }
    int lockedCount() { return 0; }
};
