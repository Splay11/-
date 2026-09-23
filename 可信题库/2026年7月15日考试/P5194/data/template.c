#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

static void trim_inplace(char* s) {
    char* a = s;
    while (*a && isspace((unsigned char)*a)) a++;
    if (a != s) memmove(s, a, strlen(a) + 1);
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = '\0';
}

static char* extract_quoted(const char* s) {
    const char* p = strchr(s, '"');
    if (!p) return NULL;
    p++;
    const char* q = strchr(p, '"');
    if (!q) return NULL;
    size_t n = (size_t)(q - p);
    char* out = (char*)malloc(n + 1);
    memcpy(out, p, n);
    out[n] = '\0';
    return out;
}

int main(void) {
    char line[1024];
    LogSystem* obj = NULL;
    int first = 1;
    while (fgets(line, sizeof(line), stdin)) {
        trim_inplace(line);
        if (line[0] == '\0') continue;
        if (!first) printf("\n");
        first = 0;

        if (strcmp(line, "LogSystem()") == 0) {
            if (obj) logSystemFree(obj);
            obj = logSystemCreate();
            printf("null");
        } else if (strncmp(line, "log(", 4) == 0) {
            char* msg = extract_quoted(line);
            if (!msg) return 1;
            char* ret = logSystemLog(obj, msg);
            printf("\"%s\"", ret ? ret : "");
            if (ret && ret != msg) free(ret);
            free(msg);
        } else if (strncmp(line, "enter(", 6) == 0) {
            int id;
            char boolBuf[16];
            if (sscanf(line, "enter(%d, %15[^)])", &id, boolBuf) != 2) return 1;
            trim_inplace(boolBuf);
            logSystemEnter(obj, id, strcmp(boolBuf, "true") == 0);
            printf("null");
        } else if (strncmp(line, "leave(", 6) == 0) {
            int id;
            if (sscanf(line, "leave(%d)", &id) != 1) return 1;
            logSystemLeave(obj, id);
            printf("null");
        } else {
            return 1;
        }
    }
    printf("\n");
    if (obj) logSystemFree(obj);
    return 0;
}
