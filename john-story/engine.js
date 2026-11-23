(function(){
var stage=document.getElementById('stage');
window.FITOPT=window.FITOPT||{safe:0,exact:false};
function fit(){
  var o=window.FITOPT,m=Math.max(0,Math.min(.12,+o.safe||0));
  var W=innerWidth,Hh=innerHeight,W2=W*(1-2*m),H2=Hh*(1-2*m),a=W2/H2,w,h,sc;
  if(o.exact){w=1440;h=810;sc=Math.min(W2/1440,H2/810);}
  else{if(a>=1440/810){h=810;w=Math.round(810*a);}else{w=1440;h=Math.round(1440/a);}sc=W2/w;}
  stage.style.width=w+'px';stage.style.height=h+'px';stage.style.marginLeft=(-w/2)+'px';stage.style.marginTop=(-h/2)+'px';
  stage.style.transform='scale('+sc+')';
  stage.style.setProperty('--ex',((h-810)/2)+'px');stage.style.setProperty('--exw',((w-1440)/2)+'px');
  window.FITINFO={W:W,H:Hh,dpr:window.devicePixelRatio||1,sc:sc};
  var narrow=(w/h)<1.7,wide=(w/h)>1.9,parH=narrow?'xMidYMax meet':'xMidYMax slice',parF=(narrow||wide)?'xMidYMax meet':'xMidYMax slice';
  [].slice.call(document.querySelectorAll('.halfL svg')).forEach(function(v){if(v.getAttribute('preserveAspectRatio')!==parH)v.setAttribute('preserveAspectRatio',parH);});
  [].slice.call(document.querySelectorAll('.ratSvg')).forEach(function(v){if(v.getAttribute('preserveAspectRatio')!==parF)v.setAttribute('preserveAspectRatio',parF);});
  stage.classList.toggle('narrow',narrow);stage.classList.toggle('wide',wide);
  if(wide){var pad=((w-1440)/2)/w*100;stage.style.setProperty('--wfa',(pad-1)+'%');stage.style.setProperty('--wfb',(pad+5)+'%');}
}
window.__refit=fit;
addEventListener('resize',fit);addEventListener('orientationchange',function(){setTimeout(fit,200);});
document.addEventListener('fullscreenchange',function(){setTimeout(fit,60);setTimeout(fit,400);});
document.addEventListener('visibilitychange',function(){if(!document.hidden)setTimeout(fit,100);});
fit();

var slides=[].slice.call(document.querySelectorAll('.slide')),i=0;
var NEED_TOTAL=7, nwShown=0, cdaMax=23185466;
function frags(s){return [].slice.call(s.querySelectorAll('.f'));}
function fmt(v){return '$'+Math.round(v).toLocaleString('en-CA');}
function short(v){return v>=1e6?'$'+(v/1e6).toFixed(2)+'M':fmt(v);}

function runCount(b,animate){
  var to=+b.dataset.to,pre=b.dataset.pre||'',suf=b.dataset.suf||'';
  function put(v){b.textContent=pre+Math.round(v).toLocaleString('en-CA')+suf;}
  cancelAnimationFrame(b._r);
  if(!animate){put(to);return;}
  var t0=performance.now(),d=1600;
  (function f(t){var p=Math.max(0,Math.min(1,(t-t0)/d)),e=1-Math.pow(1-p,3);put(to*e);if(p<1)b._r=requestAnimationFrame(f);})(t0);
}
function counters(scope,animate){
  [].slice.call(scope.querySelectorAll('.cnt')).forEach(function(b){
    var fr=b.closest('.f');
    if(!fr||fr.classList.contains('on'))runCount(b,animate);
    else{cancelAnimationFrame(b._r);b.textContent=(b.dataset.pre||'')+'0'+(b.dataset.suf||'');}
  });
}

var hud=document.getElementById('hud');
function tweenNw(to){
  var el=document.getElementById('hNw'),from=nwShown,t0=performance.now();nwShown=to;
  cancelAnimationFrame(el._r);
  (function f(t){var p=Math.max(0,Math.min(1,(t-t0)/900)),e=1-Math.pow(1-p,3);el.textContent=short(from+(to-from)*e);if(p<1)el._r=requestAnimationFrame(f);})(t0);
}
var bigT;
function updHud(s){
  clearTimeout(bigT);
  var wasOn=hud.classList.contains('on'),big=s.classList.contains('sScore');
  if(!big)hud.classList.remove('xpand');
  if(!s.dataset.hud||s.classList.contains('sFull')||s.classList.contains('sRat')){hud.classList.remove('on');return;}
  hud.classList.add('on');
  if(big){var hb=document.getElementById('hudBig');[].slice.call(hb.querySelectorAll('.cnt')).forEach(function(b){b.textContent=(b.dataset.pre||'')+'0'+(b.dataset.suf||'');});
    bigT=setTimeout(function(){hud.classList.add('xpand');bigT=setTimeout(function(){counters(hb,true);},1000);},wasOn?350:900);}
  var age=+s.dataset.age;
  document.getElementById('hAge').textContent=age;
  document.getElementById('hDot').style.left=((age-40)/50*100)+'%';
  tweenNw(+s.dataset.nw);
  var c=+s.dataset.cda;document.getElementById('hCda').textContent=c?'up to '+short(c):'none yet';
  document.getElementById('hBf').style.height=(c/cdaMax*100)+'%';
  var lit=(s.dataset.needs||'').split(',').filter(String).map(Number);
  [].slice.call(document.querySelectorAll('#hOrn i')).forEach(function(o,k){o.classList.toggle('on',lit.indexOf(k)>=0);});
  var r=s.dataset.rules||'000';
  [].slice.call(document.querySelectorAll('#hRu em')).forEach(function(o,k){o.classList.toggle('on',r[k]==='1');});
}

var lastAge=null,lastCda=0;
function timePass(a0,a1){
  var tp=document.getElementById('tp'),y=document.getElementById('tpY'),g=document.getElementById('tpA');if(!tp)return;
  var s=slides[i];
  tp.classList.remove('on','out');void tp.offsetWidth;tp.classList.add('on');
  var t0=performance.now(),d=1500;tp.classList.remove('hold');
  (function f(t){var p=Math.max(0,Math.min(1,(t-t0)/d)),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2,a=Math.round(a0+(a1-a0)*e);y.textContent=1986+a;g.textContent='John is '+a;if(p<1)requestAnimationFrame(f);else tp.classList.add('hold');})(t0);
  clearTimeout(tp._t1);clearTimeout(tp._t2);
  tp._t1=setTimeout(function(){tp.classList.add('out');
    // replay the slide's entrance now that the clock has gone
    if(slides[i]===s){s.classList.remove('active');void s.offsetWidth;s.classList.add('active');}
  },2550);
  tp._t2=setTimeout(function(){tp.classList.remove('on','out','hold');},3100);
}
var curt=document.getElementById('curt'),curtT;
function curtain(s,dir,clocked){
  clearTimeout(curtT);curt.classList.remove('shut','open');
  if(dir<=0||!(s===slides[1]||s===slides[slides.length-1])||document.body.classList.contains('reduce'))return;
  curt.classList.add('shut');void curt.offsetWidth;
  curtT=setTimeout(function(){curt.classList.remove('shut');curt.classList.add('open');
    if(slides[i]===s){s.classList.remove('active');void s.offsetWidth;s.classList.add('active');}},clocked?2600:120);
}
var actEl=document.getElementById('act'),actT1,actT2;
function showAct(s,dir,clocked){
  clearTimeout(actT1);clearTimeout(actT2);actEl.classList.remove('on');
  if(dir<=0||!s.dataset.act)return;
  actT1=setTimeout(function(){if(slides[i]!==s)return;
    document.getElementById('actL').textContent=s.dataset.actl;document.getElementById('actT').innerHTML=s.dataset.act;
    actEl.classList.toggle('ms',s.dataset.actl!=='John takes action');
    actEl.classList.add('on');actT2=setTimeout(function(){actEl.classList.remove('on');},4500);},clocked?3200:700);
}
function pour(){
  var c=document.querySelector('.hCda');if(!c)return;
  for(var k=0;k<6;k++){var e=document.createElement('i');e.className='coinP';e.style.left=(4+Math.random()*16)+'px';e.style.animationDelay=(k*.12)+'s';c.appendChild(e);(function(e){setTimeout(function(){e.remove();},1600);})(e);}
}
function show(n,dir){
  n=Math.max(0,Math.min(slides.length-1,n));
  slides[i].classList.remove('active');
  var s=slides[n];i=n;
  if(dir<0)s.classList.add('snap');
  frags(s).forEach(function(f){f.classList.toggle('on',dir<0);});
  s.classList.add('active');
  if(dir<0){
    // coming back: show the finished slide straight away, no replays
    try{s.getAnimations({subtree:true}).forEach(function(a){var t=a.effect&&a.effect.getTiming&&a.effect.getTiming();if(t&&t.iterations!==Infinity)a.finish();});}catch(_){}
    setTimeout(function(){s.classList.remove('snap');},60);
  }
  counters(s,dir>=0);
  var ag=s.dataset.age?+s.dataset.age:null;
  var clocked=false;
  if(dir>0&&ag!==null&&lastAge!==null&&ag-lastAge>=3&&!document.body.classList.contains('reduce')){timePass(lastAge,ag);clocked=true;}
  showAct(s,dir,clocked);
  curtain(s,dir,clocked);
  if(ag!==null)lastAge=ag;
  var cd=s.dataset.cda?+s.dataset.cda:0;if(dir>0&&cd>lastCda+1)pour();lastCda=cd;
  updHud(s);
  document.getElementById('prog').style.width=((n+1)/slides.length*100)+'%';
}
function restart(){
  slides.forEach(function(s){s.classList.remove('active','snap');frags(s).forEach(function(f){f.classList.remove('on');});});
  lastAge=null;lastCda=0;nwShown=0;var tp=document.getElementById('tp');if(tp)tp.classList.remove('on');
  i=0;show(0,1);
}
function next(){
  var f=frags(slides[i]).filter(function(x){return !x.classList.contains('on');});
  if(f.length){f[0].classList.add('on');counters(f[0].classList.contains('cnt')?f[0].parentNode:f[0],true);return;}
  if(i<slides.length-1)show(i+1,1);
}
function prev(){
  var on=frags(slides[i]).filter(function(x){return x.classList.contains('on');});
  if(on.length){on[on.length-1].classList.remove('on');return;}
  if(i>0)show(i-1,-1);
}
addEventListener('keydown',function(e){
  if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].indexOf(e.key)>=0){e.preventDefault();window.deck.next();}
  else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(e.key)>=0){e.preventDefault();window.deck.prev();}
  else if(e.key==='Home')show(0,1);else if(e.key==='End')show(slides.length-1,-1);
  else if((e.key==='f'||e.key==='F')&&e.target.tagName!=='INPUT'){if(!document.fullscreenElement)document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();else document.exitFullscreen();}
  
});
addEventListener('click',function(e){if(e.target.closest('#ui,.panel,#timer'))return;if(document.body.classList.contains('noclick'))return;if(e.clientX<innerWidth*.25)window.deck.prev();else window.deck.next();});
window.deck={show:show,next:next,prev:prev,restart:restart,get i(){return i;},slides:slides};
show(0,1);
})();
/* ===== UI: fullscreen, TOC with hide, name/title editor ===== */
(function(){
var D=window.deck,slides=D.slides;
var $=function(id){return document.getElementById(id);};
function fs(){if(!document.fullscreenElement){(document.documentElement.requestFullscreen||function(){}).call(document.documentElement);}else document.exitFullscreen();}
$('bFs').onclick=function(e){e.stopPropagation();fs();this.blur();};
['ui','toc','edit','set'].forEach(function(id){$(id).addEventListener('click',function(e){e.stopPropagation();});if(id!=='ui')$(id).addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')e.stopPropagation();});});
[].slice.call(document.querySelectorAll('.pX')).forEach(function(b){b.onclick=function(){b.closest('.panel').classList.remove('open');};});
function toggle(id){var p=$(id),o=!p.classList.contains('open');document.querySelectorAll('.panel').forEach(function(x){x.classList.remove('open');});if(o){p.classList.add('open');if(id==='toc')buildToc();if(id==='edit')buildEdit();}}
$('bToc').onclick=function(){toggle('toc');this.blur();};$('bSet').onclick=function(){toggle('set');this.blur();};$('bEdit').onclick=function(){toggle('edit');this.blur();};
addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;if(e.key==='t'||e.key==='T')toggle('toc');if(e.key==='e'||e.key==='E')toggle('edit');},true);
/* hidden slides */
var hidden={};try{hidden=JSON.parse(localStorage.getItem('jsHidden')||'{}');}catch(_){}
function saveH(){try{localStorage.setItem('jsHidden',JSON.stringify(hidden));}catch(_){}}
var _show=D.show;
function vis(n,dir){var k=n;while(k>0&&k<slides.length-1&&hidden[k])k+=dir;return hidden[k]?null:k;}
var _n=D.next,_p=D.prev;
D.next=function(){var s=slides[D.i];var left=[].slice.call(s.querySelectorAll('.f')).some(function(f){return !f.classList.contains('on');});if(left){_n();return;}var k=vis(D.i+1,1);if(k!==null&&k!==D.i)_show(k,1);};
D.prev=function(){var s=slides[D.i];var any=s.querySelector('.f.on');if(any){_p();return;}var k=vis(D.i-1,-1);if(k!==null&&k!==D.i)_show(k,-1);};
function title(s){var t=s.querySelector('h1,h2,.kick');return t?t.textContent.trim().replace(/\s+/g,' ').slice(0,46):'Slide';}
function buildToc(){var L=$('tocL');L.innerHTML='';slides.forEach(function(s,k){var d=document.createElement('div');d.className='tI'+(k===D.i?' cur':'')+(hidden[k]?' hid':'');
  d.innerHTML='<b>'+(k+1)+'</b><span></span>'+(k?'<em title="Hide / show">'+(hidden[k]?'&#10005;':'&#128065;')+'</em>':'');d.querySelector('span').textContent=title(s);
  d.onclick=function(e){if(e.target.tagName==='EM'){hidden[k]=!hidden[k];if(!hidden[k])delete hidden[k];saveH();buildToc();return;}_show(k,1);buildToc();};L.appendChild(d);});}
$('tocAll').onclick=function(){hidden={};saveH();buildToc();};
/* names + title editor */
var DEF={John:'John',Emma:'Emma',Lily:'Lily',Max:'Max',Mehar:'Mehar',David:'David',Sarah:'Sarah',Raj:'Raj',Jake:'Jake'};
var LBL={John:'Main character',Emma:'His wife',Lily:'Daughter',Max:'Son',Mehar:'Advisor',David:'Accountant',Sarah:'Lawyer',Raj:'Partner dentist',Jake:'The twin'};
var cur=Object.assign({},DEF);var T0={t1:$('t1').textContent,t2:$('t2').textContent};
function walk(fn){var w=document.createTreeWalker($('stage').querySelector('.deck'),NodeFilter.SHOW_TEXT,null);var n;while((n=w.nextNode()))fn(n);}
function esc(x){return x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function apply(map){walk(function(n){var v=n.nodeValue,o=v;Object.keys(map).forEach(function(k){if(cur[k]!==map[k]){v=v.replace(new RegExp('\\b'+esc(cur[k])+'\\b','g'),'\u0000'+k+'\u0000');}});
  if(v!==o){v=v.replace(/\u0000(\w+)\u0000/g,function(_,k){return map[k];});n.nodeValue=v;}});cur=Object.assign({},map);}
function setTitle(t){if(t.t1)$('t1').textContent=t.t1;if(t.t2)$('t2').textContent=t.t2;}
var saved={};try{saved=JSON.parse(localStorage.getItem('jsNames')||'{}');}catch(_){}
var clinicName='Smile Dental';
function fitClinic(){[].slice.call(document.querySelectorAll('text.clinicNm')).forEach(function(t){t.removeAttribute('textLength');t.removeAttribute('lengthAdjust');
  var mw=+t.dataset.w||146,l=0;try{l=t.getComputedTextLength();}catch(_){}if(l>mw){t.setAttribute('textLength',mw);t.setAttribute('lengthAdjust','spacingAndGlyphs');}});}
function setClinic(nm){clinicName=nm;[].slice.call(document.querySelectorAll('text.clinicNm')).forEach(function(t){var n=+t.dataset.n;t.textContent=nm.toUpperCase()+(n>1?' #'+n:'');});fitClinic();}
window.__fitClinic=fitClinic;
if(saved.clinic)setClinic(saved.clinic);
if(saved.names)apply(Object.assign({},DEF,saved.names));if(saved.title)setTitle(saved.title);
function buildEdit(){var L=$('editL');L.innerHTML='';
  var add=function(id,lab,val){var r=document.createElement('div');r.className='eR';r.innerHTML='<label></label><input>';r.querySelector('label').textContent=lab;var i=r.querySelector('input');i.value=val;i.dataset.k=id;L.appendChild(r);};
  add('t1','Title line 1 (after the hat T)',$('t1').textContent);add('t2','Title line 2',$('t2').textContent);
  add('clinic','Clinic name',clinicName);
  Object.keys(DEF).forEach(function(k){add(k,LBL[k],cur[k]);});}
$('edSave').onclick=function(){var m={},t={};[].slice.call(document.querySelectorAll('#editL input')).forEach(function(i){var v=i.value.trim();if(!v)return;if(i.dataset.k==='clinic'){setClinic(v);return;}if(i.dataset.k==='t1'||i.dataset.k==='t2')t[i.dataset.k]=v;else m[i.dataset.k]=v;});
  apply(Object.assign({},cur,m));setTitle(t);try{localStorage.setItem('jsNames',JSON.stringify({names:cur,clinic:clinicName,title:{t1:$('t1').textContent,t2:$('t2').textContent}}));}catch(_){}$('edit').classList.remove('open');};
$('edReset').onclick=function(){apply(DEF);setTitle(T0);setClinic('Smile Dental');try{localStorage.removeItem('jsNames');}catch(_){}buildEdit();};
})();

/* ===== Settings ===== */
(function(){
var D=window.deck,$=function(id){return document.getElementById(id);},B=document.body;
var OPTS=[['snow','Snow & sparkle effects','Turn off on slower laptops',true],
  ['motion','Smooth animations','Off = everything appears instantly',true],
  ['hud','Story bar at the bottom','Age, net worth, CDA, 7 needs, 3 rules',true],
  ['badge','Mehar’s process badges','"Step 3 of 7" in the top-left',true],
  ['intl','“For internal use only” tag','',true],
  ['click','Click anywhere to advance','Off = keyboard or clicker only',true],
  ['timer','Presenter timer','Counts up to your 40-minute target',false]];
var SCR=[['autofit','Auto screen optimizer','Re-fits automatically when you AirPlay, plug in HDMI, change resolution or resize',true],
  ['exact','Keep exact 16:9 shape','Adds black bars instead of stretching to the screen; use if a TV crops or distorts',false]];
var st={};try{st=JSON.parse(localStorage.getItem('jsSet')||'{}');}catch(_){}
OPTS.concat(SCR).forEach(function(o){if(!(o[0] in st))st[o[0]]=o[3];});if(!('safe' in st))st.safe=0;
function applyS(){B.classList.toggle('lite',!st.snow);B.classList.toggle('reduce',!st.motion);B.classList.toggle('nohud',!st.hud);
  B.classList.toggle('nobadge',!st.badge);B.classList.toggle('nointl',!st.intl);B.classList.toggle('noclick',!st.click);B.classList.toggle('timer',!!st.timer);
  window.FITOPT.safe=(+st.safe||0)/100;window.FITOPT.exact=!!st.exact;if(window.__refit)window.__refit();
  try{localStorage.setItem('jsSet',JSON.stringify(st));}catch(_){}}
var lastSig='';setInterval(function(){if(!st.autofit)return;var sig=[innerWidth,innerHeight,window.devicePixelRatio,screen.width,screen.height,screen.availWidth,screen.availHeight].join('x');
  if(sig!==lastSig){lastSig=sig;if(window.__refit)window.__refit();var inf=document.getElementById('scrInfo');if(inf)inf.textContent=scrText();}},700);
function scrText(){var f=window.FITINFO||{};return 'Detected: '+f.W+' \u00d7 '+f.H+' window \u00b7 '+screen.width+' \u00d7 '+screen.height+' screen \u00b7 scale '+(f.sc||1).toFixed(2);}
function build(){var L=$('setL');L.innerHTML='';
  var r=document.createElement('button');r.className='sBig';r.textContent='↻  Restart presentation from the beginning';r.onclick=function(){restartAll();$('set').classList.remove('open');};L.appendChild(r);
  OPTS.forEach(function(o){var d=document.createElement('div');d.className='sRow';d.innerHTML='<span></span><i class="tg"></i>';
    d.querySelector('span').innerHTML=o[1]+(o[2]?'<em>'+o[2]+'</em>':'');var t=d.querySelector('.tg');t.classList.toggle('on',!!st[o[0]]);
    t.onclick=function(){st[o[0]]=!st[o[0]];t.classList.toggle('on',st[o[0]]);applyS();};L.appendChild(d);});
  var hd=document.createElement('div');hd.className='sHead';hd.textContent='Screen';L.appendChild(hd);
  SCR.forEach(function(o){var d=document.createElement('div');d.className='sRow';d.innerHTML='<span></span><i class="tg"></i>';
    d.querySelector('span').innerHTML=o[1]+'<em>'+o[2]+'</em>';var t=d.querySelector('.tg');t.classList.toggle('on',!!st[o[0]]);
    t.onclick=function(){st[o[0]]=!st[o[0]];t.classList.toggle('on',st[o[0]]);applyS();inf.textContent=scrText();};L.appendChild(d);});
  var sm=document.createElement('div');sm.className='sRow';sm.innerHTML='<span>TV safe margins<em>Shrinks the slide slightly if the TV cuts off the edges (overscan)</em></span><div class="stp"><button>&minus;</button><b></b><button>+</button></div>';
  var sb=sm.querySelector('b');sb.textContent=st.safe+'%';var bs=sm.querySelectorAll('button');
  bs[0].onclick=function(){st.safe=Math.max(0,st.safe-1);sb.textContent=st.safe+'%';applyS();inf.textContent=scrText();};
  bs[1].onclick=function(){st.safe=Math.min(10,st.safe+1);sb.textContent=st.safe+'%';applyS();inf.textContent=scrText();};L.appendChild(sm);
  var rf=document.createElement('div');rf.className='sRow';rf.innerHTML='<span id="scrInfo"></span><button class="rfB">Re-fit now</button>';var inf=rf.querySelector('#scrInfo');inf.textContent=scrText();
  rf.querySelector('.rfB').onclick=function(){if(window.__refit)window.__refit();inf.textContent=scrText();};L.appendChild(rf);
  var k=document.createElement('div');k.className='sRow';k.innerHTML='<span>Keys<em>→ next · ← back · F full screen · B black screen · R restart · T slides · S settings</em></span>';L.appendChild(k);}
$('setReset').onclick=function(){st={};OPTS.concat(SCR).forEach(function(o){st[o[0]]=o[3];});st.safe=0;applyS();build();};
var t0=null;function fmt(ms){var s=Math.floor(ms/1000);return Math.floor(s/60)+':'+('0'+s%60).slice(-2);}
setInterval(function(){var el=$('timer');if(!el)return;if(t0===null){el.textContent='0:00 / 40:00';return;}var ms=Date.now()-t0;el.textContent=fmt(ms)+' / 40:00';el.classList.toggle('over',ms>40*60000);},500);
$('timer').onclick=function(e){e.stopPropagation();t0=Date.now();};
addEventListener('keydown',function(e){if(t0===null&&D.i>0)t0=Date.now();},true);
addEventListener('click',function(){if(t0===null)setTimeout(function(){if(D.i>0&&t0===null)t0=Date.now();},50);});
function restartAll(){document.querySelectorAll('.panel').forEach(function(x){x.classList.remove('open');});B.classList.remove('black');t0=null;D.restart();}
addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;var k=e.key;
  if(k==='b'||k==='B'||k==='.'){B.classList.toggle('black');e.stopImmediatePropagation();}
  else if(k==='r'||k==='R')restartAll();
  else if(k==='s'||k==='S'){var p=$('set'),o=!p.classList.contains('open');document.querySelectorAll('.panel').forEach(function(x){x.classList.remove('open');});if(o){p.classList.add('open');build();}}
},true);
var _o=$('bSet').onclick;$('bSet').onclick=function(){_o.call(this);if($('set').classList.contains('open'))build();};
applyS();
})();

