#include <stdbool.h>
#include <stdlib.h>

typedef struct JobQueueSys JobQueueSys;

struct JobQueueSys {
    int unused;
};

JobQueueSys* jobQueueSysCreate(void) {
    return (JobQueueSys*)calloc(1, sizeof(JobQueueSys));
}

void jobQueueSysFree(JobQueueSys* obj) {
    free(obj);
}

bool jobQueueSysSubmit(JobQueueSys* obj, int jobId, int priority) {
    (void)obj;
    (void)jobId;
    (void)priority;
    return false;
}

bool jobQueueSysCancel(JobQueueSys* obj, int jobId) {
    (void)obj;
    (void)jobId;
    return false;
}

int jobQueueSysPopJob(JobQueueSys* obj) {
    (void)obj;
    return -1;
}

int jobQueueSysPeekJob(JobQueueSys* obj) {
    (void)obj;
    return -1;
}
