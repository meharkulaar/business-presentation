(function(){
var stage=document.getElementById('stage');
function fit(){var s=Math.min(innerWidth/1440,innerHeight/810);stage.style.transform='scale('+s+')';}
addEventListener('resize',fit);fit();

var slides=[].slice.call(document.querySelectorAll('.slide')),i=0;
var NEED_TOTAL=7, nwShown=0, cdaMax=14183158;
function frags(s){return [].slice.call(s.querySelectorAll('.f'));}
function fmt(v){return '$'+Math.round(v).toLocaleString('en-CA');}
function short(v){return v>=1e6?'$'+(v/1e6).toFixed(2)+'M':fmt(v);}

function runCount(b,animate){
  var to=+b.dataset.to,pre=b.dataset.pre||'',suf=b.dataset.suf||'';
  function put(v){b.textContent=pre+Math.round(v).toLocaleString('en-CA')+suf;}
  cancelAnimationFrame(b._r);
  if(!animate){put(to);return;}
  var t0=performance.now(),d=1600;
  (function f(t){var p=Math.min(1,(t-t0)/d),e=1-Math.pow(1-p,3);put(to*e);if(p<1)b._r=requestAnimationFrame(f);})(t0);
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
  (function f(t){var p=Math.min(1,(t-t0)/900),e=1-Math.pow(1-p,3);el.textContent=short(from+(to-from)*e);if(p<1)el._r=requestAnimationFrame(f);})(t0);
}
function updHud(s){
  if(!s.dataset.hud){hud.classList.remove('on');return;}
  hud.classList.add('on');
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

function show(n,dir){
  n=Math.max(0,Math.min(slides.length-1,n));
  slides[i].classList.remove('active');
  var s=slides[n];i=n;
  frags(s).forEach(function(f){f.classList.toggle('on',dir<0);});
  s.classList.add('active');
  // restart CSS animations on entry
  [].slice.call(s.querySelectorAll('.ln,.bkFill')).forEach(function(e){e.style.animation='none';e.offsetWidth;e.style.animation='';});
  counters(s,dir>=0);
  updHud(s);
  document.getElementById('prog').style.width=((n+1)/slides.length*100)+'%';
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
  else if(e.key==='l'||e.key==='L')document.body.classList.toggle('lite');
});
addEventListener('click',function(e){if(e.target.closest('#ui,.panel'))return;if(e.clientX<innerWidth*.25)window.deck.prev();else window.deck.next();});
window.deck={show:show,next:next,prev:prev,get i(){return i;},slides:slides};
show(0,1);
})();
/* ===== UI: fullscreen, TOC with hide, name/title editor ===== */
(function(){
var D=window.deck,slides=D.slides;
var $=function(id){return document.getElementById(id);};
function fs(){if(!document.fullscreenElement){(document.documentElement.requestFullscreen||function(){}).call(document.documentElement);}else document.exitFullscreen();}
$('bFs').onclick=function(e){e.stopPropagation();fs();this.blur();};
['ui','toc','edit'].forEach(function(id){$(id).addEventListener('click',function(e){e.stopPropagation();});if(id!=='ui')$(id).addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')e.stopPropagation();});});
[].slice.call(document.querySelectorAll('.pX')).forEach(function(b){b.onclick=function(){b.closest('.panel').classList.remove('open');};});
function toggle(id){var p=$(id),o=!p.classList.contains('open');document.querySelectorAll('.panel').forEach(function(x){x.classList.remove('open');});if(o){p.classList.add('open');if(id==='toc')buildToc();if(id==='edit')buildEdit();}}
$('bToc').onclick=function(){toggle('toc');this.blur();};$('bEdit').onclick=function(){toggle('edit');this.blur();};
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
if(saved.names)apply(Object.assign({},DEF,saved.names));if(saved.title)setTitle(saved.title);
function buildEdit(){var L=$('editL');L.innerHTML='';
  var add=function(id,lab,val){var r=document.createElement('div');r.className='eR';r.innerHTML='<label></label><input>';r.querySelector('label').textContent=lab;var i=r.querySelector('input');i.value=val;i.dataset.k=id;L.appendChild(r);};
  add('t1','Title line 1 (after the hat T)',$('t1').textContent);add('t2','Title line 2',$('t2').textContent);
  Object.keys(DEF).forEach(function(k){add(k,LBL[k],cur[k]);});}
$('edSave').onclick=function(){var m={},t={};[].slice.call(document.querySelectorAll('#editL input')).forEach(function(i){var v=i.value.trim();if(!v)return;if(i.dataset.k==='t1'||i.dataset.k==='t2')t[i.dataset.k]=v;else m[i.dataset.k]=v;});
  apply(Object.assign({},cur,m));setTitle(t);try{localStorage.setItem('jsNames',JSON.stringify({names:cur,title:{t1:$('t1').textContent,t2:$('t2').textContent}}));}catch(_){}$('edit').classList.remove('open');};
$('edReset').onclick=function(){apply(DEF);setTitle(T0);try{localStorage.removeItem('jsNames');}catch(_){}buildEdit();};
})();
