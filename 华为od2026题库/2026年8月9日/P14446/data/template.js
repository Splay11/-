// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析输入："lights",t
    const start = line.indexOf('"');
    const end = line.indexOf('"', start + 1);
    const lights = line.substring(start + 1, end);

    // 逗号后的整数
    const comma = line.indexOf(',', end);
    const t = parseInt(line.substring(comma + 1).trim());

    // 调用用户代码
    const result = lightStripTransform(lights, t);
    console.log('"' + result + '"');
});
