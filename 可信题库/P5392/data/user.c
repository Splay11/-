#include <stdbool.h>
#include <stdlib.h>

typedef struct FileLockBoard FileLockBoard;

struct FileLockBoard {
    int unused;
};

FileLockBoard* fileLockBoardCreate(void) {
    return (FileLockBoard*)calloc(1, sizeof(FileLockBoard));
}

void fileLockBoardFree(FileLockBoard* obj) {
    free(obj);
}

bool fileLockBoardLock(FileLockBoard* obj, int fileId, int ownerId) {
    (void)obj;
    (void)fileId;
    (void)ownerId;
    return false;
}

bool fileLockBoardUnlock(FileLockBoard* obj, int fileId, int ownerId) {
    (void)obj;
    (void)fileId;
    (void)ownerId;
    return false;
}

int fileLockBoardHolder(FileLockBoard* obj, int fileId) {
    (void)obj;
    (void)fileId;
    return -1;
}

int fileLockBoardLockedCount(FileLockBoard* obj) {
    (void)obj;
    return 0;
}
