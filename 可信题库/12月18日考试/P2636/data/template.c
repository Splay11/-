#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static char* read_line(void) {
    size_t cap = 1 << 16, len = 0;
    char* buf = (char*)malloc(cap);
    int c;
    while ((c = getchar()) != EOF && c != '\n') {
        if (c == '\r') continue;
        if (len + 1 >= cap) {
            cap *= 2;
            buf = (char*)realloc(buf, cap);
        }
        buf[len++] = (char)c;
    }
    if (c == EOF && len == 0) {
        free(buf);
        return NULL;
    }
    buf[len] = '\0';
    return buf;
}

int main(void) {
    char* line = read_line();
    if (!line) return 0;

    InvokeInfo* invokes = (InvokeInfo*)malloc(sizeof(InvokeInfo) * 200000);
    int invokesSize = 0;
    char* p = line;
    while (*p) {
        while (*p && *p != '[') p++;
        if (!*p) break;
        p++;
        while (*p && isspace((unsigned char)*p)) p++;
        char* end;
        long t = strtol(p, &end, 10);
        if (end == p) break;
        p = end;
        while (*p && (isspace((unsigned char)*p) || *p == ',')) p++;
        long id = strtol(p, &end, 10);
        if (end == p) break;
        p = end;
        invokes[invokesSize].time = (int)t;
        invokes[invokesSize].interfaceId = (int)id;
        invokesSize++;
        while (*p && *p != ']') p++;
        if (*p == ']') p++;
    }
    free(line);

    int timeSegment = 0, minLimits = 0;
    if (scanf("%d", &timeSegment) != 1) return 1;
    if (scanf("%d", &minLimits) != 1) return 1;

    int returnSize = 0;
    int* ans = getInterfaces(invokes, invokesSize, timeSegment, minLimits, &returnSize);
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i) printf(", ");
        printf("%d", ans[i]);
    }
    printf("]");
    free(ans);
    free(invokes);
    return 0;
}
