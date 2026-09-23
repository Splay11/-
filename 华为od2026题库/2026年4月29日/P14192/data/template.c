#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int countValidPatterns(char* L);

int main() {
    char line[1005];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    char L[20];
    if (len == 0) {
        L[0] = '\0';
    } else {
        int j = 0;
        bool inStr = false;
        for (int i = 0; i < len; i++) {
            if (line[i] == '"') {
                inStr = !inStr;
            } else if (inStr) {
                L[j++] = line[i];
            }
        }
        L[j] = '\0';
    }

    int result = countValidPatterns(L);
    printf("%d\n", result);
    return 0;
}
