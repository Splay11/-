// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 2,4,{80, 90, 95},{1,2,3}
    // 定位两个花括号对
    const lbrace1 = line.indexOf('{');
    const rbrace1 = line.indexOf('}');
    const lbrace2 = line.indexOf('{', rbrace1 + 1);
    const rbrace2 = line.indexOf('}', lbrace2 + 1);

    // 解析 N,T (第一个 { 之前的部分)
    const header = line.substring(0, lbrace1);
    const firstComma = header.indexOf(',');
    const N = parseInt(header.substring(0, firstComma));
    const T = parseInt(header.substring(firstComma + 1));

    // 解析 accuracy 数组
    const accStr = line.substring(lbrace1, rbrace1 + 1);
    const accuracy = accStr.substring(1, accStr.length - 1).split(',').map(x => parseInt(x.trim()));

    // 解析 latency 数组
    const latStr = line.substring(lbrace2, rbrace2 + 1);
    const latency = latStr.substring(1, latStr.length - 1).split(',').map(x => parseInt(x.trim()));

    console.log(maxTotalAccuracy(N, T, accuracy, latency));
});
