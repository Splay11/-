// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [[1000, 800, 900],[1200, 900, 1100],[800, 600, 700]],2800
    const idx = input.lastIndexOf('],');
    const subArraysStr = input.substring(0, idx + 1).trim();
    const stationCapacityStr = input.substring(idx + 2).trim();
    const sub_arrays = JSON.parse(subArraysStr);
    const station_capacity = parseInt(stationCapacityStr);

    const result = predictGeneration(sub_arrays, station_capacity);
    console.log(JSON.stringify(result));
});
