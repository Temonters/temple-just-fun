// === Анімація пилу / вогників ===
(function(){
  const canvas=document.getElementById('ash');
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  let w,h, parts=[];
  function resize(){ w=canvas.width=innerWidth; h=canvas.height=innerHeight; }
  addEventListener('resize', resize); resize();
  for(let i=0;i<70;i++) parts.push({x:Math.random()*w,y:Math.random()*h,r:Math.random()*2.5+0.3,vx:(Math.random()-0.5)*0.4,vy:-(Math.random()*0.9+0.2),o:Math.random()*0.5+0.2});
  (function loop(){
    ctx.clearRect(0,0,w,h);
    for(let p of parts){
      p.x+=p.vx; p.y+=p.vy;
      if(p.y<-10){ p.y=h+10; p.x=Math.random()*w; }
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*4);
      g.addColorStop(0,`rgba(241,208,122,${p.o})`);
      g.addColorStop(1,'transparent');
      ctx.fillStyle=g;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r*3,0,6.28); ctx.fill();
    }
    requestAnimationFrame(loop);
  })();
})();

// === Тема ТЕМНА / ЯСНА ===
(function(){
  const root=document.documentElement;
  const switchEl=document.getElementById('themeSwitch');
  if(!switchEl) return;
  const btns=switchEl.querySelectorAll('button');
  function setTheme(t){
    root.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
    btns.forEach(b=> b.classList.toggle('active', b.dataset.theme===t));
    const hero=document.getElementById('heroImg');
    if(hero){
      hero.style.filter = t==='light' ? 'brightness(0.58) saturate(0.9) blur(1px)' : 'brightness(0.36) saturate(1.05) blur(1px)';
    }
  }
  const saved=localStorage.getItem('theme')||'dark';
  setTheme(saved);
  btns.forEach(b=> b.addEventListener('click', ()=> setTheme(b.dataset.theme)));
})();

// === Таби і пошук (спрощено, бо у тебе Django рендерить боси на бекенді) ===
(function(){
  const tabs=document.querySelectorAll('.chapter-tab');
  const search=document.getElementById('search');
  if(!tabs.length) return;
  let active=1;
  function render(){
    // тут твій оригінальний код рендеру босів з crafts.js
    // якщо в base.html боси вже в HTML — просто фільтруємо
    const q=(search?.value||'').toLowerCase();
    document.querySelectorAll('.boss-card').forEach(card=>{
      const txt=card.textContent.toLowerCase();
      card.style.display = q && !txt.includes(q) ? 'none' : '';
    });
  }
  tabs.forEach(btn=>{
    btn.addEventListener('click', ()=>{
      active=parseInt(btn.dataset.tab);
      tabs.forEach(b=>{ b.classList.remove('active'); b.classList.add('inactive'); });
      btn.classList.add('active'); btn.classList.remove('inactive');
      render();
    });
  });
  search?.addEventListener('input', render);
})();