#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 500000
#define MAX_NODES 100000

struct TreeNode {
    int val;
    struct TreeNode* left;
    struct TreeNode* right;
};

#include "foo.c"

static struct TreeNode* parseTree(const char* s) {
    int len = strlen(s);
    int pos = 0;
    if (len == 0) return NULL;
    while (pos < len && (s[pos] == '{' || s[pos] == ' ')) pos++;
    int end = len - 1;
    while (end >= 0 && (s[end] == '}' || s[end] == ' ' || s[end] == '\n' || s[end] == '\r')) end--;
    int tokens = 0;
    char** parts = (char**)malloc(MAX_NODES * sizeof(char*));
    int i = pos;
    char cur[20];
    int curLen = 0;
    while (i <= end) {
        char c = s[i];
        if (c == ',') {
            cur[curLen] = '\0';
            parts[tokens] = (char*)malloc(curLen + 1);
            strcpy(parts[tokens++], cur);
            curLen = 0;
        } else {
            cur[curLen++] = c;
        }
        i++;
    }
    if (curLen > 0) {
        cur[curLen] = '\0';
        parts[tokens] = (char*)malloc(curLen + 1);
        strcpy(parts[tokens++], cur);
    }
    if (tokens == 0) { free(parts); return NULL; }
    if (tokens == 1 && (strcmp(parts[0], "#") == 0 || strlen(parts[0]) == 0)) {
        for (int j = 0; j < tokens; j++) free(parts[j]);
        free(parts);
        return NULL;
    }

    // BFS 队列方式建树
    struct TreeNode* root = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    root->val = atoi(parts[0]);
    root->left = NULL;
    root->right = NULL;
    free(parts[0]);

    struct TreeNode** queue = (struct TreeNode**)malloc(MAX_NODES * sizeof(struct TreeNode*));
    int qHead = 0, qTail = 0;
    queue[qTail++] = root;

    int idx = 1;
    while (qHead < qTail && idx < tokens) {
        struct TreeNode* node = queue[qHead++];

        // left child
        if (idx < tokens) {
            char* tok = parts[idx++];
            if (strcmp(tok, "#") != 0 && strlen(tok) > 0) {
                struct TreeNode* leftNode = (struct TreeNode*)malloc(sizeof(struct TreeNode));
                leftNode->val = atoi(tok);
                leftNode->left = NULL;
                leftNode->right = NULL;
                node->left = leftNode;
                queue[qTail++] = leftNode;
            }
            free(tok);
        }

        // right child
        if (idx < tokens) {
            char* tok = parts[idx++];
            if (strcmp(tok, "#") != 0 && strlen(tok) > 0) {
                struct TreeNode* rightNode = (struct TreeNode*)malloc(sizeof(struct TreeNode));
                rightNode->val = atoi(tok);
                rightNode->left = NULL;
                rightNode->right = NULL;
                node->right = rightNode;
                queue[qTail++] = rightNode;
            }
            free(tok);
        }
    }

    // 清理 remaining parts
    while (idx < tokens) { free(parts[idx]); idx++; }
    free(parts);
    free(queue);
    return root;
}

int* analyzeSpiritPaths(struct TreeNode* root, int threshold, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';
    // 找 } 后的逗号（树结构和 threshold 的分隔符）
    int commaPos = -1;
    int braceDepth = 0;
    for (int i = 0; i < len; i++) {
        if (line[i] == '{') braceDepth++;
        else if (line[i] == '}') braceDepth--;
        else if (line[i] == ',' && braceDepth == 0) {
            commaPos = i;
            break;
        }
    }
    char treeStr[MAX_LEN];
    char thresholdStr[MAX_LEN];
    if (commaPos == -1) {
        strcpy(treeStr, line);
        thresholdStr[0] = '\0';
    } else {
        strncpy(treeStr, line, commaPos);
        treeStr[commaPos] = '\0';
        strcpy(thresholdStr, line + commaPos + 1);
    }
    int threshold = atoi(thresholdStr);
    struct TreeNode* root = parseTree(treeStr);
    int returnSize = 0;
    int* result = analyzeSpiritPaths(root, threshold, &returnSize);
    printf("[%d,%d,%d]\n", result[0], result[1], result[2]);
    free(result);
    return 0;
}
