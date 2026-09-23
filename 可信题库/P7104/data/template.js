const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').replace(/\s+$/, '');
    const lines = raw ? raw.split('\n') : [];
    const n = lines.length ? parseInt(lines[0], 10) : 0;
    const ops = lines.length > 1 ? JSON.parse(lines[1]) : [];
    console.log(maxLinkLoad(n, ops));
});
