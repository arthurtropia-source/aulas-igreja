(function(){
const palco=document.getElementById('palco');
const slots=[...document.querySelectorAll('.slot')];
const paginas=slots.map(s=>s.querySelector('.pagina'));
const bPrev=document.getElementById('prev'),bNext=document.getElementById('next');
const conta=document.getElementById('conta'),onde=document.getElementById('onde'),trilha=document.querySelector('#trilha i');
const sumario=document.getElementById('sumario');
let atual=0, pularAprof=false;

/* numeração e rótulos vindos do próprio DOM — o índice nunca fica desatualizado */
const meta=paginas.map((p,i)=>({
  i, n:i+1,
  titulo:p.dataset.titulo||'',
  secao:p.dataset.secao||'',
  aula:p.dataset.aula||'',
  aprof:p.dataset.tipo==='aprofundar',
  mapa:!!p.querySelector('.pg-mapa.anim'),
  indice:p.dataset.indice!=='nao'
}));

/* carimba cabeçalho e número em cada página */
paginas.forEach((p,i)=>{
  if(p.dataset.cabecalho==='nao')return;
  const top=document.createElement('div');top.className='pg-top';
  const esc=p.classList.contains('vermelha')||p.classList.contains('preta');
  top.innerHTML='<img class="logo" src="'+(esc?LOGO_W:LOGO_K)+'" alt="'+NOME_CURSO+'"><div class="pg-right"><div class="pg-sec">'+(meta[i].secao||'')+'</div><div class="pg-num">'+meta[i].n+' / '+paginas.length+'</div></div>';
  p.prepend(top);
});

/* ajuste de enquadramento: a página inteira sempre cabe na tela */
function enquadrar(){
  const w=palco.clientWidth-48, h=palco.clientHeight-48;
  const k=Math.min(w/1280,h/720,1.35);
  document.documentElement.style.setProperty('--k',k);
  paginas.forEach(p=>{p.style.transform='scale('+k+')';});
  slots.forEach(s=>{s.style.height=(palco.clientHeight)+'px';});
  // compensa o espaço que o scale não ocupa
  paginas.forEach(p=>{p.style.marginBlock=((720*k)-720)/2+'px';});
}
addEventListener('resize',enquadrar);

function atualiza(i){
  atual=i;const m=meta[i];
  conta.innerHTML=m.n+'<span> / '+paginas.length+'</span>';
  onde.innerHTML='<strong>'+(m.titulo||'')+'</strong>'+(m.aula?m.aula+(m.secao?' · '+m.secao:''):m.secao||'');
  trilha.style.width=((i+1)/paginas.length*100)+'%';
  bPrev.disabled=i===0;bNext.disabled=i===paginas.length-1;
}
function ir(i,instante){
  i=Math.max(0,Math.min(paginas.length-1,i));
  if(pularAprof&&meta[i].aprof){const d=i>atual?1:-1;let j=i;while(j>0&&j<paginas.length-1&&meta[j].aprof)j+=d;i=j;}
  if(instante)palco.style.scrollBehavior='auto';
  slots[i].scrollIntoView({block:'center'});
  if(instante)requestAnimationFrame(()=>palco.style.scrollBehavior='smooth');
  atualiza(i);
}
bPrev.onclick=()=>ir(atual-1);bNext.onclick=()=>ir(atual+1);

/* página ativa conforme a rolagem (inclusive se rolarem com o dedo) */
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)atualiza(slots.indexOf(e.target));})},{root:palco,threshold:.6});
slots.forEach(s=>io.observe(s));

/* ── sumário gerado do DOM, com número de página ── */
function montaSumario(){
  const g=document.getElementById('grade');const porAula={};
  meta.forEach(m=>{if(!m.indice)return;const a=m.aula||'—';(porAula[a]=porAula[a]||[]).push(m);});
  const grupos=Object.entries(porAula); const retrai=grupos.length>2; g.classList.toggle('retratil',retrai);
  g.innerHTML=grupos.map(([aula,itens])=>
    '<div class="aula'+(retrai?'':' aberta')+'" data-ini="'+itens[0].i+'" data-fim="'+itens[itens.length-1].i+'"><h3><span><i class="caret"></i>'+aula+'</span><span>p. '+itens[0].n+'–'+itens[itens.length-1].n+'</span></h3><div class="lista">'+
    itens.map(m=>'<a href="#" data-i="'+m.i+'" class="'+(m.aprof?'ap':'')+'"><span class="t">'+m.titulo+(m.mapa?' <span class="tag">Mapa interativo</span>':'')+'</span><span class="pon"></span><span class="n">'+m.n+'</span></a>').join('')+
    '</div></div>').join('');
  g.onclick=e=>{const h=e.target.closest('h3');if(h){const bl=h.parentElement;if(g.classList.contains('retratil'))bl.classList.toggle('aberta');return;}
    const a=e.target.closest('a');if(!a)return;e.preventDefault();fechaSumario();ir(+a.dataset.i,true);};
}
function abreSumario(){
  const g=document.getElementById('grade');
  if(g.classList.contains('retratil')){g.querySelectorAll('.aula').forEach(b=>{const ini=+b.dataset.ini,fim=+b.dataset.fim;const aqui=atual>=ini&&atual<=fim;b.classList.toggle('aberta',aqui);if(aqui)b.scrollIntoView({block:'nearest'});});}
  sumario.classList.add('on');}
