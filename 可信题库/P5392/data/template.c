#include "foo.c"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[4096];
    FileLockBoard* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (strcmp(line, "FileLockBoard()") == 0) {
            if (obj) fileLockBoardFree(obj);
            obj = fileLockBoardCreate();
            printf("null\n");
        } else if (sscanf(line, "lock(%d, %d)", &a, &b) == 2) {
            printf("%s\n", fileLockBoardLock(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "unlock(%d, %d)", &a, &b) == 2) {
            printf("%s\n", fileLockBoardUnlock(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "holder(%d)", &a) == 1) {
            printf("%d\n", fileLockBoardHolder(obj, a));
        } else if (strcmp(line, "lockedCount()") == 0) {
            printf("%d\n", fileLockBoardLockedCount(obj));
        } else {
            return 1;
        }
    }
    if (obj) fileLockBoardFree(obj);
    return 0;
}
