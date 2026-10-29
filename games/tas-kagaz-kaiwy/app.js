import { LearningAI, winner, choices } from './rules.js';
import { hand } from './icons.js';
const D = {
  kk:{title:'Тас, қағаз, қайшы',back:'← Ойындарға',intro:'ИИ сенің әдеттеріңді үйренеді. Таңдауыңды өзгертіп, роботты алдап көр!',you:'Сен',opponent:'ИИ робот',rock:'Тас',paper:'Қағаз',scissors:'Қайшы',round:'Раунд',memory:'Үйренген үлгі',ready:'Таңдауыңды жаса!',reveal:'Тас… қағаз… қайшы!',win:'Сен жеңдің!',lose:'Бұл жолы ИИ жеңді',draw:'Тең түсті!',wins:'Жеңістер',losses:'Жеңілістер',draws:'Тең ойындар',pick:'Сенің жүрісің',keys:'Пернетақта: 1 · 2 · 3',history:'Соңғы раундтар',empty:'Алғашқы раундты баста.',rulesTitle:'Үш белгі. Мың мүмкіндік.',rules:'Тас қайшыны жеңеді. Қайшы қағазды қияды. Қағаз тасты орайды.',reset:'Есеп пен ИИ жадын тазалау',note:'Python түпнұсқасының браузерлік бейімдеуі. Камера режимдері тек Python нұсқасында бар.'},
  ru:{title:'Камень, ножницы, бумага',back:'← К играм',intro:'ИИ изучает твои привычки. Меняй тактику и попробуй перехитрить робота!',you:'Ты',opponent:'ИИ робот',rock:'Камень',paper:'Бумага',scissors:'Ножницы',round:'Раунд',memory:'Изучено шаблонов',ready:'Сделай свой выбор!',reveal:'Камень… ножницы… бумага!',win:'Ты победил!',lose:'В этот раз победил ИИ',draw:'Ничья!',wins:'Победы',losses:'Поражения',draws:'Ничьи',pick:'Твой ход',keys:'Клавиши: 1 · 2 · 3',history:'Последние раунды',empty:'Начни первый раунд.',rulesTitle:'Три знака. Тысяча возможностей.',rules:'Камень побеждает ножницы. Ножницы режут бумагу. Бумага накрывает камень.',reset:'Сбросить счёт и память ИИ',note:'Браузерная адаптация Python-оригинала. Режимы камеры доступны только в Python-версии.'},
  en:{title:'Rock, Paper, Scissors',back:'← Back to games',intro:'AI learns your habits. Switch up your moves and try to outsmart the robot!',you:'You',opponent:'AI robot',rock:'Rock',paper:'Paper',scissors:'Scissors',round:'Round',memory:'Patterns learned',ready:'Make your move!',reveal:'Rock… paper… scissors!',win:'You win!',lose:'AI wins this one',draw:'A draw!',wins:'Wins',losses:'Losses',draws:'Draws',pick:'Your move',keys:'Keyboard: 1 · 2 · 3',history:'Recent rounds',empty:'Play your first round.',rulesTitle:'Three signs. A thousand possibilities.',rules:'Rock beats scissors. Scissors cut paper. Paper covers rock.',reset:'Reset score and AI memory',note:'Browser adaptation of the Python original. Camera modes are available only in the Python version.'}
};
const $ = id => document.getElementById(id);
let lang='kk';try{const saved=localStorage.getItem('python-games-language');if(D[saved])lang=saved;}catch{}
let ai=new LearningAI(),scores={win:0,lose:0,draw:0},history=[],last=null,busy=false,timer=null,ticks=0;
const arena=document.querySelector('.arena');
function render(){
  const t=D[lang];document.documentElement.lang=lang;document.title=`${t.title} · Python Games`;$('language').value=lang;
  for(const id of ['title','back','intro','you','opponent','pick','keys','rules','reset','note'])$(id).textContent=t[id];
  $('rules-title').textContent=t.rulesTitle;$('history-title').textContent=t.history;$('no-history').textContent=t.empty;$('no-history').hidden=history.length>0;
  $('round').textContent=`${t.round} ${scores.win+scores.lose+scores.draw+1}`;$('memory').textContent=`${t.memory}: ${ai.patterns.size}`;
  for(const [id,key] of [['wins','win'],['losses','lose'],['draws','draw']]){$(id).textContent=scores[key];$(id+'-label').textContent=t[id];}
  $('result').textContent=busy?t.reveal:last?t[last.result]:t.ready;
  $('player-hand').innerHTML=hand(last&&!busy?last.player:'rock');$('ai-hand').innerHTML=hand(last&&!busy?last.opponent:'rock');
  $('player-choice').textContent=last&&!busy?t[last.player]:'?';$('ai-choice').textContent=last&&!busy?t[last.opponent]:'?';
  arena.classList.toggle('revealing',busy);arena.dataset.result=busy?'':last?.result||'';
  document.querySelectorAll('[data-choice]').forEach(b=>{b.disabled=busy;b.querySelector('strong').textContent=t[b.dataset.choice];b.setAttribute('aria-label',t[b.dataset.choice]);});
  $('history').replaceChildren(...history.slice(-5).reverse().map((entry,index)=>{
    const li=document.createElement('li'),number=document.createElement('span'),pair=document.createElement('span'),result=document.createElement('b');
    number.textContent=`${history.length-index}`;pair.className='mini-hand';pair.innerHTML=hand(entry.player)+hand(entry.opponent);pair.setAttribute('aria-label',`${t.you}: ${t[entry.player]}, ${t.opponent}: ${t[entry.opponent]}`);result.textContent=t[entry.result];li.append(number,pair,result);return li;
  }));
}
function play(player){
  if(busy)return;
  // Commit the AI choice before learning this round's player choice.
  const opponent=ai.predict();busy=true;ticks=3;$('countdown').textContent=ticks;render();
  timer=setInterval(()=>{
    ticks--;if(ticks>0){$('countdown').textContent=ticks;return;}
    clearInterval(timer);timer=null;busy=false;last={player,opponent,result:winner(player,opponent)};ai.learn(player);scores[last.result]++;history.push(last);$('countdown').textContent='✦';render();
  },300);
}
document.querySelectorAll('[data-choice]').forEach(b=>{b.querySelector('.choice-icon').innerHTML=hand(b.dataset.choice);b.addEventListener('click',()=>play(b.dataset.choice));});
$('reset').onclick=()=>{clearInterval(timer);timer=null;busy=false;ai=new LearningAI();scores={win:0,lose:0,draw:0};history=[];last=null;$('countdown').textContent='✦';render();};
$('language').onchange=e=>{lang=e.target.value;try{localStorage.setItem('python-games-language',lang);}catch{}render();};
document.addEventListener('keydown',e=>{if(e.repeat||e.target.matches('input,select,textarea'))return;const move=choices[Number(e.key)-1];if(move){e.preventDefault();play(move);}});
window.addEventListener('pagehide',()=>clearInterval(timer));render();
