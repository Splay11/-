#include <stdbool.h>
#include <stdlib.h>

typedef struct ServiceMgrSys ServiceMgrSys;

struct ServiceMgrSys {
    int unused;
};

ServiceMgrSys* serviceMgrSysCreate(void) {
    return (ServiceMgrSys*)calloc(1, sizeof(ServiceMgrSys));
}

void serviceMgrSysFree(ServiceMgrSys* obj) {
    free(obj);
}

void serviceMgrSysRebootServers(ServiceMgrSys* obj, int* serverIds, int serverIdsSize) {
    (void)obj;
    (void)serverIds;
    (void)serverIdsSize;
}

bool serviceMgrSysStartService(ServiceMgrSys* obj, int serverId, char* serviceName) {
    (void)obj;
    (void)serverId;
    (void)serviceName;
    return false;
}

bool serviceMgrSysAddDependency(ServiceMgrSys* obj, char* fromServiceName, char* toServiceName) {
    (void)obj;
    (void)fromServiceName;
    (void)toServiceName;
    return false;
}

bool serviceMgrSysIsServiceAvailable(ServiceMgrSys* obj, char* serviceName) {
    (void)obj;
    (void)serviceName;
    return false;
}
