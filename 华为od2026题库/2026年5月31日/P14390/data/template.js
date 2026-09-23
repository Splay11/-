// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [1,2,3,4,5],5,3 或 [1,2,3,4,5],3
    const closeBracket = line.indexOf(']');
    const nums = JSON.parse(line.substring(0, closeBracket + 1));
    const rest = line.substring(closeBracket + 2).split(','); // 跳过 "],"
    const n = rest.length === 1 ? nums.length : parseInt(rest[0]);
    const k = parseInt(rest[rest.length - 1]);
    console.log(maxEnergyDivisibleByK(nums, n, k));
});
