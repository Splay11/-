#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int* timeClassification(char* timeRange, int* returnSize);

int main() {
    char line[1000];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    int returnSize = 0;
    int* result = timeClassification(line, &returnSize);
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("%d", result[i]);
    }
    printf("]\n");
    free(result);
    return 0;
}
