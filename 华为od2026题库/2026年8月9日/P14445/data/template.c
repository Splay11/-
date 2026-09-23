#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 前置声明用户函数
int findBestChargingTime(int priceRecords, int hours, int* priceArray);

int main() {
    char line[4096];
    fgets(line, sizeof(line), stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析 priceRecords
    int firstComma = -1;
    for (int i = 0; i < len; i++) {
        if (line[i] == ',') { firstComma = i; break; }
    }
    char tmp[16];
    strncpy(tmp, line, firstComma);
    tmp[firstComma] = '\0';
    int priceRecords = atoi(tmp);

    // 解析 hours
    char* rest = line + firstComma + 1;
    int secondComma = -1;
    int restLen = strlen(rest);
    for (int i = 0; i < restLen; i++) {
        if (rest[i] == ',') { secondComma = i; break; }
    }
    strncpy(tmp, rest, secondComma);
    tmp[secondComma] = '\0';
    int hours = atoi(tmp);

    // 解析数组 [a,b,c,...]
    char* arrStr = rest + secondComma + 1;
    int priceArray[24];
    int arrSize = 0;
    int num = 0;
    int hasNum = 0;
    for (int i = 0; arrStr[i]; i++) {
        char c = arrStr[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            hasNum = 1;
        } else if (hasNum) {
            priceArray[arrSize++] = num;
            num = 0;
            hasNum = 0;
        }
    }
    if (hasNum) priceArray[arrSize++] = num;

    int result = findBestChargingTime(priceRecords, hours, priceArray);
    printf("%d\n", result);
    return 0;
}
