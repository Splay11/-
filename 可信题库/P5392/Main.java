import java.util.HashMap;
import java.util.Map;

class FileLockBoard {
    private Map<Integer, Integer> own = new HashMap<>();

    public FileLockBoard() {}

    public boolean lock(int fileId, int ownerId) {
        if (own.containsKey(fileId)) return false;
        own.put(fileId, ownerId);
        return true;
    }

    public boolean unlock(int fileId, int ownerId) {
        Integer h = own.get(fileId);
        if (h == null || h != ownerId) return false;
        own.remove(fileId);
        return true;
    }

    public int holder(int fileId) {
        Integer h = own.get(fileId);
        return h == null ? -1 : h;
    }

    public int lockedCount() {
        return own.size();
    }
}
