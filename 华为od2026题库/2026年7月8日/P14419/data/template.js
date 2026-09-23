const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 找顶层逗号切分三段 JSON
    let depth = 0;
    const splits = [];
    for (let i = 0; i < line.length; i++) {
        if (line[i] === '[') depth++;
        else if (line[i] === ']') depth--;
        else if (line[i] === ',' && depth === 0) splits.push(i);
    }

    const green = JSON.parse(line.substring(0, splits[0]));
    const carbon = JSON.parse(line.substring(splits[0] + 1, splits[1]));
    const edges = JSON.parse(line.substring(splits[1] + 1));

    const result = maxCarbonReduction(green, carbon, edges);
    console.log(result);
});
