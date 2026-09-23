// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [5,4,0,3],1
    const commaIndex = line.lastIndexOf(',');
    const arrStr = line.substring(0, commaIndex).trim();
    const numStr = line.substring(commaIndex + 1).trim();
    const goodProceeTime = JSON.parse(arrStr);
    const optimize = parseInt(numStr);
    console.log(minProcessTime(goodProceeTime, optimize));
});
