const fs = require('fs');

// 读取全部输入
const input = fs.readFileSync(0, 'utf8').trim();
let pos = 0;

// 跳过空白
function skipSpaces() {
    while (pos < input.length && input[pos] === ' ') pos++;
}

// 解析引号字符串
function parseString() {
    if (input[pos] !== '"') throw new Error('Expected "');
    pos++;
    let result = '';
    while (pos < input.length && input[pos] !== '"') {
        if (input[pos] === '\\' && pos + 1 < input.length) {
            pos++;
            result += input[pos];
        } else {
            result += input[pos];
        }
        pos++;
    }
    pos++; // 跳过闭合引号
    return result;
}

// 解析字符串数组
function parseStringArray() {
    if (input[pos] !== '[') throw new Error('Expected [');
    pos++;
    skipSpaces();
    let result = [];
    if (input[pos] === ']') { pos++; return result; }
    while (true) {
        skipSpaces();
        result.push(parseString());
        skipSpaces();
        if (input[pos] === ']') { pos++; break; }
        if (input[pos] === ',') { pos++; }
    }
    return result;
}

// 解析整数数组
function parseIntArray() {
    if (input[pos] !== '[') throw new Error('Expected [');
    pos++;
    skipSpaces();
    let result = [];
    if (input[pos] === ']') { pos++; return result; }
    while (true) {
        skipSpaces();
        let start = pos;
        if (input[pos] === '-') pos++;
        while (pos < input.length && input[pos] >= '0' && input[pos] <= '9') pos++;
        result.push(parseInt(input.substring(start, pos), 10));
        skipSpaces();
        if (input[pos] === ']') { pos++; break; }
        if (input[pos] === ',') { pos++; }
    }
    return result;
}

// 解析输入
const target = parseString();
skipSpaces();
if (input[pos] === ',') pos++;
skipSpaces();
const files = parseStringArray();
skipSpaces();
if (input[pos] === ',') pos++;
skipSpaces();
const sizes = parseIntArray();

// 调用用户代码并输出（格式与题面样例一致：逗号后带空格）
const result = findMaxOccupiedPaths(target, files, sizes);
const output = '[' + result.map(s => '"' + s + '"').join(', ') + ']';
console.log(output);
