#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000
#define MAX_TOKENS 1000

// 解析 [1,2,3] 形式的整型数组
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

int catFishCardGame(int* cardA, int cardASize, int* cardB, int cardBSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    const char* comma = strstr(line, "],[");
    int splitPos = (int)(comma - line);
    char cardAStr[MAX_LEN];
    strncpy(cardAStr, line, splitPos + 1);
    cardAStr[splitPos + 1] = '\0';
    const char* cardBStr = line + splitPos + 2;
    int cardASize, cardBSize;
    int* cardA = parseIntList(cardAStr, &cardASize);
    int* cardB = parseIntList(cardBStr, &cardBSize);

    int result = catFishCardGame(cardA, cardASize, cardB, cardBSize);
    printf("%d\n", result);

    free(cardA);
    free(cardB);
    return 0;
}
