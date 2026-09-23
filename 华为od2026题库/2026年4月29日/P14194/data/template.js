// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    const logs = JSON.parse(input);
    const result = findAnomalyLogs(logs);
    console.log(result.length === 0 ? 'NONE' : JSON.stringify(result));
});
