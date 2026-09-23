// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [7, 2, 5, 10, 8],2
    const commaIndex = input.lastIndexOf(',');
    const numsStr = input.substring(0, commaIndex).trim();
    const kStr = input.substring(commaIndex + 1).trim();
    const nums = JSON.parse(numsStr);
    const k = parseInt(kStr, 10);
    console.log(minimumLatency(nums, k));
});
