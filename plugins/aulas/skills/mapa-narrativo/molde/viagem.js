(() => {
'use strict';
const NS = 'http://www.w3.org/2000/svg';
const D = DADOS, [BW, BH] = D.base, CENAS = D.cenas;
const $ = s => document.querySelector(s);
const svg = $('#mapa'), caixa = $('#caixa');
const G = { reg: $('#g-regioes'), tri: $('#g-trilhas'), rot: $('#g-rotas'), car: $('#g-cartas'), lug: $('#g-lugares'), via: $('#g-viajante') };
const LUG = {}; D.lugares.forEach(l => LUG[l.n] = l);
const el = (tag, at = {}, pai) => { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); if (pai) pai.appendChild(e); return e; };
const esperar = ms => new Promise(r => setTimeout(r, ms));
const suave = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const ESCALAVEIS = []; // grupos desenhados em pixels de tela: [g, x, y]

/* ---------- a tela e a câmera ---------- */
let W, H, livre, vista = null, cenaAtual = -1, rodada = 0, automatico = false;
function medir() {
  W = innerWidth; H = innerHeight;
  if (W / H <= 1) {               // celular em pé: o box ocupa a parte de baixo
    livre = { x: 16, y: 60, w: W - 32, h: H * 0.5 - 76 };
  } else if (document.body.classList.contains('caixa-direita')) {   // telão, foco na borda esquerda do mapa
    const esq = caixa.offsetLeft - 24;
    livre = { x: 70, y: 90, w: esq - 70, h: H - 90 - 120 };
  } else {                        // telão: o box fica à esquerda
    const dir = caixa.offsetLeft + caixa.offsetWidth + 24;
    livre = { x: dir, y: 90, w: W - dir - 70, h: H - 90 - 120 };
  }
}
const sMin = () => Math.max(W / BW, H / BH);
function prender(v) {             // nunca mostra além da base do mapa
  const s = Math.max(v.s, sMin());
  const fx = livre.x + livre.w / 2, fy = livre.y + livre.h / 2;
  let x0 = v.cx - fx / s, y0 = v.cy - fy / s;
  x0 = Math.min(Math.max(x0, 0), BW - W / s); y0 = Math.min(Math.max(y0, 0), BH - H / s);
  return { cx: x0 + fx / s, cy: y0 + fy / s, s };
}
function enquadrar(b) {
  const bw = Math.max(b[2] - b[0], 1), bh = Math.max(b[3] - b[1], 1);
  return prender({ cx: (b[0] + b[2]) / 2, cy: (b[1] + b[3]) / 2, s: Math.min(livre.w / bw, livre.h / bh) });
}
function aplicar(v) {
  vista = v;
  const fx = livre.x + livre.w / 2, fy = livre.y + livre.h / 2;
  svg.setAttribute('viewBox', `${v.cx - fx / v.s} ${v.cy - fy / v.s} ${W / v.s} ${H / v.s}`);
  const k = 1 / v.s, z = v.s / sMin();
  for (const [g, x, y] of ESCALAVEIS) g.setAttribute('transform', `translate(${x} ${y}) scale(${k})`);
  for (const r of REGIOES) {
    const a = Math.min(1, Math.max(0, Math.min((z - r.z0) / 0.6 + 1, (r.z1 - z) / 0.6 + 1)));
    r.e.style.opacity = r.z0 <= 0 && z <= r.z1 ? Math.min(1, (r.z1 - z) / 0.6 + 1) : a;
  }
}
function voar(alvo, ms, tok) {    // vai e volta no zoom quando a distância é grande
  const de = vista;
  const dist = Math.hypot(alvo.cx - de.cx, alvo.cy - de.cy);
  const precisa = Math.min(W, H) * 0.9 / Math.max(dist, 1);
  const baixo = Math.min(de.s, alvo.s);
  const salto = precisa < baixo ? Math.log(baixo) - Math.log(Math.max(precisa, sMin())) : 0;
  const dur = ms ?? Math.min(3400, 1300 + 900 * salto + 0.25 * dist);
  return new Promise((ok, falha) => {
    const t0 = performance.now();
    const passo = agora => {
      if (tok !== rodada) return falha('cancelada');
      const t = Math.min(1, Math.max(0, (agora - t0) / dur)), e = suave(t);
      const ls = Math.log(de.s) + (Math.log(alvo.s) - Math.log(de.s)) * e - salto * Math.sin(Math.PI * e);
      aplicar(prender({ cx: de.cx + (alvo.cx - de.cx) * e, cy: de.cy + (alvo.cy - de.cy) * e, s: Math.exp(ls) }));
      t < 1 ? requestAnimationFrame(passo) : ok();
    };
    requestAnimationFrame(passo);
  });
}

/* ---------- o que é desenhado ---------- */
const REGIOES = D.regioes.map(r => {
  const g = el('g', {}, G.reg);
  const t = el('text', { class: 'reg ' + (r.tipo === 'mar' ? 'mar' : r.tipo === 'rio' ? 'rio' : ''), 'text-anchor': 'middle',
    'font-size': r.tipo === 'região' ? 14 : r.tipo === 'rio' ? 15 : 17 }, g);
  t.textContent = r.t;
  ESCALAVEIS.push([g, r.x, r.y]);
  return { ...r, e: g };
});
const TORRE = 'M-7,5 L-7,-3 L-5,-3 L-5,-6 L-2.5,-6 L-2.5,-3 L2.5,-3 L2.5,-6 L5,-6 L5,-3 L7,-3 L7,5 Z';
for (const l of D.lugares) {
  const g = el('g', { class: 'lugar oculto' + (l.chave ? ' chave' : '') }, G.lug);
  el('circle', { class: 'pulso', r: 10 }, g);
  if (l.chave) el('path', { d: TORRE, fill: l.cor || '#7a1f12', stroke: '#2a1d10', 'stroke-width': 1.2 }, g);
  else el('circle', { r: 3.8, fill: '#f6ecd2', stroke: '#2a1d10', 'stroke-width': 1.6 }, g);
  const t = el('text', { class: 'nome', x: l.dx * 1.15, y: l.dy * 1.15 + (l.dy > 0 ? 2 : 0), 'font-size': l.chave ? 18 : 15 }, g);
  t.textContent = l.n;
  l.e = g; ESCALAVEIS.push([g, l.x, l.y]);
}

function caminho(pts, ate) {      // a linha até o comprimento "ate" (ou inteira)
  let d = `M${pts[0][0]},${pts[0][1]}`, feito = 0, fim = pts[0];
  for (let i = 1; i < pts.length; i++) {
    const [a, b] = [pts[i - 1], pts[i]], seg = Math.hypot(b[0] - a[0], b[1] - a[1]);
    if (ate != null && feito + seg >= ate) {
      const f = (ate - feito) / seg; fim = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
      d += `L${fim[0]},${fim[1]}`; return { d, fim, i };
    }
    d += `L${b[0]},${b[1]}`; feito += seg; fim = b;
  }
  return { d, fim, i: pts.length };
}
const comprimento = pts => pts.slice(1).reduce((s, b, i) => s + Math.hypot(b[0] - pts[i][0], b[1] - pts[i][1]), 0);

function arco(c, n) {             // a curva do voo da carta
  const [a, b] = [c.a, c.b], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
  const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy);
  const curva = 0.28 + 0.14 * n, q = [mx + dy * curva * (dx > 0 ? -1 : 1), my - Math.abs(dx) * curva - L * 0.05];
  return t => [(1 - t) ** 2 * a[0] + 2 * (1 - t) * t * q[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * q[1] + t * t * b[1]];
}
function desenharVoo(c, n, pai) {
  const f = arco(c, n); let d = '';
  for (let i = 0; i <= 40; i++) { const p = f(i / 40); d += (i ? 'L' : 'M') + p[0] + ',' + p[1]; }
  return el('path', { class: 'voo', d }, pai);
}
function rolo(rot) {
  const g = el('g', { class: 'rolo' }, G.car);
  el('rect', { x: -13, y: -8, width: 26, height: 16, rx: 3, fill: '#f6ecd2', stroke: '#2a1d10', 'stroke-width': 1.4 }, g);
  el('circle', { cx: -13, cy: 0, r: 8, fill: '#e4d2a8', stroke: '#2a1d10', 'stroke-width': 1.4 }, g);
  el('circle', { cx: 13, cy: 0, r: 8, fill: '#e4d2a8', stroke: '#2a1d10', 'stroke-width': 1.4 }, g);
  el('rect', { x: -2.5, y: -8, width: 5, height: 16, fill: '#7a1f12' }, g);
  const t = el('text', { y: -16, 'text-anchor': 'middle', 'font-size': 17 }, g); t.textContent = rot;
  const item = [g, 0, 0]; ESCALAVEIS.push(item);
  return item;
}
function soltar(item) { item[0].remove(); ESCALAVEIS.splice(ESCALAVEIS.indexOf(item), 1); }

/* ---------- o estado de cada cena ---------- */
function vistos(ate) {            // lugares revelados antes da cena "ate"
  const s = new Set();
  CENAS.slice(0, ate).forEach(c => { c.acender.forEach(n => s.add(n)); c.percursos.forEach(p => p.nomes.forEach(n => LUG[n] && s.add(n))); c.cartas.forEach(k => { s.add(k.de); s.add(k.para); }); });
  return s;
}
function marcarLugares(revelados, acesos) {
  for (const l of D.lugares) {
    const c = l.e.classList;
    c.remove('oculto', 'nevoa', 'aceso');
    if (acesos.has(l.n)) c.add('aceso');
    else if (!revelados.has(l.n)) c.add(l.chave ? 'nevoa' : 'oculto');
  }
}
function limpar() {
  for (const g of [G.tri, G.rot, G.car, G.via]) g.replaceChildren();
  for (let i = ESCALAVEIS.length - 1; i >= 0; i--) if (!ESCALAVEIS[i][0].isConnected) ESCALAVEIS.splice(i, 1);
}
function montarEstado(i, completa) {
  limpar();
  const trilha = el('g', { class: 'trilha' }, G.tri);
  CENAS.slice(0, i).forEach(c => c.percursos.forEach(p => el('path', { class: 'rota ' + p.tipo, d: caminho(p.pts).d }, trilha)));
  CENAS.slice(0, i).forEach(c => c.cartas.forEach((k, n) => desenharVoo(k, n, trilha)));
  const c = CENAS[i], rev = vistos(i);
  if (completa) {
    c.percursos.forEach(p => el('path', { class: 'rota ' + p.tipo, d: caminho(p.pts).d }, G.rot));
    c.cartas.forEach((k, n) => desenharVoo(k, n, G.car));
    vistos(i + 1).forEach(n => rev.add(n));
    marcarLugares(rev, new Set(c.acender));
  } else marcarLugares(rev, new Set());
}

/* ---------- tocar uma cena ---------- */
function bboxDe(pts, folga = 1.25) {
  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
  const w = Math.max(Math.max(...xs) - Math.min(...xs), 30) * folga, h = Math.max(Math.max(...ys) - Math.min(...ys), 20) * folga;
  return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2];
}
async function percorrer(p, tok) {
  const L = comprimento(p.pts), linha = el('path', { class: 'rota ' + p.tipo }, G.rot);
  const viajante = el('g', {}, G.via);
  el('circle', { r: 15, fill: '#7a1f12', opacity: .22 }, viajante);
  el('circle', { r: 8, fill: '#7a1f12', stroke: '#f6ecd2', 'stroke-width': 2.4 }, viajante);
  const item = [viajante, p.pts[0][0], p.pts[0][1]]; ESCALAVEIS.push(item);
  const dur = Math.min(5200, Math.max(1600, L * vista.s / 0.32));
  const rev = new Set();
  await new Promise((ok, falha) => {
    const t0 = performance.now();
    const passo = agora => {
      if (tok !== rodada) return falha('cancelada');
      const t = Math.min(1, Math.max(0, (agora - t0) / dur)), r = caminho(p.pts, L * (t < 1 ? suave(t) : 1));
      linha.setAttribute('d', r.d);
      item[1] = r.fim[0]; item[2] = r.fim[1];
      viajante.setAttribute('transform', `translate(${r.fim[0]} ${r.fim[1]}) scale(${1 / vista.s})`);
      for (let j = 0; j < r.i; j++) { const n = p.nomes[j]; if (LUG[n] && !rev.has(n)) { rev.add(n); LUG[n].e.classList.remove('oculto', 'nevoa'); } }
      t < 1 ? requestAnimationFrame(passo) : ok();
    };
    requestAnimationFrame(passo);
  });
  p.nomes.forEach(n => LUG[n] && LUG[n].e.classList.remove('oculto', 'nevoa'));
  soltar(item);
}
async function enviarCarta(k, n, tok) {
  const f = arco(k, n), trilho = desenharVoo(k, n, G.car), item = rolo(k.rot);
  trilho.style.opacity = 0;
  await new Promise((ok, falha) => {
    const t0 = performance.now(), dur = 2200;
    const passo = agora => {
      if (tok !== rodada) return falha('cancelada');
      const t = Math.min(1, Math.max(0, (agora - t0) / dur)), p = f(suave(t));
      item[1] = p[0]; item[2] = p[1];
      item[0].setAttribute('transform', `translate(${p[0]} ${p[1]}) scale(${1 / vista.s})`);
      trilho.style.opacity = Math.min(.8, t * 2);
      t < 1 ? requestAnimationFrame(passo) : ok();
    };
    requestAnimationFrame(passo);
  });
  LUG[k.para] && LUG[k.para].e.classList.remove('oculto', 'nevoa');
}
async function tocar(i, tok) {
  const c = CENAS[i];
  montarEstado(i, false);
  if (c.percursos.length) {
    await voar(enquadrar(bboxDe(c.percursos.flatMap(p => p.pts))), null, tok);
    for (const p of c.percursos) await percorrer(p, tok);
    await esperar(250);
  }
  await voar(enquadrar(c.cam), null, tok);
  for (let n = 0; n < c.cartas.length; n++) {
    const fim = enviarCarta(c.cartas[n], n, tok);
    if (n === c.cartas.length - 1) await fim; else await esperar(700);
  }
  if (tok !== rodada) return;
  marcarLugares(vistos(i + 1), new Set(c.acender));
}

