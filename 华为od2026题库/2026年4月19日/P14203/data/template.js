// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入使用单引号，替换为双引号以便 JSON.parse
    const fixed = input.replace(/'/g, '"');
    const arr = JSON.parse(fixed);
    console.log(networkPlanning(arr));
});
