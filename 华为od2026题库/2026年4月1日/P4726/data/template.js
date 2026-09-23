const fs = require('fs');
const line = fs.readFileSync(0, 'utf8').trim();

// 找到第一个 ], 后面的逗号位置
// 格式: [[...],[...]],maxDiff
let bracketDepth = 0;
let splitPos = -1;
for (let i = 0; i < line.length; i++) {
    if (line[i] === '[') bracketDepth++;
    else if (line[i] === ']') bracketDepth--;
    else if (line[i] === ',' && bracketDepth === 0) {
        splitPos = i;
        break;
    }
}

const gridStr = line.substring(0, splitPos);
const maxDiff = parseInt(line.substring(splitPos + 1).trim(), 10);
const grid = JSON.parse(gridStr);

const result = countHikingPaths(grid, maxDiff);
console.log(result);
