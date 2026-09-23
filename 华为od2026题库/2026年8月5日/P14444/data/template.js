// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析输入: "CIDR",N,[requirements]
    // 找第一个顶层逗号
    let bracketDepth = 0, inString = false, comma1 = -1;
    for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === '"') {
            inString = !inString;
        } else if (!inString) {
            if (c === '[') bracketDepth++;
            else if (c === ']') bracketDepth--;
            else if (c === ',' && bracketDepth === 0) {
                comma1 = i;
                break;
            }
        }
    }

    const cidrPart = line.substring(0, comma1);
    const cidr = parseQuotedString(cidrPart);

    const rest = line.substring(comma1 + 1);

    // 第二个顶层逗号
    bracketDepth = 0;
    inString = false;
    let comma2 = -1;
    for (let i = 0; i < rest.length; i++) {
        const c = rest[i];
        if (c === '"') {
            inString = !inString;
        } else if (!inString) {
            if (c === '[') bracketDepth++;
            else if (c === ']') bracketDepth--;
            else if (c === ',' && bracketDepth === 0) {
                comma2 = i;
                break;
            }
        }
    }

    const n = parseInt(rest.substring(0, comma2).trim());
    const requirements = JSON.parse(rest.substring(comma2 + 1).trim());

    // 调用用户代码
    const result = allocateSubnets(cidr, n, requirements);
    console.log("[" + result.map(r => '"' + r + '"').join(",") + "]");
});

/**
 * 提取引号内的字符串
 */
function parseQuotedString(s) {
    const start = s.indexOf('"');
    const end = s.lastIndexOf('"');
    if (start === -1 || end === -1 || start >= end) return "";
    return s.substring(start + 1, end);
}
