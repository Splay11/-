#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 4096

char* mergeBroadcastChannels(int n, const char* channels);

static int findTopLevelComma(const char* s) {
    bool inString = false;
    int bracket = 0;
    int len = (int)strlen(s);
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '"') {
            inString = !inString;
        } else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int comma = findTopLevelComma(line);
    char nStr[16];
    strncpy(nStr, line, comma);
    nStr[comma] = '\0';
    int n = atoi(nStr);

    // 提取引号内的字符串
    const char* rest = line + comma + 1;
    const char* startQuote = strchr(rest, '"');
    const char* endQuote = strrchr(rest, '"');
    char channels[MAX_LEN];
    int chanLen = (int)(endQuote - startQuote - 1);
    strncpy(channels, startQuote + 1, chanLen);
    channels[chanLen] = '\0';

    char* result = mergeBroadcastChannels(n, channels);
    printf("%s\n", result);
    free(result);

    return 0;
}
