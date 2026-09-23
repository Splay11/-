// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 将整行包成 JSON 数组 [n, m, files, cost] 后解析
    const arr = JSON.parse('[' + line + ']');
    const n = arr[0], m = arr[1], files = arr[2], cost = arr[3];

    // 调用用户代码
    console.log(minCost(n, m, files, cost));
});
