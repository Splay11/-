// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: "ABC","BAC",A
    const parts = input.split(',');
    const preorderStr = parts[0].trim();
    const inorderStr = parts[1].trim();
    const beDeletedNode = parts[2].trim();

    // 去除多余的引号
    const cleanPreorder = preorderStr.replace(/^"|"$/g, '');
    const cleanInorder = inorderStr.replace(/^"|"$/g, '');
    const cleanDelete = beDeletedNode.replace(/^"|"$/g, '');

    console.log('"' + buildAfterDelete(cleanPreorder, cleanInorder, cleanDelete) + '"');
});
