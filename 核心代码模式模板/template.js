// LeetCode 核心代码模式 - JS 输入输出模板
// 读取整行输入
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on('line', (line) => {
  line = line.trim();

  // 解析输入：month, employees, birthdays
  const firstComma = line.indexOf(',');
  const month = parseInt(line.substring(0, firstComma).trim());

  const rest = line.substring(firstComma + 1).trim();
  const split = rest.indexOf('],[');
  const employeesStr = rest.substring(0, split + 1);
  const birthdaysStr = rest.substring(split + 2);

  const employees = JSON.parse(employeesStr);
  const birthdays = JSON.parse(birthdaysStr);

  // 调用用户代码
  const solution = new Solution();
  console.log(solution.countBirthdayGifts(month, employees, birthdays));

  rl.close();
});
