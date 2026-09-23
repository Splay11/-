#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000

// 解析 [[a,b],[c,d]] 形式的二维数组
static int** parseInt2DArray(const char* s, int* outRows, int** outCols) {
    int** res = (int**)malloc(10000 * sizeof(int*));
    int* cols = (int*)malloc(10000 * sizeof(int));
    *outRows = 0;
    int cur[100], curCount = 0;
    bool inNum = false;
    char numBuf[50];
    int numLen = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c >= '0' && c <= '9')) {
            numBuf[numLen++] = c;
            inNum = true;
        } else {
            if (inNum) {
                numBuf[numLen] = '\0';
                cur[curCount++] = atoi(numBuf);
                numLen = 0;
                inNum = false;
            }
            if (c == ']') {
                if (curCount > 0) {
                    res[*outRows] = (int*)malloc(curCount * sizeof(int));
                    for (int j = 0; j < curCount; j++) res[*outRows][j] = cur[j];
                    cols[*outRows] = curCount;
                    (*outRows)++;
                    curCount = 0;
                }
            }
        }
    }
    *outCols = cols;
    return res;
}

int countIsolatedIntervals(int** intervals, int intervalsSize, int* intervalsColSize);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    int intervalsSize;
    int* intervalsColSize;
    int** intervals = parseInt2DArray(line, &intervalsSize, &intervalsColSize);

    int result = countIsolatedIntervals(intervals, intervalsSize, intervalsColSize);
    printf("%d\n", result);

    for (int i = 0; i < intervalsSize; i++) free(intervals[i]);
    free(intervals);
    free(intervalsColSize);
    return 0;
}
