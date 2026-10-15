const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:1000,height:900},deviceScaleFactor:2});
  await p.route(/cdnjs/,r=>r.abort());
  await p.goto('file://' + require('path').resolve(process.argv[2]));   // usage: node shots.js path/to/dist/code/index.html
  await p.evaluate(()=>{document.querySelectorAll('.tab-panel').forEach(x=>x.hidden=false)});
  const ids=await p.$$eval('.item', els=>els.filter(e=>e.querySelector('svg')).map(e=>e.id));
  for(const id of ids){ const el=await p.$(`#${id} svg`); await el.screenshot({path:id+'.png'}); const bb=await el.boundingBox(); console.log(id,Math.round(bb.width),Math.round(bb.height)); }
  await b.close();
})();
