#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char line[256];
    MemMgmtSys* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (sscanf(line, "MemMgmtSys(%d)", &a) == 1) {
            if (obj) memMgmtSysFree(obj);
            obj = memMgmtSysCreate(a);
            printf("null\n");
        } else if (sscanf(line, "processMemAlloc(%d, %d)", &a, &b) == 2) {
            printf("%d\n", memMgmtSysProcessMemAlloc(obj, a, b));
        } else if (sscanf(line, "processMemFree(%d)", &a) == 1) {
            memMgmtSysProcessMemFree(obj, a);
            printf("null\n");
        } else if (sscanf(line, "processMemQuery(%d)", &a) == 1) {
            printf("%d\n", memMgmtSysProcessMemQuery(obj, a));
        } else {
            return 1;
        }
    }
    if (obj) memMgmtSysFree(obj);
    return 0;
}
