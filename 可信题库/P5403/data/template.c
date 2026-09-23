#include "foo.c"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main(void) {
    char line[4096];
    MicQueue* obj = NULL;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        int a, b;
        if (strcmp(line, "MicQueue()") == 0) {
            if (obj) micQueueFree(obj);
            obj = micQueueCreate();
            printf("null\n");
        } else if (sscanf(line, "enroll(%d, %d)", &a, &b) == 2) {
            printf("%s\n", micQueueEnroll(obj, a, b) ? "true" : "false");
        } else if (strcmp(line, "nextPlay()") == 0) {
            printf("%d\n", micQueueNextPlay(obj));
        } else if (sscanf(line, "boost(%d, %d)", &a, &b) == 2) {
            printf("%s\n", micQueueBoost(obj, a, b) ? "true" : "false");
        } else if (sscanf(line, "cancel(%d)", &a) == 1) {
            printf("%s\n", micQueueCancel(obj, a) ? "true" : "false");
        } else if (strcmp(line, "waiting()") == 0) {
            printf("%d\n", micQueueWaiting(obj));
        } else {
            return 1;
        }
    }
    if (obj) micQueueFree(obj);
    return 0;
}
