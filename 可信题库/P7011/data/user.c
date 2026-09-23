#include <stdbool.h>
#include <stdlib.h>

typedef struct certAuthority certAuthority;

struct certAuthority {
    int unused;
};

certAuthority* certAuthorityCreate(void) {
    return (certAuthority*)calloc(1, sizeof(certAuthority));
}

void certAuthorityFree(certAuthority* obj) {
    free(obj);
}

bool certAuthorityIssue(certAuthority* obj, int certId, int parentId, int expireAt) {
    (void)obj;
    (void)certId;
    (void)parentId;
    (void)expireAt;
    return false;
}

bool certAuthorityRevoke(certAuthority* obj, int certId) {
    (void)obj;
    (void)certId;
    return false;
}

bool certAuthorityIsValid(certAuthority* obj, int certId, int now) {
    (void)obj;
    (void)certId;
    (void)now;
    return false;
}

int certAuthorityTtl(certAuthority* obj, int certId, int now) {
    (void)obj;
    (void)certId;
    (void)now;
    return -1;
}

int certAuthorityIssuerOf(certAuthority* obj, int certId) {
    (void)obj;
    (void)certId;
    return -1;
}

int certAuthorityRootOf(certAuthority* obj, int certId) {
    (void)obj;
    (void)certId;
    return -1;
}
