class ClusterPool {
    public ClusterPool() {}

    public boolean addNode(int nodeId, int capacity) {
        return false;
    }

    public boolean removeNode(int nodeId) {
        return false;
    }

    public int submit(int jobId, int size) {
        return -1;
    }

    public boolean kill(int jobId) {
        return false;
    }

    public int usedOf(int nodeId) {
        return -1;
    }

    public int freeOf(int nodeId) {
        return -1;
    }

    public int jobNode(int jobId) {
        return -1;
    }
}

public class Solution {}
