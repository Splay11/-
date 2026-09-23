// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 8,[20,25,30,28,35,40,42,25],3,10
    // 解析第一个参数 n
    let idx1 = line.indexOf(',');
    const nStr = line.substring(0, idx1).trim();
    const n = parseInt(nStr, 10);

    // 找到 temperatures 数组部分
    let idxStartArr = line.indexOf('[', idx1);
    let idxEndArr = line.indexOf(']', idxStartArr);
    const arrStr = line.substring(idxStartArr, idxEndArr + 1);
    const temperatures = JSON.parse(arrStr);

    // 剩余部分解析 k 和 t
    const rest = line.substring(idxEndArr + 1).trim();
    const parts = rest.split(',').filter(s => s.length > 0);
    const k = parseInt(parts[0], 10);
    const t = parseInt(parts[1], 10);

    const result = analyzeTemperatureData(temperatures, k, t);
    console.log('[' + result.join(',') + ']');
});
