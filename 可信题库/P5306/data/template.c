#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 1000000
static void trim_nl(char* s) {
    int n = (int)strlen(s);
    while (n > 0 && (s[n-1]=='\n'||s[n-1]=='\r')) s[--n]=0;
}
LeaseManager* leaseManagerCreate(int ttl);
void leaseManagerFree(LeaseManager* obj);
bool leaseManagerAcquire(LeaseManager* obj, int resourceId, int nodeId, int time);
bool leaseManagerRenew(LeaseManager* obj, int resourceId, int nodeId, int time);
bool leaseManagerRelease(LeaseManager* obj, int resourceId, int nodeId);
int leaseManagerHolder(LeaseManager* obj, int resourceId, int time);
int leaseManagerAliveCount(LeaseManager* obj, int time);
int main() {
    char* line = (char*)malloc(MAX_LEN);
    LeaseManager* obj = NULL;
    while (fgets(line, MAX_LEN, stdin)) {
        trim_nl(line);
        if (!line[0]) continue;
        int a,b,c;
        if (sscanf(line, "LeaseManager(%d)", &a) == 1) {
            obj = leaseManagerCreate(a);
            puts("null");
        } else if (sscanf(line, "acquire(%d, %d, %d)", &a, &b, &c) == 3 || sscanf(line, "acquire(%d,%d,%d)", &a, &b, &c) == 3) {
            puts(leaseManagerAcquire(obj,a,b,c) ? "true" : "false");
        } else if (sscanf(line, "renew(%d, %d, %d)", &a, &b, &c) == 3 || sscanf(line, "renew(%d,%d,%d)", &a, &b, &c) == 3) {
            puts(leaseManagerRenew(obj,a,b,c) ? "true" : "false");
        } else if (sscanf(line, "release(%d, %d)", &a, &b) == 2 || sscanf(line, "release(%d,%d)", &a, &b) == 2) {
            puts(leaseManagerRelease(obj,a,b) ? "true" : "false");
        } else if (sscanf(line, "holder(%d, %d)", &a, &b) == 2 || sscanf(line, "holder(%d,%d)", &a, &b) == 2) {
            printf("%d\n", leaseManagerHolder(obj,a,b));
        } else if (sscanf(line, "aliveCount(%d)", &a) == 1) {
            printf("%d\n", leaseManagerAliveCount(obj,a));
        } else return 1;
    }
    free(line);
    return 0;
}
