#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

static char* strip_quotes(char* s) {
    while (*s && isspace((unsigned char)*s)) s++;
    char* q1 = strchr(s, '"');
    if (!q1) return s;
    char* q2 = strchr(q1 + 1, '"');
    if (!q2) return q1 + 1;
    *q2 = '\0';
    return q1 + 1;
}

static int* parse_int_list(const char* s, int* outCnt) {
    int* ids = (int*)malloc(sizeof(int) * 1024);
    *outCnt = 0;
    const char* p = strchr(s, '[');
    if (!p) return ids;
    p++;
    while (*p && *p != ']') {
        while (*p && (isspace((unsigned char)*p) || *p == ',')) p++;
        if (*p == ']' || !*p) break;
        char* end;
        long v = strtol(p, &end, 10);
        if (end == p) break;
        ids[(*outCnt)++] = (int)v;
        p = end;
    }
    return ids;
}

int main(void) {
    char line[4096];
    ServiceMgrSys* sys = serviceMgrSysCreate();
    printf("null\n");
    if (!fgets(line, sizeof(line), stdin)) {
        serviceMgrSysFree(sys);
        return 0;
    }
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = '\0';
        if (len == 0) continue;

        if (strncmp(line, "startService", 12) == 0) {
            char* lp = strchr(line, '(');
            char* rp = strrchr(line, ')');
            if (!lp || !rp) return 1;
            *rp = '\0';
            char* comma = strchr(lp + 1, ',');
            if (!comma) return 1;
            *comma = '\0';
            int serverId = atoi(lp + 1);
            char* name = strip_quotes(comma + 1);
            printf("%s\n", serviceMgrSysStartService(sys, serverId, name) ? "true" : "false");
        } else if (strncmp(line, "addDependency", 13) == 0) {
            char* lp = strchr(line, '(');
            char* rp = strrchr(line, ')');
            if (!lp || !rp) return 1;
            *rp = '\0';
            char* comma = strchr(lp + 1, ',');
            if (!comma) return 1;
            *comma = '\0';
            char* from = strip_quotes(lp + 1);
            char* to = strip_quotes(comma + 1);
            printf("%s\n", serviceMgrSysAddDependency(sys, from, to) ? "true" : "false");
        } else if (strncmp(line, "isServiceAvailable", 18) == 0) {
            char* lp = strchr(line, '(');
            char* rp = strrchr(line, ')');
            if (!lp || !rp) return 1;
            *rp = '\0';
            char* name = strip_quotes(lp + 1);
            printf("%s\n", serviceMgrSysIsServiceAvailable(sys, name) ? "true" : "false");
        } else if (strncmp(line, "rebootServers", 13) == 0) {
            int cnt = 0;
            int* ids = parse_int_list(line, &cnt);
            serviceMgrSysRebootServers(sys, ids, cnt);
            free(ids);
            printf("null\n");
        }
    }
    serviceMgrSysFree(sys);
    return 0;
}
