// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 5,["Alice", "Bob", ...],["1985/5/10", ...]
    const firstComma = line.indexOf(',');
    const month = parseInt(line.substring(0, firstComma).trim());
    const rest = line.substring(firstComma + 1).trim();

    // 找到两个数组
    const arrStart1 = rest.indexOf('[');
    const arrEnd1 = rest.indexOf(']');
    const employeesStr = rest.substring(arrStart1, arrEnd1 + 1);
    const afterFirst = rest.substring(arrEnd1 + 1).trim();
    const arrStart2 = afterFirst.indexOf('[');
    const arrEnd2 = afterFirst.lastIndexOf(']');
    const birthdaysStr = afterFirst.substring(arrStart2, arrEnd2 + 1);

    const employees = JSON.parse(employeesStr);
    const birthdays = JSON.parse(birthdaysStr);

    console.log(countBirthdayGifts(month, employees, birthdays));
});