function fechaSumario(){sumario.classList.remove('on');}
document.getElementById('bSumario').onclick=()=>sumario.classList.contains('on')?fechaSumario():abreSumario();
document.getElementById('fecharSum').onclick=fechaSumario;

/* ── ir para página: digite o número ── */
const irpara=document.getElementById('irpara'),irv=document.getElementById('irv');let buf='',t=null;
function digito(d){
  buf=(buf+d).slice(0,3);irv.textContent=buf;irpara.classList.add('on');
  clearTimeout(t);t=setTimeout(confirma,1400);
}
function confirma(){if(buf){ir(parseInt(buf,10)-1,true);}buf='';irpara.classList.remove('on');}

/* ── teclado ── */
addEventListener('keydown',e=>{
  if(e.key>='0'&&e.key<='9'){digito(e.key);return;}
  switch(e.key){
    case 'ArrowRight':case 'PageDown':case ' ':case 'ArrowDown':e.preventDefault();ir(atual+1);break;
    case 'ArrowLeft':case 'PageUp':case 'ArrowUp':e.preventDefault();ir(atual-1);break;
    case 'Home':e.preventDefault();ir(0,true);break;
    case 'End':e.preventDefault();ir(paginas.length-1,true);break;
    case 'Enter':confirma();break;
    case 'Escape':fechaSumario();buf='';irpara.classList.remove('on');break;
    case 's':case 'S':sumario.classList.contains('on')?fechaSumario():abreSumario();break;
    case 'f':case 'F':document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();break;
  }
});
document.getElementById('bTela').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();
const bAp=document.getElementById('bAprof');
if(bAp)bAp.onclick=()=>{pularAprof=!pularAprof;bAp.textContent=pularAprof?'Aprofundar: oculto':'Aprofundar: incluso';bAp.style.borderColor=pularAprof?'rgba(255,255,255,.25)':'';};

montaSumario();enquadrar();atualiza(0);
})();

