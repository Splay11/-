const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    const arr = JSON.parse(line);
    const treeLevelOrder = arr[0];
    const frm = arr[1];
    const to = arr[2];

    console.log(minJumps(treeLevelOrder, frm, to));
});
