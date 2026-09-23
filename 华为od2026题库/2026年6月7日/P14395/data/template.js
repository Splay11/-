// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
const input = fs.readFileSync(0, 'utf8').trim();
const ips = JSON.parse(input);
console.log(JSON.stringify(filterValidAClassIPs(ips)));
