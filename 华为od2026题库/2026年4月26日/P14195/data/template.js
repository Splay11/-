// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: ["user","auth","database","api"],[["user","auth"],["auth","database"],["api","database"]]
    const splitIdx = line.indexOf('],[');
    const modulesStr = line.substring(0, splitIdx + 1);
    const dependenciesStr = line.substring(splitIdx + 2);
    const modules = JSON.parse(modulesStr);
    const dependencies = JSON.parse(dependenciesStr);

    console.log(JSON.stringify(allBuildOrders(modules, dependencies)));
});
