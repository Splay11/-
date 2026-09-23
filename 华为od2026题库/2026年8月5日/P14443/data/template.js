// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析输入：n,"channels"
    const firstComma = line.indexOf(',');
    const n = parseInt(line.substring(0, firstComma).trim());
    const rest = line.substring(firstComma + 1).trim();
    const channels = rest.replace(/"/g, '');

    // 调用用户代码
    console.log(mergeBroadcastChannels(n, channels));
});