/* ---------- o box, o topo e a barra ---------- */
function preencherCaixa(c) {
  caixa.classList.add('saindo');
  setTimeout(() => {
    caixa.querySelector('.rotulo').textContent = c['rótulo'] || '';
    caixa.querySelector('.titulo').textContent = c['título'];
    caixa.querySelector('.texto').textContent = c.texto;
    caixa.querySelector('.nota').textContent = c.nota || '';
    caixa.querySelector('.fonte').textContent = 'Fonte: ' + c.fonte;
    caixa.scrollTop = 0;
    caixa.classList.remove('saindo');
  }, 320);
  $('#topo .trecho').textContent = c.trecho || '';
  $('#topo .contador').textContent = `${cenaAtual + 1} / ${CENAS.length}`;
  document.querySelectorAll('#progresso button').forEach((b, j) => {
    b.classList.toggle('feita', j < cenaAtual); b.classList.toggle('atual', j === cenaAtual);
  });
}
function montarBarra() {
  const nav = $('#progresso'); let grupo = null, nome = null;
  CENAS.forEach((c, j) => {
    if (c.trecho !== nome) {
      nome = c.trecho; grupo = document.createElement('div'); grupo.className = 'grupo';
      grupo.innerHTML = `<span>${nome || ''}</span><div class="marcas"></div>`; nav.appendChild(grupo); grupo.n = 0;
    }
    const b = document.createElement('button'); b.title = c.nome; b.setAttribute('aria-label', c.nome);
    b.onclick = e => { e.stopPropagation(); ir(j, false); };
    grupo.querySelector('.marcas').appendChild(b); grupo.style.setProperty('--n', ++grupo.n);
  });
}

