import java.util.*;

class FileLogger {
    static class LogChunk {
        int mid, idx, sz;
        LogChunk(int mid, int idx) {
            this.mid = mid;
            this.idx = idx;
        }
    }

    private int cap, quota;
    private List<LogChunk> files = new ArrayList<>();
    private Map<Integer, LogChunk> cur = new HashMap<>();
    private Map<Integer, Integer> seq = new HashMap<>();

    public FileLogger(int fileCap, int totalCap) {
        this.cap = fileCap;
        this.quota = totalCap;
    }

    public int totalSize() {
        int s = 0;
        for (LogChunk f : files) s += f.sz;
        return s;
    }

    private void dropOldest() {
        LogChunk f = files.remove(0);
        if (cur.get(f.mid) == f) cur.remove(f.mid);
    }

    public int putLog(int mid, int nbytes) {
        while (totalSize() + nbytes > quota) dropOldest();
        LogChunk now = cur.get(mid);
        if (now == null || now.sz + nbytes > cap) {
            int nxt = seq.getOrDefault(mid, 0) + 1;
            seq.put(mid, nxt);
            now = new LogChunk(mid, nxt);
            files.add(now);
            cur.put(mid, now);
        }
        now.sz += nbytes;
        return now.sz;
    }

    public int[][] listFiles() {
        int[][] ans = new int[files.size()][3];
        for (int i = 0; i < files.size(); i++) {
            LogChunk f = files.get(i);
            ans[i][0] = f.mid;
            ans[i][1] = f.idx;
            ans[i][2] = f.sz;
        }
        return ans;
    }
}
