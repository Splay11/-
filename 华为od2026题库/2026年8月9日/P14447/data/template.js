// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 顶层逗号查找（不在括号内的逗号）
    function findTopLevelComma(s) {
        let bracket = 0;
        for (let i = 0; i < s.length; i++) {
            const c = s[i];
            if (c === '[') bracket++;
            else if (c === ']') bracket--;
            else if (c === ',' && bracket === 0) return i;
        }
        return -1;
    }

    // 解析 count
    const comma1 = findTopLevelComma(line);
    const count = parseInt(line.substring(0, comma1).trim());

    // 解析 total
    const rest1 = line.substring(comma1 + 1).trim();
    const comma2 = findTopLevelComma(rest1);
    const total = parseInt(rest1.substring(0, comma2).trim());

    // 解析数组部分
    const rest2 = rest1.substring(comma2 + 1).trim();
    const split = rest2.indexOf('],[');
    const valuesStr = rest2.substring(0, split + 1);
    const decaysStr = '[' + rest2.substring(split + 3);

    const values = JSON.parse(valuesStr);
    const decays = JSON.parse(decaysStr);

    // 调用用户代码
    console.log(maxMushroomValue(count, total, values, decays));
});
