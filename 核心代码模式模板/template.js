// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // === 以下需根据具体题目修改解析逻辑 ===
    const firstComma = line.indexOf(',');
    const month = parseInt(line.substring(0, firstComma).trim());
    const rest = line.substring(firstComma + 1).trim();
    const split = rest.indexOf('],[');
    const employeesStr = rest.substring(0, split + 1);
    const birthdaysStr = rest.substring(split + 2);
    const employees = JSON.parse(employeesStr);
    const birthdays = JSON.parse(birthdaysStr);

    // 调用用户代码
    console.log(countBirthdayGifts(month, employees, birthdays));
});