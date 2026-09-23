class FileLockBoard {
    constructor() {}
    lock(fileId, ownerId) {
        return false;
    }
    unlock(fileId, ownerId) {
        return false;
    }
    holder(fileId) {
        return -1;
    }
    lockedCount() {
        return 0;
    }
}
