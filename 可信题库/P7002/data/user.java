public class JobQueueSys {
    public JobQueueSys() {}

    public boolean submit(int jobId, int priority) {
        return false;
    }

    public boolean cancel(int jobId) {
        return false;
    }

    public int popJob() {
        return -1;
    }

    public int peekJob() {
        return -1;
    }
}
