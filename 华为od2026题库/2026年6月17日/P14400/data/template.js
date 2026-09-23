// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: "abaabacbda",3
    const firstComma = input.lastIndexOf(',');
    const sPart = input.substring(0, firstComma).trim();
    const nPart = input.substring(firstComma + 1).trim();
    const s = JSON.parse(sPart);
    const n = parseInt(nPart, 10);

    console.log(JSON.stringify(processChunks(s, n)));
});
