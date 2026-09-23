// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    const firstComma = line.indexOf(',');
    const n = parseInt(line.substring(0, firstComma).trim());
    const numsStr = line.substring(firstComma + 1).trim();
    const nums = JSON.parse(numsStr);
    console.log(minSplitRangeSum(nums));
});
