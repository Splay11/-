#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000

int maxChargingDemand(int n, int m, int k, int* demands);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int n = 0, m = 0, k = 0;
    char arrStr[MAX_LEN];
    int idx = 0, cnt = 0;
    char *token;
    char tmp[MAX_LEN];
    strcpy(tmp, line);

    // Parse n,m,k,[array]
    // format: n,m,k,[a,b,c,...]
    char *start = tmp;
    char *comma1 = strchr(start, ',');
    *comma1 = '\0';
    n = atoi(start);

    char *comma2 = strchr(comma1 + 1, ',');
    *comma2 = '\0';
    m = atoi(comma1 + 1);

    char *comma3 = strchr(comma2 + 1, ',');
    *comma3 = '\0';
    k = atoi(comma2 + 1);

    char *arrayStart = strchr(comma3 + 1, '[');
    char *arrayEnd = strchr(comma3 + 1, ']');
    char arrayContent[MAX_LEN];
    strncpy(arrayContent, arrayStart + 1, arrayEnd - arrayStart - 1);
    arrayContent[arrayEnd - arrayStart - 1] = '\0';

    // parse arrayContent as ints
    int *demands = (int*)malloc(n * sizeof(int));
    cnt = 0;
    token = strtok(arrayContent, ",");
    while (token) {
        demands[cnt++] = atoi(token);
        token = strtok(NULL, ",");
    }

    int result = maxChargingDemand(n, m, k, demands);
    printf("%d\n", result);

    free(demands);
    return 0;
}
