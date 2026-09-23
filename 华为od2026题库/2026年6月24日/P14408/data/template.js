// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 4,2,[5,1,3,4],[[1,2],[2,3]]
    let parts = input.split(',');
    const n = parseInt(parts[0].trim());
    const k = parseInt(parts[1].trim());

    // 找到第三部分的数组起始 [
    const weightsStart = input.indexOf('[', input.indexOf(',') + 1);
    const weightsEnd = input.indexOf(']', weightsStart);
    const weightsStr = input.substring(weightsStart, weightsEnd + 1);
    const weights = JSON.parse(weightsStr);

    // 第四部分 conflicts 数组
    const conflictsStart = input.indexOf('[', weightsEnd + 1);
    const conflictsStr = input.substring(conflictsStart);
    const conflicts = JSON.parse(conflictsStr);

    const result = selectMaxWeightPolicies(n, k, weights, conflicts);
    console.log(JSON.stringify(result));
});
