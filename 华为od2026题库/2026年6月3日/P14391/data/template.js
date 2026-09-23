// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
// 输入形如: ["add","add","query","add","query"],[1,2,3,3,6]
const input = fs.readFileSync(0, 'utf8').trim();
const commaIndex = input.indexOf('],[');
const opsStr = input.substring(0, commaIndex + 1);
const valsStr = input.substring(commaIndex + 2);
const ops = JSON.parse(opsStr);
const vals = JSON.parse(valsStr);
console.log(JSON.stringify(monitor(ops, vals)));
