// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析三个逗号分隔的值：capacity,efficiency,scene
    const parts = line.split(',');
    const capacity = parseFloat(parts[0].trim());
    const efficiency = parseFloat(parts[1].trim());
    const scene = parseInt(parts[2].trim(), 10);

    // 调用用户代码
    console.log(calculateRange(capacity, efficiency, scene));
});
