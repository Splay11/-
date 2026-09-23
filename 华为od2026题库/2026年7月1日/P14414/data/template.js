// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: N,K,M,[a1,a2,a3,...,aN]
    const parts = line.split(',');
    const N = parseInt(parts[0].trim());
    const K = parseInt(parts[1].trim());
    const M = parseInt(parts[2].trim());
    const arrStr = line.substring(line.indexOf('['));
    const A = JSON.parse(arrStr);
    console.log(maxSpiritPower(N, K, M, A));
});
