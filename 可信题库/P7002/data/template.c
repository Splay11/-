#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[256];
    JobQueueSys* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (strcmp(line, "JobQueueSys()") == 0) {
            if (obj) jobQueueSysFree(obj);
            obj = jobQueueSysCreate();
            printf("null\n");
        } else if (sscanf(line, "submit(%d, %d)", &a, &b) == 2) {
            printf("%s\n", jobQueueSysSubmit(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "cancel(%d)", &a) == 1) {
            printf("%s\n", jobQueueSysCancel(obj, a) ? "true" : "false");
        } else if (strcmp(line, "popJob()") == 0) {
            printf("%d\n", jobQueueSysPopJob(obj));
        } else if (strcmp(line, "peekJob()") == 0) {
            printf("%d\n", jobQueueSysPeekJob(obj));
        } else {
            return 1;
        }
    }
    if (obj) jobQueueSysFree(obj);
    return 0;
}
