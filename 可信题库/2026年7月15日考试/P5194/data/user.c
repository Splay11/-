#include <stdbool.h>
#include <stdlib.h>

typedef struct LogSystem LogSystem;

struct LogSystem {
    int unused;
};

LogSystem* logSystemCreate(void) {
    return (LogSystem*)calloc(1, sizeof(LogSystem));
}

void logSystemFree(LogSystem* obj) {
    free(obj);
}

void logSystemEnter(LogSystem* obj, int spanId, bool inherit) {
    (void)obj;
    (void)spanId;
    (void)inherit;
}

char* logSystemLog(LogSystem* obj, char* msg) {
    (void)obj;
    return msg;
}

void logSystemLeave(LogSystem* obj, int spanId) {
    (void)obj;
    (void)spanId;
}
