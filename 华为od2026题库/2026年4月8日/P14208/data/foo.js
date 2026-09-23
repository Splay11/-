/**
 * @param {number} month 要发放礼物的月份
 * @param {string[]} employees 员工姓名列表
 * @param {string[]} birthdays 对应的员工生日日期列表
 * @return {number} 该月份要准备的礼品个数
 */
var countBirthdayGifts = function(month, employees, birthdays) {
    // 用 object 记录每个员工最后一次录入的生日月份
    const lastMonth = {};
    for (let i = 0; i < employees.length; i++) {
        const m = parseInt(birthdays[i].split('/')[1], 10);
        lastMonth[employees[i]] = m;
    }
    // 统计生日月份等于目标月份的员工数
    let cnt = 0;
    for (const m of Object.values(lastMonth)) {
        if (m === month) cnt++;
    }
    return cnt;
};
