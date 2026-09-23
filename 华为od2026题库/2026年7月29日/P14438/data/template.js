// 读取整行输入
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

rl.on('line', function(line) {
    // 解析 R
    let c1 = line.indexOf(',');
    let R = parseInt(line.substring(0, c1).trim());

    // 解析 G
    let rest1 = line.substring(c1 + 1);
    let c2 = rest1.indexOf(',');
    let G = parseInt(rest1.substring(0, c2).trim());

    // 剩余部分: [E,S,W,N],[0,1,3,6]
    let rest2 = rest1.substring(c2 + 1);
    let split = rest2.indexOf('],[');
    let dirsStr = rest2.substring(1, split);        // E,S,W,N
    let timesStr = rest2.substring(split + 3);       // 0,1,3,6]

    // 去掉 timesStr 末尾的 ']'
    if (timesStr.endsWith(']')) {
        timesStr = timesStr.substring(0, timesStr.length - 1);
    }

    // 解析方向列表
    let directions = dirsStr.split(',').filter(s => s.trim() !== '').map(s => s.trim());

    // 解析到达时间列表
    let arrivalTimes = timesStr.split(',').filter(s => s.trim() !== '').map(s => parseInt(s.trim()));

    // 调用用户代码
    let result = intersectionWaitingTime(R, G, directions, arrivalTimes);
    console.log('[' + result[0] + ',' + result[1] + ']');
});
