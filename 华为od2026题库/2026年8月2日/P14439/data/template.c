#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAX_LEN 256

#include "foo.c"

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析三个逗号分隔的值：capacity,efficiency,scene
    char* comma1 = strchr(line, ',');
    *comma1 = '\0';
    double capacity = atof(line);

    char* rest1 = comma1 + 1;
    char* comma2 = strchr(rest1, ',');
    *comma2 = '\0';
    double efficiency = atof(rest1);

    int scene = atoi(comma2 + 1);

    int result = calculateRange(capacity, efficiency, scene);
    printf("%d\n", result);

    return 0;
}
