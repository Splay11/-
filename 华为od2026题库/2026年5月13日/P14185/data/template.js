// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: "abc123EFEDG34aadD78er",2
    const commaIndex = line.lastIndexOf(',');
    const inputStr = JSON.parse(line.substring(0, commaIndex).trim());
    const inputDivisor = parseInt(line.substring(commaIndex + 1).trim(), 10);
    console.log(getMaxDivisibleNumber(inputStr, inputDivisor));
});