/* ---------- de que lado fica o box: o que esconde menos lugares da cena ---------- */
function pontosDaCena(c) {
  const p = c.acender.map(n => [LUG[n].x, LUG[n].y]);
  c.cartas.forEach(k => p.push(k.a, k.b));
  if (!p.length) p.push([(c.cam[0] + c.cam[2]) / 2, (c.cam[1] + c.cam[3]) / 2]);
  return p;
}
function escondidos(c) {
  medir();
  const v = enquadrar(c.cam), fx = livre.x + livre.w / 2, fy = livre.y + livre.h / 2;
  const r = caixa.getBoundingClientRect(), m = 40;
  return pontosDaCena(c).filter(([x, y]) => {
    const sx = (x - v.cx) * v.s + fx, sy = (y - v.cy) * v.s + fy;
    return sx > r.left - m && sx < r.right + 140 && sy > r.top - m && sy < r.bottom + m;
  }).length;
}
function escolherLado(c) {
  const corpo = document.body.classList;
  if (W / H <= 1 || c.caixa) { corpo.toggle('caixa-direita', c.caixa === 'direita'); medir(); return; }
  corpo.remove('caixa-direita'); const esq = escondidos(c);
  corpo.add('caixa-direita'); const dir = escondidos(c);
  corpo.toggle('caixa-direita', dir < esq);
  medir();
}

