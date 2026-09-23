// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: "8:00 23:30"
    const timeRange = input.slice(1, -1); // 去掉前后双引号
    console.log(JSON.stringify(timeClassification(timeRange)));
});