/* ===== interactive chart hover ===== */
(function(){
[].slice.call(document.querySelectorAll('svg.hov')).forEach(function(svg){
  var pts=[].slice.call(svg.querySelectorAll('.hvD i')).map(function(e){return e.dataset;});
  var G=svg.querySelector('.hvG'),L=svg.querySelector('.hvL'),cd=svg.querySelector('.hvC.db'),cc=svg.querySelector('.hvC.cv'),T=svg.querySelector('.hvT'),hit=svg.querySelector('.hvHit');
  var tx=[0,1,2,3].map(function(k){return T.querySelector('.t'+k);});
  function at(ev){var p=svg.createSVGPoint();p.x=ev.clientX;p.y=ev.clientY;var q=p.matrixTransform(svg.getScreenCTM().inverse());
    var best=pts[0],bd=1e9;pts.forEach(function(d){var dd=Math.abs(+d.x-q.x);if(dd<bd){bd=dd;best=d;}});return best;}
  hit.addEventListener('mousemove',function(ev){var d=at(ev);G.classList.add('on');
    L.setAttribute('x1',d.x);L.setAttribute('x2',d.x);cd.setAttribute('cx',d.x);cd.setAttribute('cy',d.ydb);cc.setAttribute('cx',d.x);cc.setAttribute('cy',d.ycv);
    var tX=+d.x+16;if(tX>1260-240)tX=+d.x-246;var tY=Math.max(10,Math.min(+d.ydb-30,280));T.setAttribute('transform','translate('+tX+','+tY+')');
    tx[0].textContent='Age '+d.a+'  ·  '+(1986+(+d.a));tx[1].textContent='Death benefit: '+d.db;tx[2].textContent='Cash value: '+d.cv;tx[3].textContent='Premiums paid: '+d.pr;});
  hit.addEventListener('mouseleave',function(){G.classList.remove('on');});
  hit.addEventListener('click',function(e){e.stopPropagation();});
});
})();
