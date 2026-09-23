// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: [100,200,150,50,300],[[0,1],[1,2],[3,4]]
    const commaIdx = line.indexOf('],');
    const loadsStr = line.substring(0, commaIdx + 1);
    const edgesStr = line.substring(commaIdx + 2);
    const loads = JSON.parse(loadsStr);
    const edges = JSON.parse(edgesStr);

    console.log(maxZoneImbalance(loads, edges));
});
