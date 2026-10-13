(function(){
  'use strict';

  const W=1240,H=1754,M=78,FOOT=105,CONTENT_W=W-M*2;
  const LANG={
    ru:{report:'SEO-аудит сайта',issues:'Ключевые проблемы',noIssues:'Критичных проблем в базовых технических проверках не найдено.',plan:'Приоритетный план работ',checks:'Результаты базовых проверок',generated:'Отчёт сформирован',score:'SEO SCORE',page:'Страница',fix:'исправить',generating:'Формируем PDF…'},
    en:{report:'Website SEO audit',issues:'Key issues',noIssues:'No critical issues were found in the core technical checks.',plan:'Priority action plan',checks:'Core check results',generated:'Report generated',score:'SEO SCORE',page:'Page',fix:'fix',generating:'Generating PDF…'},
    ka:{report:'საიტის SEO აუდიტი',issues:'ძირითადი პრობლემები',noIssues:'ძირითად ტექნიკურ შემოწმებებში კრიტიკული პრობლემა არ აღმოჩნდა.',plan:'პრიორიტეტული სამოქმედო გეგმა',checks:'ძირითადი შემოწმებების შედეგები',generated:'ანგარიში შექმნილია',score:'SEO SCORE',page:'გვერდი',fix:'შესასწორებელია',generating:'PDF მზადდება…'}
  };

  function lang(){const l=(document.documentElement.lang||'ru').toLowerCase();return LANG[l]||LANG.ru}
  function locale(){const l=(document.documentElement.lang||'ru').toLowerCase();return l==='ka'?'ka-GE':l==='en'?'en-GB':'ru-RU'}
  function audit(){try{return currentAudit||null}catch(_){return null}}
  function issueList(a){try{return issues(a)||[]}catch(_){return (a?.checks||[]).filter(c=>Number(c.points)<Number(c.max))}}
  function planList(a){try{return planItems(a)||[]}catch(_){return []}}
  function label(c){try{return labelFor(c)}catch(_){return c?.label||c?.id||''}}
  function detail(c){try{return detailFor(c)}catch(_){return c?.detail||''}}
  function safeName(v){return String(v||'site').replace(/[^a-z0-9а-яё.-]+/gi,'-').replace(/-+/g,'-').replace(/^-|-$/g,'')||'site'}

  function rr(ctx,x,y,w,h,r){
    r=Math.min(r,w/2,h/2);ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();
  }
  function lines(ctx,text,maxWidth){
    const out=[];for(const para of String(text??'').split(/\n/)){const words=para.split(/\s+/).filter(Boolean);if(!words.length){out.push('');continue}let line='';for(const word of words){const test=line?line+' '+word:word;if(ctx.measureText(test).width<=maxWidth){line=test;continue}if(line)out.push(line);if(ctx.measureText(word).width<=maxWidth){line=word;continue}let chunk='';for(const ch of word){const t=chunk+ch;if(ctx.measureText(t).width>maxWidth&&chunk){out.push(chunk);chunk=ch}else chunk=t}line=chunk}if(line)out.push(line)}return out;
  }
  function text(ctx,str,x,y,maxWidth,lineHeight){for(const ln of lines(ctx,str,maxWidth)){ctx.fillText(ln,x,y);y+=lineHeight}return y}

  function makePage(){
    const canvas=document.createElement('canvas');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');ctx.fillStyle='#ffffff';ctx.fillRect(0,0,W,H);ctx.textBaseline='top';
    ctx.fillStyle='#f2f7fc';rr(ctx,M,48,64,64,18);ctx.fill();ctx.fillStyle='#9aa9b8';ctx.font='900 35px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText('B',M+32,60);ctx.textAlign='left';
    ctx.fillStyle='#0d427b';ctx.font='900 34px system-ui,sans-serif';ctx.fillText('BEQSON',M+88,50);ctx.fillStyle='#607991';ctx.font='700 12px system-ui,sans-serif';ctx.letterSpacing='3px';ctx.fillText('D I G I T A L   S T U D I O',M+89,93);ctx.letterSpacing='0px';
    ctx.fillStyle='#31a9ff';ctx.fillRect(M,132,CONTENT_W,5);
    return {canvas,ctx,y:170};
  }

  function sectionTitle(state,title){
    const {ctx}=state;ctx.fillStyle='#173a5c';ctx.font='900 27px system-ui,sans-serif';state.y=text(ctx,title,M,state.y,CONTENT_W,34)+12;
  }
  function pageHas(state,h){return state.y+h<=H-FOOT}
  function addPage(pages){const p=makePage();pages.push(p);return p}
  function ensure(stateRef,pages,h,repeatTitle){
    if(pageHas(stateRef.value,h))return;
    stateRef.value=addPage(pages);if(repeatTitle)sectionTitle(stateRef.value,repeatTitle);
  }

  function drawHero(state,a,T){
    const ctx=state.ctx,site=a.final_url||a.url||'',host=a.host||site,date=new Date().toLocaleDateString(locale(),{day:'2-digit',month:'long',year:'numeric'});
    ctx.fillStyle='#61758a';ctx.font='600 16px system-ui,sans-serif';ctx.textAlign='right';ctx.fillText(T.report,W-M,55);ctx.fillText(date,W-M,80);ctx.textAlign='left';
    ctx.fillStyle='#143755';ctx.font='900 47px system-ui,sans-serif';let yy=text(ctx,T.report,M,190,720,55);ctx.fillStyle='#1478d8';ctx.font='900 31px system-ui,sans-serif';yy=text(ctx,host,M,yy+6,720,39);ctx.fillStyle='#6f8295';ctx.font='500 16px system-ui,sans-serif';text(ctx,site,M,yy+2,720,23);
    const cx=W-202,cy=260;ctx.lineWidth=18;ctx.strokeStyle='#35aaff';ctx.beginPath();ctx.arc(cx,cy,91,0,Math.PI*2);ctx.stroke();ctx.lineWidth=8;ctx.strokeStyle='#e7f3fd';ctx.beginPath();ctx.arc(cx,cy,69,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#12385f';ctx.textAlign='center';ctx.font='900 57px system-ui,sans-serif';ctx.fillText(String(a.score??'—'),cx,216);ctx.font='900 16px system-ui,sans-serif';ctx.fillText(`${T.score} · ${a.grade||'—'}`,cx,288);ctx.textAlign='left';state.y=390;
  }

  function measureCard(ctx,title,body,width,titleSize=19,bodySize=15){
    ctx.font=`800 ${titleSize}px system-ui,sans-serif`;const tl=lines(ctx,title,width-56);ctx.font=`500 ${bodySize}px system-ui,sans-serif`;const bl=lines(ctx,body,width-56);return Math.max(76,22+tl.length*(titleSize+7)+Math.max(1,bl.length)*(bodySize+7)+14);
  }
  function drawIssue(stateRef,pages,c,T){
    let s=stateRef.value,ctx=s.ctx;const title=label(c),body=detail(c),h=measureCard(ctx,title,body,CONTENT_W,19,15);ensure(stateRef,pages,h+14,T.issues);s=stateRef.value;ctx=s.ctx;
    ctx.fillStyle='#fff';ctx.strokeStyle='#d6e2ee';ctx.lineWidth=2;rr(ctx,M,s.y,CONTENT_W,h,20);ctx.fill();ctx.stroke();
    ctx.fillStyle='#f2a322';ctx.font='900 23px system-ui,sans-serif';ctx.fillText('!',M+28,s.y+25);ctx.fillStyle='#173956';ctx.font='800 19px system-ui,sans-serif';let yy=text(ctx,title,M+74,s.y+20,760,26);ctx.fillStyle='#5f7489';ctx.font='500 15px system-ui,sans-serif';text(ctx,body,M+74,yy+2,760,22);ctx.fillStyle='#c86b00';ctx.font='900 14px system-ui,sans-serif';ctx.textAlign='right';ctx.fillText(T.fix,W-M-25,s.y+27);ctx.textAlign='left';s.y+=h+14;
  }
  function drawGood(stateRef,pages,T){
    let s=stateRef.value;const h=78;ensure(stateRef,pages,h+14,T.issues);s=stateRef.value;const ctx=s.ctx;ctx.fillStyle='#f2fbf6';ctx.strokeStyle='#cdebdc';ctx.lineWidth=2;rr(ctx,M,s.y,CONTENT_W,h,18);ctx.fill();ctx.stroke();ctx.fillStyle='#16865e';ctx.font='900 24px system-ui,sans-serif';ctx.fillText('✓',M+28,s.y+22);ctx.fillStyle='#31566f';ctx.font='600 16px system-ui,sans-serif';text(ctx,T.noIssues,M+72,s.y+22,CONTENT_W-100,23);s.y+=h+14;
  }
  function drawPlan(stateRef,pages,p,i,T){
    let s=stateRef.value,ctx=s.ctx;const title=`${i+1}. ${p.title}`,body=p.text||'',h=measureCard(ctx,title,body,CONTENT_W,18,14);ensure(stateRef,pages,h+12,T.plan);s=stateRef.value;ctx=s.ctx;ctx.fillStyle='#f8fbfe';ctx.strokeStyle='#d8e5f0';ctx.lineWidth=2;rr(ctx,M,s.y,CONTENT_W,h,18);ctx.fill();ctx.stroke();ctx.fillStyle='#1478d8';ctx.font='900 16px system-ui,sans-serif';ctx.fillText(String(i+1),M+28,s.y+21);ctx.fillStyle='#173956';ctx.font='800 18px system-ui,sans-serif';let yy=text(ctx,p.title,M+72,s.y+18,CONTENT_W-100,25);ctx.fillStyle='#5d7286';ctx.font='500 14px system-ui,sans-serif';text(ctx,body,M+72,yy+2,CONTENT_W-100,21);s.y+=h+12;
  }
  function drawChecks(stateRef,pages,checks,T){
    sectionTitle(stateRef.value,T.checks);const gap=18,colW=(CONTENT_W-gap)/2;
    for(let i=0;i<checks.length;i+=2){
      let s=stateRef.value,ctx=s.ctx;const pair=checks.slice(i,i+2);const heights=pair.map(c=>measureCard(ctx,`${label(c)} · ${c.points}/${c.max}`,detail(c),colW,16,13));const rowH=Math.max(...heights);ensure(stateRef,pages,rowH+14,T.checks);s=stateRef.value;ctx=s.ctx;
      pair.forEach((c,j)=>{const x=M+j*(colW+gap),ok=Number(c.points)===Number(c.max);ctx.fillStyle='#fff';ctx.strokeStyle=ok?'#d7e4ef':'#f0d7b5';ctx.lineWidth=2;rr(ctx,x,s.y,colW,rowH,16);ctx.fill();ctx.stroke();ctx.fillStyle=ok?'#18865e':'#d17a00';ctx.fillRect(x,s.y,6,rowH);ctx.fillStyle='#173956';ctx.font='800 16px system-ui,sans-serif';let yy=text(ctx,`${label(c)} · ${c.points}/${c.max}`,x+24,s.y+16,colW-48,22);ctx.fillStyle='#607589';ctx.font='500 13px system-ui,sans-serif';text(ctx,detail(c),x+24,yy+2,colW-48,19)});s.y+=rowH+14;
    }
  }

  function renderPages(a){
    const T=lang(),pages=[],ref={value:addPage(pages)};drawHero(ref.value,a,T);sectionTitle(ref.value,T.issues);const bad=issueList(a);if(bad.length)bad.forEach(c=>drawIssue(ref,pages,c,T));else drawGood(ref,pages,T);sectionTitle(ref.value,T.plan);planList(a).forEach((p,i)=>drawPlan(ref,pages,p,i,T));drawChecks(ref,pages,a.checks||[],T);
    pages.forEach((p,idx)=>{const ctx=p.ctx;ctx.fillStyle='#d6e3ef';ctx.fillRect(M,H-82,CONTENT_W,2);ctx.fillStyle='#6e8194';ctx.font='600 13px system-ui,sans-serif';ctx.textAlign='left';ctx.fillText('BEQSON · Website Audit',M,H-58);ctx.textAlign='right';ctx.fillText(`beqson.com · digitalstudiobeqson@gmail.com · +995 551 73 93 33${pages.length>1?' · '+T.page+' '+(idx+1)+'/'+pages.length:''}`,W-M,H-58);ctx.textAlign='left'});
    return pages.map(p=>p.canvas);
  }

  function b64Bytes(url){const raw=atob(url.split(',')[1]);const out=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)out[i]=raw.charCodeAt(i);return out}
  function enc(s){return new TextEncoder().encode(s)}
  function cat(parts){const n=parts.reduce((a,b)=>a+b.length,0),out=new Uint8Array(n);let o=0;for(const p of parts){out.set(p,o);o+=p.length}return out}
  function pdfFromCanvases(canvases){
    const jpgs=canvases.map(c=>b64Bytes(c.toDataURL('image/jpeg',0.93))),n=canvases.length,total=2+n*3,objects=new Array(total+1);objects[1]=enc('<< /Type /Catalog /Pages 2 0 R >>');const kids=[];for(let i=0;i<n;i++)kids.push(`${3+i*3} 0 R`);objects[2]=enc(`<< /Type /Pages /Kids [${kids.join(' ')}] /Count ${n} >>`);
    for(let i=0;i<n;i++){const page=3+i*3,img=page+1,content=page+2,jpg=jpgs[i];objects[page]=enc(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Resources << /XObject << /Im${i+1} ${img} 0 R >> >> /Contents ${content} 0 R >>`);objects[img]=cat([enc(`<< /Type /XObject /Subtype /Image /Width ${W} /Height ${H} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${jpg.length} >>\nstream\n`),jpg,enc('\nendstream')]);const cmd=enc(`q\n595.28 0 0 841.89 0 0 cm\n/Im${i+1} Do\nQ\n`);objects[content]=cat([enc(`<< /Length ${cmd.length} >>\nstream\n`),cmd,enc('endstream')]);}
    const header=enc('%PDF-1.4\n%BEQSON\n'),parts=[header],offsets=new Array(total+1).fill(0);let pos=header.length;for(let i=1;i<=total;i++){offsets[i]=pos;const obj=cat([enc(`${i} 0 obj\n`),objects[i],enc('\nendobj\n')]);parts.push(obj);pos+=obj.length}const xrefPos=pos;let x=`xref\n0 ${total+1}\n0000000000 65535 f \n`;for(let i=1;i<=total;i++)x+=String(offsets[i]).padStart(10,'0')+' 00000 n \n';x+=`trailer\n<< /Size ${total+1} /Root 1 0 R >>\nstartxref\n${xrefPos}\n%%EOF`;parts.push(enc(x));return new Blob(parts,{type:'application/pdf'});
  }
  function save(blob,name){const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500)}
  async function exportV3(){const a=audit();if(!a)return;const canvases=renderPages(a),host=a.host||a.final_url||a.url||'site';save(pdfFromCanvases(canvases),`BEQSON-SEO-Audit-${safeName(host)}.pdf`)}

  function install(){
    const old=document.getElementById('downloadPdf');if(!old||old.dataset.pdfv3==='1')return;const b=old.cloneNode(true);b.dataset.pdfv3='1';old.replaceWith(b);b.addEventListener('click',async()=>{const a=audit();if(!a)return;const oldHtml=b.innerHTML;b.disabled=true;b.innerHTML='<span class="pdfIcon">◌</span> '+lang().generating;try{await exportV3()}catch(e){console.error('BEQSON PDF v3 failed',e);try{printPdfFallback()}catch(_){}}finally{b.disabled=false;b.innerHTML=oldHtml}});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
})();
