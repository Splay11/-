#include <stdlib.h>

typedef struct MemMgmtSys MemMgmtSys;

struct MemMgmtSys {
    int unused;
};

MemMgmtSys* memMgmtSysCreate(int num) {
    (void)num;
    return (MemMgmtSys*)calloc(1, sizeof(MemMgmtSys));
}

void memMgmtSysFree(MemMgmtSys* obj) {
    free(obj);
}

int memMgmtSysProcessMemAlloc(MemMgmtSys* obj, int processId, int size) {
    (void)obj;
    (void)processId;
    (void)size;
    return -1;
}

void memMgmtSysProcessMemFree(MemMgmtSys* obj, int processId) {
    (void)obj;
    (void)processId;
}

int memMgmtSysProcessMemQuery(MemMgmtSys* obj, int processId) {
    (void)obj;
    (void)processId;
    return -1;
}
