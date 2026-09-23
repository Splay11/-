// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: {10,-5,20,#,8,-6,15},40
    const lastComma = input.lastIndexOf(',');
    const treeStr = input.substring(0, lastComma).trim();
    const threshold = parseInt(input.substring(lastComma + 1).trim(), 10);

    function buildTree(data) {
        if (!data || data === '{}' || data === '{#}') return null;
        const content = data.slice(1, -1).trim();
        if (!content) return null;
        const vals = content.split(',').map(s => s.trim());
        if (vals.length === 0 || vals[0] === '#' || vals[0] === '') return null;
        const root = { val: parseInt(vals[0], 10), left: null, right: null };
        const queue = [root];
        let idx = 1;
        while (queue.length > 0 && idx < vals.length) {
            const node = queue.shift();
            // left child
            if (idx < vals.length) {
                const v = vals[idx++];
                if (v !== '#' && v !== '') {
                    node.left = { val: parseInt(v, 10), left: null, right: null };
                    queue.push(node.left);
                }
            }
            // right child
            if (idx < vals.length) {
                const v = vals[idx++];
                if (v !== '#' && v !== '') {
                    node.right = { val: parseInt(v, 10), left: null, right: null };
                    queue.push(node.right);
                }
            }
        }
        return root;
    }

    const root = buildTree(treeStr);
    const result = analyzeSpiritPaths(root, threshold);
    console.log(JSON.stringify(result));
});
