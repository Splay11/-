// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const ip = fs.readFileSync(0, 'utf8').trim();
    console.log(classifyIPv4(ip));
});
