#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000
#define MAX_TOKENS 1000

static int* parseIntArray(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_TOKENS * sizeof(int));
    *outCount = 0;
    int num = 0, sign = 1;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') { sign = -1; }
        else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                res[*outCount] = num * sign;
                (*outCount)++;
                num = 0;
                sign = 1;
                inNum = false;
            }
        }
    }
    if (inNum) {
        res[*outCount] = num * sign;
        (*outCount)++;
    }
    return res;
}

// parse 2D array like [[1,2],[3,4]]
static int** parseInt2DArray(const char* s, int* outSize) {
    int** res = (int**)malloc(MAX_TOKENS * sizeof(int*));
    *outSize = 0;
    int cur[2];
    int curLen = 0;
    int num = 0, sign = 1;
    bool inNum = false;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '-') { sign = -1; }
        else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else {
            if (inNum) {
                cur[curLen++] = num * sign;
                num = 0;
                sign = 1;
                inNum = false;
            }
            if (c == ']' && curLen == 2) {
                res[*outSize] = (int*)malloc(2 * sizeof(int));
                res[*outSize][0] = cur[0];
                res[*outSize][1] = cur[1];
                (*outSize)++;
                curLen = 0;
            }
        }
    }
    return res;
}

int** selectMaxWeightPolicies(int n, int k, int* weights, int** conflicts, int conflictsSize, int* returnSize);

int main() {
    char input[MAX_LEN];
    if (!fgets(input, MAX_LEN, stdin)) return 0;
    int len = strlen(input);
    while (len > 0 && (input[len-1]=='\n'||input[len-1]=='\r')) input[--len]='\0';

    // input format: n,k,[weights],[conflicts]
    // find first comma
    int idx = 0, stage = 0;
    int n = 0, k = 0;
    char weightsStr[MAX_LEN];
    char conflictsStr[MAX_LEN];
    int pos = 0;
    int i = 0;
    // parse n
    while (input[i] && input[i] != ',') i++;
    char tmp[100];
    strncpy(tmp, input, i);
    tmp[i] = '\0';
    n = atoi(tmp);
    i++;
    // parse k
    int start = i;
    while (input[i] && input[i] != ',') i++;
    strncpy(tmp, input + start, i - start);
    tmp[i - start] = '\0';
    k = atoi(tmp);
    i++;
    // parse weights array
    int lbr = 0;
    while (input[i]) {
        if (input[i] == '[') { lbr++; if (lbr == 1) start = i; }
        else if (input[i] == ']') {
            lbr--;
            if (lbr == 0) {
                strncpy(weightsStr, input + start, i - start + 1);
                weightsStr[i - start + 1] = '\0';
                i++;
                break;
            }
        }
        i++;
    }
    // skip comma
    while (input[i] && input[i] != '[') i++;
    lbr = 0;
    while (input[i]) {
        if (input[i] == '[') {
            lbr++;
            if (lbr == 1) start = i;
        }
        else if (input[i] == ']') {
            lbr--;
            if (lbr == 0) {
                strncpy(conflictsStr, input + start, i - start + 1);
                conflictsStr[i - start + 1] = '\0';
                break;
            }
        }
        i++;
    }

    int weightsSize = 0;
    int* weights = parseIntArray(weightsStr, &weightsSize);
    int conflictsSize = 0;
    int** conflicts = parseInt2DArray(conflictsStr, &conflictsSize);

    int returnSize = 0;
    int** result = selectMaxWeightPolicies(n, k, weights, conflicts, conflictsSize, &returnSize);

    printf("[");
    for (int a = 0; a < returnSize; a++) {
        if (a > 0) printf(",");
        printf("[");
        int j = 0;
        while (result[a][j] != 0) j++;
        for (int b = 0; b < j; b++) {
            if (b > 0) printf(",");
            printf("%d", result[a][b]);
        }
        printf("]");
    }
    printf("]\n");

    free(weights);
    for (int x = 0; x < conflictsSize; x++) free(conflicts[x]);
    free(conflicts);
    return 0;
}
