class FileLockBoard {
    public FileLockBoard() {}

    public boolean lock(int fileId, int ownerId) {
        return false;
    }

    public boolean unlock(int fileId, int ownerId) {
        return false;
    }

    public int holder(int fileId) {
        return -1;
    }

    public int lockedCount() {
        return 0;
    }
}
