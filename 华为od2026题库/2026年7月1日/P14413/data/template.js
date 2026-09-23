// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: [-1,0,1,2,-1,-4],0
    const commaIndex = line.lastIndexOf(',');
    const numsStr = line.substring(0, commaIndex).trim();
    const targetStr = line.substring(commaIndex + 1).trim();
    const nums = JSON.parse(numsStr);
    const target = parseInt(targetStr);

    console.log(JSON.stringify(threeSumWithParity(nums, target)));
});
