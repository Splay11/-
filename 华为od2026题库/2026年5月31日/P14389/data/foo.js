/**
 * @param {string[]} nodes 序列表示的企业部门节点
 * @return {number} 最大管理层级深度
 */
var maxDepth = function(nodes) {
    // 空树或根节点为空
    if (!nodes || nodes.length === 0 || nodes[0] === '#') {
        return 0;
    }

    // 队列存储每个存在节点的深度
    var queue = [1];
    var ans = 1;
    var index = 1;  // 下一个要处理的子节点下标

    var head = 0;
    while (head < queue.length) {
        var depth = queue[head++];

        // 处理左子节点
        if (index < nodes.length) {
            if (nodes[index] !== '#') {
                queue.push(depth + 1);
                ans = Math.max(ans, depth + 1);
            }
            index++;
        }

        // 处理右子节点
        if (index < nodes.length) {
            if (nodes[index] !== '#') {
                queue.push(depth + 1);
                ans = Math.max(ans, depth + 1);
            }
            index++;
        }
    }

    return ans;
};
