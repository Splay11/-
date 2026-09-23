#include <stdlib.h>

typedef struct {
    int mid, idx, sz;
} logChunk;

typedef struct {
    int unused;
} fileLogger;

fileLogger* fileLoggerCreate(int fileCap, int totalCap) {
    (void)fileCap;
    (void)totalCap;
    return (fileLogger*)calloc(1, sizeof(fileLogger));
}

void fileLoggerFree(fileLogger* obj) { free(obj); }

int fileLoggerPutLog(fileLogger* obj, int mid, int nbytes) {
    (void)obj;
    (void)mid;
    (void)nbytes;
    return 0;
}

int fileLoggerTotalSize(fileLogger* obj) {
    (void)obj;
    return 0;
}

logChunk* fileLoggerListFiles(fileLogger* obj, int* returnSize) {
    (void)obj;
    *returnSize = 0;
    return NULL;
}
