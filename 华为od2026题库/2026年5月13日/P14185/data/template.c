#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int getMaxDivisibleNumber(char* inputStr, int inputDivisor);

int main() {
    char line[10050];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len-1]=='\n' || line[len-1]=='\r')) line[--len]='\0';

    char strPart[10050];
    int divisor = 0;

    bool inQuote = false;
    int strLen = 0;
    for (int i = 0; i < len; i++) {
        char c = line[i];
        if (c == '"') {
            inQuote = !inQuote;
            continue;
        }
        if (inQuote) {
            strPart[strLen++] = c;
        } else if (c == ',') {
            divisor = atoi(line + i + 1);
            break;
        }
    }
    strPart[strLen] = '\0';

    int result = getMaxDivisibleNumber(strPart, divisor);
    printf("%d\n", result);
    return 0;
}
