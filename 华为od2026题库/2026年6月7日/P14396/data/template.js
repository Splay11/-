// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
const line = fs.readFileSync(0, 'utf8').trim();

// 输入形如: 3,[2,1,3],[3,2,5],[10,20,30]
const parts = line.split(',[');
const n = parseInt(parts[0].trim());
const durationStr = '[' + parts[1];
const deadlineStr = '[' + parts[2];
const profitStr = '[' + parts[3];
const durationEnd = durationStr.indexOf(']') + 1;
const deadlineEnd = deadlineStr.indexOf(']') + 1;
const profitEnd = profitStr.indexOf(']') + 1;
const duration = JSON.parse(durationStr.substring(0, durationEnd));
const deadline = JSON.parse(deadlineStr.substring(0, deadlineEnd));
const profit = JSON.parse(profitStr.substring(0, profitEnd));

console.log(maximumProfit(duration, deadline, profit));
