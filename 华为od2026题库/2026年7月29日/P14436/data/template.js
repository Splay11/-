// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析 "n,[a1,a2,...,an]"
    const comma = line.indexOf(',');
    const n = parseInt(line.substring(0, comma).trim());
    const arrStr = line.substring(comma + 1).trim();

    let energies;
    if (arrStr === '[]') {
        energies = [];
    } else {
        energies = JSON.parse(arrStr);
    }

    const result = energyCollision(energies);
    console.log(JSON.stringify(result));
});
