const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+__dirname+'/pages.html');await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:'new_pages.pdf',preferCSSPageSize:true,printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});await b.close();})();