/* ── páginas com passos (mapas animados) ── */
(function(){
const anims=[...document.querySelectorAll('.pg-mapa.anim')];
anims.forEach(a=>{
  const svg=a.querySelector('svg'); const vb0=svg.getAttribute('viewBox'); svg.dataset.vb0=vb0; const vbZ=a.dataset.zoom;
  const segs=[...svg.querySelectorAll('.seg')]; const caps=[...a.querySelectorAll('.cap')];
  const cidades=JSON.parse(a.dataset.cidades.replace(/'/g,'"'));
  segs.forEach(s=>{if(s.hasAttribute('stroke-dasharray')){s.classList.add('tracejada');}else{const L=s.getTotalLength();s.style.setProperty('--len',L);}});
  let cur=0,raf=null;
  function lerpVB(from,to,t){const f=from.split(' ').map(Number),g=to.split(' ').map(Number);return f.map((v,i)=>v+(g[i]-v)*t).join(' ');}
  function animVB(to){const from=svg.getAttribute('viewBox');if(from===to)return;cancelAnimationFrame(raf);const t0=performance.now();
    (function step(now){const t=Math.min(1,(now-t0)/900);const e=t<.5?2*t*t:-1+(4-2*t)*t;svg.setAttribute('viewBox',lerpVB(from,to,e));if(t<1)raf=requestAnimationFrame(step);})(t0);}
  function render(){
    a.dataset.cur=cur;
    caps.forEach(c=>c.classList.toggle('on',+c.dataset.passo===cur));
    segs.forEach(s=>{const p=+s.dataset.passo;s.classList.toggle('on',p<=cur&&cur>0);s.classList.toggle('feita',p<cur&&cur>0);});
    svg.querySelectorAll('.foco').forEach(f=>f.classList.toggle('on',cur>0&&f.dataset.cidade===cidades[cur]));
    animVB(cur===0?vb0:vbZ); svg.classList.toggle('zoom',cur>0);
  }
  a.__passo=function(d){const n=+a.dataset.passos;const nx=cur+d;if(nx<0||nx>n)return false;cur=nx;render();return true;};
  a.querySelector('.quadro').addEventListener('click',()=>{if(!a.__passo(1))a.__passo(-cur);});
  render();
});
/* intercepta as setas: avança passo antes de mudar de página */
const palco=document.getElementById('palco');
addEventListener('keydown',e=>{
  if(!['ArrowRight','ArrowLeft',' ','PageDown','PageUp','ArrowDown','ArrowUp'].includes(e.key))return;
  const slots=[...document.querySelectorAll('.slot')];
  const vis=slots.find(s=>{const r=s.getBoundingClientRect();return r.top<innerHeight/2&&r.bottom>innerHeight/2;});
  const a=vis&&vis.querySelector('.pg-mapa.anim'); if(!a)return;
  const fwd=['ArrowRight',' ','PageDown','ArrowDown'].includes(e.key);
  if(a.__passo(fwd?1:-1)){e.stopImmediatePropagation();e.preventDefault();}
},true);
})();

/* ── modo de edição: E liga/desliga; "Salvar" publica nova versão (no artefato) ou baixa o HTML (arquivo) ── */
(function(){
const barra=document.getElementById('barra');
const bEd=document.createElement('button');bEd.id='bEditar';bEd.textContent='Editar (E)';
const bSv=document.createElement('button');bSv.id='bSalvar';bSv.textContent='Salvar';bSv.style.display='none';
const aviso=document.createElement('div');aviso.id='aviso';document.body.appendChild(aviso);
barra.insertBefore(bSv,document.getElementById('bTela'));barra.insertBefore(bEd,bSv);
let on=false, artifactNS=undefined;
function avisa(t,ms){aviso.textContent=t;aviso.classList.add('on');clearTimeout(aviso._t);if(ms)aviso._t=setTimeout(()=>aviso.classList.remove('on'),ms);}
function toggle(){on=!on;document.querySelectorAll('.pagina').forEach(p=>{p.contentEditable=on;p.classList.toggle('editando',on);});
  bEd.textContent=on?'Editando… (Esc sai)':'Editar (E)';bSv.style.display=on?'':'none';
  document.getElementById('palco').style.scrollSnapType=on?'none':'';}
bEd.onclick=toggle;
addEventListener('keydown',e=>{if((e.key==='e'||e.key==='E')&&!on&&!e.ctrlKey&&!e.metaKey)toggle();else if(e.key==='Escape'&&on)toggle();});
addEventListener('keydown',e=>{if(on&&!['Escape','F11'].includes(e.key))e.stopImmediatePropagation();},true);
/* documento limpo, regenerado a partir do conteúdo das páginas (sem estado de execução) */
function documento(){
  const body=document.body.cloneNode(true);
  body.querySelectorAll('.pg-top,#aviso,[id^=plaud]').forEach(x=>x.remove());
  body.querySelectorAll('.pagina').forEach(p=>{p.removeAttribute('contenteditable');p.classList.remove('editando');p.style.transform='';p.style.marginBlock='';if(!p.getAttribute('style'))p.removeAttribute('style');});
  body.querySelectorAll('.slot').forEach(s=>s.removeAttribute('style'));
  body.querySelectorAll('.pg-mapa.anim').forEach(a=>{a.dataset.cur='0';a.querySelectorAll('.cap.on,.seg.on,.seg.feita,.foco.on,svg.zoom').forEach(x=>x.classList.remove('on','feita','zoom'));const s=a.querySelector('svg');if(s&&s.dataset.vb0)s.setAttribute('viewBox',s.dataset.vb0);});
  const b=body.querySelector('#bSalvar');if(b){b.style.display='none'}
  const ed=body.querySelector('#bEditar');if(ed)ed.textContent='Editar (E)';
  const palco=body.querySelector('#palco');if(palco)palco.removeAttribute('style');
  const quer=['TITLE','STYLE','#palco','#trilha','#barra','#sumario','#irpara','SCRIPT'];
  const partes=[...body.children].filter(el=>quer.includes(el.tagName)||quer.includes('#'+el.id)).map(el=>el.outerHTML);
  const reset=(document.head.querySelector('style')||{}).textContent||'';
  const ehArtefato=!!document.head.querySelector('meta[name=viewport][content*="viewport-fit"]');
  if(ehArtefato) return '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>'+reset+'</style></head><body>\n'+partes.join('\n')+'\n</body></html>';
  return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+document.title+'</title></head><body>\n'+partes.join('\n')+'\n</body></html>';
}
bSv.onclick=async()=>{
  const html=documento();
  if(window.claude&&claude.use){
    if(artifactNS===undefined){avisa('Conectando…');try{artifactNS=await claude.use('artifact');}catch(e){artifactNS=null;}}
    if(artifactNS){
      avisa('Salvando nova versão…');
      try{await artifactNS.publish(html);avisa('Salvo. A página vai recarregar com a nova versão.',4000);return;}
      catch(err){const c=err&&err.code;
        if(c==='conflict'){avisa('Outra versão foi publicada antes; a página vai recarregar. Refaça a edição nela.',6000);return;}
        if(c==='not_writer'||c==='not_granted'){avisa('Você não tem permissão de edição neste artefato.',6000);return;}
        avisa('Não foi possível salvar ('+(c||'erro')+').',6000);return;}
    }
  }
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([html],{type:'text/html'}));
  a.download=(document.title.replace(/[^\w\- ]+/g,'').trim()||'slides')+' - editado.html';a.click();
  avisa('Arquivo baixado.',3000);
};
})();
