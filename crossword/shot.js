const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const f of ['puzzle','answer']){const p=await b.newPage({viewport:{width:1080,height:1000},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/'+f+'.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
console.log(f,await p.evaluate(()=>document.fonts.check('40px "Tiro Devanagari Marathi"','क')));
await p.locator('.page').screenshot({path:'/home/user/my-first-app/marathi-shabdakhel-1-'+(f==='puzzle'?'kode':'uttar')+'.png'});}
await b.close();})();
