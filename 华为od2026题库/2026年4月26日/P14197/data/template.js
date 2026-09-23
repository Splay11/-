// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    const portRates = JSON.parse(line);
    console.log(JSON.stringify(StatPortRates(portRates)));
});
