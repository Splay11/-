// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: [1,2,4],2
    const commaIndex = line.lastIndexOf(',');
    const timestampsStr = line.substring(0, commaIndex).trim();
    const minIntervalStr = line.substring(commaIndex + 1).trim();

    const timestamps = JSON.parse(timestampsStr);
    const minInterval = parseInt(minIntervalStr, 10);

    console.log(countValidPlans(timestamps, minInterval));
});
