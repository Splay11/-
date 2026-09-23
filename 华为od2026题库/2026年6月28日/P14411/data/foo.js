var analyzeSpiritPaths = function(root, threshold) {
    var INT_MIN_VAL = -2147483648;
    if (root === null || root === undefined) {
        return [INT_MIN_VAL, 0, 0];
    }

    var max_val = INT_MIN_VAL;
    var count = 0;
    var has_ge = 0;

    function dfs(node, cur_sum, prev_neg) {
        var is_neg = node.val < 0;
        // 连续两个负结点，当前路径非法
        if (is_neg && prev_neg) return;

        var new_sum = cur_sum + node.val;
        var is_leaf = node.left === null && node.right === null;

        if (is_leaf) {
            max_val = Math.max(max_val, new_sum);
            count++;
            if (new_sum >= threshold) has_ge = 1;
            return;
        }

        if (node.left !== null) dfs(node.left, new_sum, is_neg);
        if (node.right !== null) dfs(node.right, new_sum, is_neg);
    }

    dfs(root, 0, false);

    if (count === 0) max_val = INT_MIN_VAL;
    return [max_val, has_ge, count];
};
