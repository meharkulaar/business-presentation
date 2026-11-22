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
  if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].indexOf(e.key)>=0){e.preventDefault();next();}
  else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(e.key)>=0){e.preventDefault();prev();}
  else if(e.key==='Home')show(0,1);else if(e.key==='End')show(slides.length-1,-1);
  else if(e.key==='f'||e.key==='F'){if(!document.fullscreenElement)document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();else document.exitFullscreen();}
  else if(e.key==='l'||e.key==='L')document.body.classList.toggle('lite');
});
addEventListener('click',function(e){if(e.clientX<innerWidth*.25)prev();else next();});
window.deck={show:show,next:next,prev:prev,get i(){return i;},slides:slides};
show(0,1);
})();
