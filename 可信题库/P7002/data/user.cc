class JobQueueSys {
 public:
  JobQueueSys() {}
  bool submit(int jobId, int priority) { return false; }
  bool cancel(int jobId) { return false; }
  int popJob() { return -1; }
  int peekJob() { return -1; }
};
