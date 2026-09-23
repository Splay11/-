// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
const input = fs.readFileSync(0, 'utf8').trim();

// 输入形如: [1,2,3,4,5,6,7],[0,1,1,2,2,3,0],2
const firstBracketEnd = input.indexOf(']');
const fileIdsStr = input.substring(0, firstBracketEnd + 1);
const rest1 = input.substring(firstBracketEnd + 2);
const secondBracketEnd = rest1.indexOf(']');
const parentIdsStr = rest1.substring(0, secondBracketEnd + 1);
const rest2 = rest1.substring(secondBracketEnd + 2);
const targetId = parseInt(rest2.replace(/,/g, '').trim(), 10);

const fileIds = JSON.parse(fileIdsStr);
const parentIds = JSON.parse(parentIdsStr);

console.log(JSON.stringify(getLoadedFileIds(fileIds, parentIds, targetId)));
