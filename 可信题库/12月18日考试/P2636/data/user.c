#include <stdlib.h>

typedef struct {
    int interfaceId;
    int time;
} InvokeInfo;

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* getInterfaces(InvokeInfo* invokes, int invokesSize, int timeSegment, int minLimits, int* returnSize) {
    (void)invokes;
    (void)invokesSize;
    (void)timeSegment;
    (void)minLimits;
    *returnSize = 0;
    return NULL;
}
