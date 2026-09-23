// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
const input = fs.readFileSync(0, 'utf8').trim();

// 输入格式:
// [4,3,5],[(1,2),(1,3),(2,4)],[(1,2),(2,3),(1,3)],[(1,2),(3,4)]
const commaIndex = input.indexOf('],');
const resourceStr = input.substring(0, commaIndex + 1).trim();
const resourceCount = JSON.parse(resourceStr);

const rest = input.substring(commaIndex + 2).trim();
const conflictParts = [];
let i = 0, j = 0;
while (i < rest.length) {
    if (rest[i] === '[') {
        let depth = 0;
        for (j = i; j < rest.length; j++) {
            if (rest[j] === '[') depth++;
            else if (rest[j] === ']') {
                depth--;
                if (depth === 0) break;
            }
        }
        conflictParts.push(rest.substring(i, j + 1));
        i = j + 1;
        if (i < rest.length && rest[i] === ',') i++;
    } else {
        i++;
    }
}

const conflicts = conflictParts.map(str => {
    if (str === '[]') return [];
    str = str.replace(/^\[\(/, '[[').replace(/\)\,$/, ']]').replace(/\),\(/g, '],[').replace(/\)\]$/, ']]').replace(/\(/g, '[').replace(/\)/g, ']');
    try {
        return JSON.parse(str);
    } catch {
        // fallback
        const pairs = str.slice(1, -1).split('),(').map(p => p.replace(/\(|\)/g,''));
        return pairs.filter(p=>p.trim().length>0).map(p=>p.split(',').map(Number));
    }
});

const ans = canIsolateWithTwoPools(resourceCount, conflicts);
console.log(JSON.stringify(ans));
