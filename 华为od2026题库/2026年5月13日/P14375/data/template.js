// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如:
    // [["0","music","sports"],["1","music","reading"],["2","music"],["3","play","music","sports"]],[["0","1"],["1","2"],["2","3"],["0","3"]],"0",2
    let idx = 0;
    function parseArray(str, start) {
        let depth = 0;
        for (let i = start; i < str.length; i++) {
            if (str[i] === '[') depth++;
            else if (str[i] === ']') {
                depth--;
                if (depth === 0) {
                    return [JSON.parse(str.substring(start, i + 1)), i + 1];
                }
            }
        }
        return [[], str.length];
    }

    let [nodes, pos1] = parseArray(input, idx);
    let nextComma = input.indexOf(',', pos1);
    let [relations, pos2] = parseArray(input, nextComma + 1);
    let rest = input.substring(pos2).trim();
    if (rest.startsWith(',')) rest = rest.slice(1).trim();
    let parts = rest.split(',');
    let myId = JSON.parse(parts[0].trim());
    let maxHop = parseInt(parts[1].trim());

    console.log(JSON.stringify(queryFriends(nodes, relations, myId, maxHop)));
});
