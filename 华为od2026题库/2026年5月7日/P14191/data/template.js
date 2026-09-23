// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: ["display port status", "display device "],"display"
    const lastComma = input.lastIndexOf(',');
    const arrStr = input.substring(0, lastComma).trim();
    const prefixStr = input.substring(lastComma + 1).trim();
    const commands = JSON.parse(arrStr);
    const prefix = JSON.parse(prefixStr);
    console.log(JSON.stringify(FindNextKeywords(commands, prefix)));
});
