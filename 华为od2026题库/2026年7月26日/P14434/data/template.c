#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 2048

char* convertNumber(char* num, char* sourceDigits, char* targetDigits);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int i = 0;
    char num[MAX_LEN], sourceDigits[MAX_LEN], targetDigits[MAX_LEN];
    int j;

    // 解析 num
    while (line[i] && line[i] != '"') i++;
    i++;
    j = 0;
    while (line[i] && line[i] != '"') num[j++] = line[i++];
    num[j] = '\0';
    i++;

    // 解析 sourceDigits
    while (line[i] && line[i] != '"') i++;
    i++;
    j = 0;
    while (line[i] && line[i] != '"') sourceDigits[j++] = line[i++];
    sourceDigits[j] = '\0';
    i++;

    // 解析 targetDigits
    while (line[i] && line[i] != '"') i++;
    i++;
    j = 0;
    while (line[i] && line[i] != '"') targetDigits[j++] = line[i++];
    targetDigits[j] = '\0';

    char* result = convertNumber(num, sourceDigits, targetDigits);
    printf("\"%s\"\n", result);
    free(result);
    return 0;
}
