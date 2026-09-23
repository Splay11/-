// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [10,25,3,15,8],16
    const splitIndex = line.lastIndexOf(',');
    const numsStr = line.substring(0, splitIndex).trim();
    const baseStr = line.substring(splitIndex + 1).trim();
    const nums = JSON.parse(numsStr);
    const base = parseInt(baseStr);
    console.log(JSON.stringify(sortConvertedNums(nums, base)));
});
