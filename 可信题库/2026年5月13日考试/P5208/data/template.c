#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static void trim_inplace(char* s) {
    char* a = s;
    while (*a && isspace((unsigned char)*a)) a++;
    if (a != s) memmove(s, a, strlen(a) + 1);
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = '\0';
}

static int* parse_int_array(const char* s0, int* outCnt) {
    char buf[4096];
    strncpy(buf, s0, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';
    trim_inplace(buf);
    int* vals = (int*)malloc(sizeof(int) * 4096);
    *outCnt = 0;
    char* p = buf;
    if (*p != '[') {
        free(vals);
        return NULL;
    }
    p++;
    while (*p) {
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p == ']') break;
        char* end;
        long v = strtol(p, &end, 10);
        if (end == p) {
            free(vals);
            return NULL;
        }
        vals[(*outCnt)++] = (int)v;
        p = end;
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p == ']') break;
        if (*p != ',') {
            free(vals);
            return NULL;
        }
        p++;
    }
    return vals;
}

static void print_list(const int* a, int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        if (i) printf(", ");
        printf("%d", a[i]);
    }
    printf("]");
}

int main(void) {
    char line[8192];
    GCSystem* obj = NULL;
    int first = 1;
    while (fgets(line, sizeof(line), stdin)) {
        trim_inplace(line);
        if (line[0] == '\0') continue;
        if (!first) printf("\n");
        first = 0;

        int x;
        if (sscanf(line, "GCSystem(%d)", &x) == 1) {
            if (obj) gCSystemFree(obj);
            obj = gCSystemCreate(x);
            printf("null");
        } else if (sscanf(line, "createObject(%d)", &x) == 1) {
            gCSystemCreateObject(obj, x);
            printf("null");
        } else if (strncmp(line, "markObjects(", 12) == 0) {
            size_t n = strlen(line);
            if (n < 13 || line[n - 1] != ')') return 1;
            line[n - 1] = '\0';
            int cnt = 0;
            int* ids = parse_int_array(line + 12, &cnt);
            if (!ids) return 1;
            gCSystemMarkObjects(obj, ids, cnt);
            free(ids);
            printf("null");
        } else if (sscanf(line, "manualGC(%d)", &x) == 1) {
            gCSystemManualGC(obj, x);
            printf("null");
        } else if (sscanf(line, "getLiveObjects(%d)", &x) == 1) {
            int retSize = 0;
            int* live = gCSystemGetLiveObjects(obj, x, &retSize);
            print_list(live, retSize);
            free(live);
        } else {
            return 1;
        }
    }
    printf("\n");
    if (obj) gCSystemFree(obj);
    return 0;
}
