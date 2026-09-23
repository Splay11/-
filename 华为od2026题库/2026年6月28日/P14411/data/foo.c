#include <stdbool.h>
#include <stdlib.h>

#define INT_MIN_VAL (-2147483648)

// struct TreeNode 由 template.c 定义

static int max_val, count, has_ge;

static void dfs(struct TreeNode* node, long long cur_sum, bool prev_neg, int threshold) {
    bool is_neg = node->val < 0;
    // 连续两个负结点，当前路径非法
    if (is_neg && prev_neg) return;

    long long new_sum = cur_sum + node->val;
    bool is_leaf = (node->left == NULL && node->right == NULL);

    if (is_leaf) {
        if ((int)new_sum > max_val) max_val = (int)new_sum;
        count++;
        if (new_sum >= threshold) has_ge = 1;
        return;
    }

    if (node->left != NULL) dfs(node->left, new_sum, is_neg, threshold);
    if (node->right != NULL) dfs(node->right, new_sum, is_neg, threshold);
}

int* analyzeSpiritPaths(struct TreeNode* root, int threshold, int* returnSize) {
    int* res = (int*)malloc(3 * sizeof(int));
    *returnSize = 3;

    if (root == NULL) {
        res[0] = INT_MIN_VAL;
        res[1] = 0;
        res[2] = 0;
        return res;
    }

    max_val = INT_MIN_VAL;
    count = 0;
    has_ge = 0;

    dfs(root, 0LL, false, threshold);

    if (count == 0) max_val = INT_MIN_VAL;
    res[0] = max_val;
    res[1] = has_ge;
    res[2] = count;
    return res;
}
