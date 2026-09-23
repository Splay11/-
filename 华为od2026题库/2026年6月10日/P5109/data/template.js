// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    const commaIndex = input.indexOf(',');
    const resA = JSON.parse(input.substring(0, commaIndex).trim());
    const resB = JSON.parse(input.substring(commaIndex + 1).trim());
    console.log(minDistinctAfterSwap(resA, resB));
});
