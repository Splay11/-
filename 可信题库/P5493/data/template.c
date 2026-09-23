#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[512];
    fileLogger* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (sscanf(line, "FileLogger(%d, %d)", &a, &b) == 2
            || sscanf(line, "FileLogger(%d,%d)", &a, &b) == 2) {
            if (obj) fileLoggerFree(obj);
            obj = fileLoggerCreate(a, b);
            printf("null\n");
        } else if (sscanf(line, "putLog(%d, %d)", &a, &b) == 2
                   || sscanf(line, "putLog(%d,%d)", &a, &b) == 2) {
            printf("%d\n", fileLoggerPutLog(obj, a, b));
        } else if (strcmp(line, "totalSize()") == 0) {
            printf("%d\n", fileLoggerTotalSize(obj));
        } else if (strcmp(line, "listFiles()") == 0) {
            int n = 0;
            logChunk* fs = fileLoggerListFiles(obj, &n);
            printf("[");
            for (int i = 0; i < n; i++) {
                if (i) printf(", ");
                printf("[%d, %d, %d]", fs[i].mid, fs[i].idx, fs[i].sz);
            }
            printf("]\n");
        } else {
            return 1;
        }
    }
    if (obj) fileLoggerFree(obj);
    return 0;
}
