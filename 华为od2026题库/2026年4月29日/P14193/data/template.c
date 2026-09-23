#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 500000
#define MAX_TOKENS 2000

static char*** parse2DStringList(const char* s, int* outRow, int** outColSizes) {
    char*** result = (char***)malloc(MAX_TOKENS * sizeof(char**));
    *outRow = 0;
    *outColSizes = (int*)malloc(MAX_TOKENS * sizeof(int));
    int i = 0;
    char* cur = (char*)malloc(MAX_LEN);

    // 跳过外层 [
    while (s[i] && s[i] != '[') i++;
    if (s[i] == '[') i++;

    while (s[i]) {
        // 跳过空白和逗号（可能出现在 "[[" 之间或行间）
        while (s[i] && (s[i] == ' ' || s[i] == ',' || s[i] == '\r' || s[i] == '\n')) i++;
        if (s[i] == ']') break; // 外层数组结束

        if (s[i] == '[') {
            i++; // 跳过内层 [
            char** row = (char**)malloc(MAX_TOKENS * sizeof(char*));
            int colCount = 0;
            bool inString = false;
            int curLen = 0;

            while (s[i] && !(s[i] == ']' && !inString)) {
                char c = s[i];
                if (c == '"') {
                    if (inString) {
                        cur[curLen] = '\0';
                        row[colCount] = (char*)malloc(curLen + 1);
                        strcpy(row[colCount], cur);
                        colCount++;
                        curLen = 0;
                    }
                    inString = !inString;
                } else if (inString) {
                    cur[curLen++] = c;
                }
                i++;
            }
            if (s[i] == ']') i++; // 跳过内层 ]

            if (colCount > 0) {
                result[*outRow] = (char**)malloc(colCount * sizeof(char*));
                for (int k = 0; k < colCount; k++) {
                    result[*outRow][k] = row[k];
                }
                (*outColSizes)[*outRow] = colCount;
                (*outRow)++;
            }
            free(row);
        } else {
            i++;
        }
    }

    free(cur);
    return result;
}

char* execute_command(char*** command, int commandSize, int* commandColSize);

int main() {
    char* input = (char*)malloc(MAX_LEN);
    if (!fgets(input, MAX_LEN, stdin)) { free(input); return 0; }
    int len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r')) input[--len] = '\0';
    int commandSize;
    int* commandColSize;
    char*** command = parse2DStringList(input, &commandSize, &commandColSize);
    char* result = execute_command(command, commandSize, commandColSize);
    printf("\"%s\"\n", result);
    free(result);
    for (int i = 0; i < commandSize; i++) {
        for (int j = 0; j < commandColSize[i]; j++) {
            free(command[i][j]);
        }
        free(command[i]);
    }
    free(command);
    free(commandColSize);
    free(input);
    return 0;
}
