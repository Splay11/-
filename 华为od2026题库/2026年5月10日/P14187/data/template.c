#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 2000000
#define MAX_TOKENS 200000

static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if ((c >= '0' && c <= '9')) {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                res[*outCount] = num;
                (*outCount)++;
                num = 0;
                inNum = false;
            }
        }
    }
    if (inNum) {
        res[*outCount] = num;
        (*outCount)++;
    }
    return res;
}

// 解析 [[u,v,type],[...]] 形式
static int** parseIntMatrix(const char* s, int* outCount) {
    int** res = (int**)malloc(MAX_TOKENS * sizeof(int*));
    *outCount = 0;
    int nums[3];
    int idx = 0, num = 0;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else if (c == ',' || c == ']' || c == '[') {
            if (inNum) {
                nums[idx++] = num;
                num = 0;
                inNum = false;
                if (idx == 3) {
                    res[*outCount] = (int*)malloc(3 * sizeof(int));
                    memcpy(res[*outCount], nums, 3 * sizeof(int));
                    (*outCount)++;
                    idx = 0;
                }
            }
        }
    }
    return res;
}

int* findIsolatedStations(int n, int* sources, int sourcesSize, int** pipes, int pipesSize, int* returnSize);

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line) return 1;
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    // 找 n
    int pos = 0;
    while (pos < len && line[pos] != ',') pos++;
    char nStr[50];
    strncpy(nStr, line, pos);
    nStr[pos] = '\0';
    int n = atoi(nStr);

    // 找 sources
    char* rest = line + pos + 1;
    char* mid = strstr(rest, "],[");
    int midPos = (int)(mid - rest);
    char* sourcesStr = (char*)malloc(midPos + 2);
    strncpy(sourcesStr, rest, midPos + 1);
    sourcesStr[midPos + 1] = '\0';
    char* pipesStr = rest + midPos + 2;

    int sourcesSize, pipesSize;
    int* sources = parseIntList(sourcesStr, &sourcesSize);
    int** pipes = parseIntMatrix(pipesStr, &pipesSize);

    int returnSize = 0;
    int* resArr = findIsolatedStations(n, sources, sourcesSize, pipes, pipesSize, &returnSize);

    printf("[");
    for (int i = 0; i < returnSize; i++) {
        printf("%d", resArr[i]);
        if (i + 1 < returnSize) printf(",");
    }
    printf("]\n");

    for (int i = 0; i < pipesSize; i++) free(pipes[i]);
    free(pipes);
    free(sources);
    free(sourcesStr);
    free(resArr);
    free(line);
    return 0;
}
