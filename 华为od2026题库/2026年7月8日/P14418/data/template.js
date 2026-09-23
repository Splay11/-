const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    const fragments = JSON.parse(line);
    const result = magicFragments(fragments);
    console.log(JSON.stringify(result));
});
