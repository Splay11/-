// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 找到顶层逗号分隔 data 和 interval
    let bracket = 0;
    let commaPos = -1;
    for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === '[') bracket++;
        else if (c === ']') bracket--;
        else if (c === ',' && bracket === 0) {
            commaPos = i;
            break;
        }
    }

    const data = JSON.parse(line.substring(0, commaPos));
    const interval = parseInt(line.substring(commaPos + 1));

    // 调用用户代码
    const result = getMaxValues(data, interval);
    console.log(JSON.stringify(result).replace(/\s/g, ''));
});
