#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_LEN 200005

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!fgets(line, MAX_LEN, stdin)) { free(line); return 0; }
    int n = (int)strlen(line);
    while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r'))
        line[--n] = '\0';

    int* arr = (int*)malloc(MAX_LEN * sizeof(int));
    int arrSize = 0;
    int num = 0;
    bool have = false;
    bool neg = false;
    for (int i = 0; line[i]; i++) {
        char c = line[i];
        if (isdigit((unsigned char)c)) {
            num = num * 10 + (c - '0');
            have = true;
        } else if (c == '-' && !have) {
            neg = true;
        } else if (have) {
            arr[arrSize++] = neg ? -num : num;
            num = 0; have = false; neg = false;
        }
    }
    if (have) arr[arrSize++] = neg ? -num : num;

    int result = countDistinctTags(arr, arrSize);
    printf("%d\n", result);

    free(arr);
    free(line);
    return 0;
}
