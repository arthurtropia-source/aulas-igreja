
/* ── motor 2026-10 · versículo "ao clicar": o botão mostra e esconde a ARA ── */
document.addEventListener('click',e=>{const b=e.target.closest('.vbtn');if(!b)return;e.stopPropagation();b.parentElement.classList.toggle('aberta');});