/* ---------- navegação ---------- */
async function ir(i, animar = true) {
  i = Math.max(0, Math.min(CENAS.length - 1, i));
  const anterior = cenaAtual, tok = ++rodada;
  cenaAtual = i; history.replaceState(null, '', '#' + (i + 1));
  const c = CENAS[i];
  preencherCaixa(c);
  escolherLado(c);
  const t0 = performance.now();
  try {
    if (animar && i === anterior + 1) await tocar(i, tok);
    else { montarEstado(i, true); await voar(enquadrar(CENAS[i].cam), anterior < 0 ? 1 : 900, tok); }
  } catch (e) { return; }
  document.body.dataset.pronta = i + 1;
  if (automatico && tok === rodada && i < CENAS.length - 1) {
    await esperar(Math.max(1500, (CENAS[i].dur || 10) * 1000 - (performance.now() - t0)));
    if (automatico && tok === rodada) ir(i + 1);
  }
}
const avancar = () => ir(cenaAtual + 1), voltar = () => ir(cenaAtual - 1, false);

document.addEventListener('keydown', e => {
  if (['ArrowRight', ' ', 'PageDown', 'Enter'].includes(e.key)) { e.preventDefault(); avancar(); }
  else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); voltar(); }
  else if (e.key === 'Home') ir(0, false);
  else if (e.key === 'End') ir(CENAS.length - 1, false);
  else if (/^[fF]$/.test(e.key)) document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.();
  else if (/^[aA]$/.test(e.key)) { automatico = !automatico; document.body.classList.toggle('automatico', automatico); if (automatico) avancar(); }
  else if (/^[nN]$/.test(e.key)) document.body.classList.toggle('sem-fontes');
  $('#ajuda').classList.add('some');
});
let toque = null;
$('#palco').addEventListener('touchstart', e => { toque = [e.touches[0].clientX, e.touches[0].clientY]; }, { passive: true });
$('#palco').addEventListener('touchend', e => {
  if (!toque) return;
  const dx = e.changedTouches[0].clientX - toque[0], dy = e.changedTouches[0].clientY - toque[1];
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? avancar() : voltar(); toque = 'feito'; }
}, { passive: true });
$('#palco').addEventListener('click', e => {
  if (toque === 'feito') { toque = null; return; }
  if (e.target.closest('#caixa, #progresso')) return;
  e.clientX < W * 0.25 ? voltar() : avancar();
  $('#ajuda').classList.add('some');
});
addEventListener('resize', () => { medir(); if (cenaAtual >= 0) aplicar(enquadrar(CENAS[cenaAtual].cam)); });

/* ---------- começo ---------- */
$('#topo .titulo-aula').textContent = (D.meta['título'] || '').split('·')[0].trim();
if (D.meta['versão']) $('#selo').textContent = 'prévia · ' + D.meta['versão'].split('·')[0].replace('prévia', '').trim(); else $('#selo').remove();
montarBarra(); medir(); aplicar(prender({ cx: BW / 2, cy: BH / 2, s: sMin() }));
setTimeout(() => $('#ajuda').classList.add('some'), 6000);
const h = parseInt(location.hash.slice(1), 10);
ir(h > 0 ? h - 1 : 0, false);
window.__viagem = { ir, CENAS, get cena() { return cenaAtual; } };
})();
