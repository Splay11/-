// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 5,[1],[[1,0,0],[1,2,0]]
    const firstComma = line.indexOf(',');
    const n = parseInt(line.substring(0, firstComma).trim());
    const rest = line.substring(firstComma + 1).trim();

    // 找到 sources 数组部分
    const firstBracket = rest.indexOf('[');
    const secondBracket = rest.indexOf(']');
    const sourcesStr = rest.substring(firstBracket, secondBracket + 1);
    const sources = JSON.parse(sourcesStr);

    // pipes 数组部分
    const startPipes = rest.indexOf('[', secondBracket + 1);
    const pipesStr = rest.substring(startPipes);
    const pipes = JSON.parse(pipesStr);

    console.log(JSON.stringify(findIsolatedStations(n, sources, pipes)));
});
