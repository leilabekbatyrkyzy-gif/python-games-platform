import { generateMaze, solveMaze } from './maze.js';
const translations = {
  kk: { title:'Ақылды лабиринт', back:'← Ойындарға', intro:'Шығатын жолды тап. Қаласаң, BFS көмекшісі дұрыс бағытты көрсетеді.', difficulty:'Күрделілік', levels:['Оңай','Орташа','Қиын'], solve:'AI жолды көрсету', reset:'Жаңа лабиринт', sound:'Дыбыс', on:'қосулы', off:'өшірулі', help:'Бағыттауыштар немесе WASD, экран батырмалары не свайп. Enter — көмек, Space — жаңа ойын.', note:'labirint.py негізіндегі браузерлік бейімдеу. Көк жол — BFS шешімі; оны көрсету жеңіс болып саналмайды.', player:'● Сен', goal:'■ Мақсат', playing:'Мақсатқа жет!', won:'ЖЕҢІС! Мақсатқа жеттің.', solved:'BFS жолы көрсетілді', steps:'қадам', up:'Жоғары', down:'Төмен', left:'Солға', right:'Оңға' },
  ru: { title:'Умный лабиринт', back:'← К играм', intro:'Найди выход. Если понадобится, помощник BFS покажет правильный путь.', difficulty:'Сложность', levels:['Легко','Средне','Сложно'], solve:'AI: показать путь', reset:'Новый лабиринт', sound:'Звук', on:'включён', off:'выключен', help:'Стрелки или WASD, экранные кнопки или свайп. Enter — помощь, Space — новая игра.', note:'Браузерная адаптация labirint.py. Синий путь — решение BFS; его показ не считается победой.', player:'● Ты', goal:'■ Цель', playing:'Доберись до цели!', won:'ПОБЕДА! Ты у цели.', solved:'Путь BFS показан', steps:'шагов', up:'Вверх', down:'Вниз', left:'Влево', right:'Вправо' },
  en: { title:'Smart Maze', back:'← Back to games', intro:'Find the exit. Need a hand? The BFS helper can reveal the right path.', difficulty:'Difficulty', levels:['Easy','Medium','Hard'], solve:'AI: reveal path', reset:'New maze', sound:'Sound', on:'on', off:'off', help:'Arrow keys or WASD, on-screen buttons, or swipe. Enter for a hint; Space for a new maze.', note:'Browser adaptation of labirint.py. The blue route is a BFS solution; revealing it does not count as a win.', player:'● You', goal:'■ Goal', playing:'Reach the goal!', won:'YOU WIN! Goal reached.', solved:'BFS route revealed', steps:'steps', up:'Up', down:'Down', left:'Left', right:'Right' }
};
const $ = id => document.getElementById(id);
const canvas = $('maze'), ctx = canvas.getContext('2d');
let language = 'kk';
try { const saved = localStorage.getItem('python-games-language'); if (translations[saved]) language = saved; } catch {}
let grid, position, route = [], won = false, size = 31, muted = true, audio, moves = 0;
let hold = null, origin = null;
const directions = { up:[-1,0], down:[1,0], left:[0,-1], right:[0,1] };
function tone(frequency) {
  if (muted) return;
  try {
    audio ??= new AudioContext(); audio.resume();
    const oscillator = audio.createOscillator(), gain = audio.createGain();
    oscillator.frequency.value = frequency;
    gain.gain.setValueAtTime(.035, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(.001, audio.currentTime + .1);
    oscillator.connect(gain).connect(audio.destination); oscillator.start(); oscillator.stop(audio.currentTime + .1);
  } catch {}
}
function labels() {
  const t = translations[language];
  document.documentElement.lang = language; document.title = `${t.title} · Python Games`;
  $('language').value = language;
  for (const key of ['title','back','intro','solve','reset','help','note']) $(key).textContent = t[key];
  $('difficulty-label').textContent = t.difficulty;
  [...$('difficulty').options].forEach((option,i) => option.textContent = `${t.levels[i]} · ${option.value} × ${option.value}`);
  $('player-label').textContent = t.player; $('goal-label').textContent = t.goal;
  $('sound').textContent = `${t.sound}: ${t[muted ? 'off' : 'on']}`;
  document.querySelector('.dpad').setAttribute('aria-label', t.help);
  document.querySelectorAll('[data-move]').forEach(button => button.setAttribute('aria-label', t[button.dataset.move]));
  $('status').textContent = `${t[won ? 'won' : route.length ? 'solved' : 'playing']} · ${moves} ${t.steps}`;
  canvas.setAttribute('aria-label', `${t.title}, ${size} × ${size}. ${t.help}`);
}
function draw() {
  const cell = 620 / size, highlighted = new Set(route.map(p => p.join(',')));
  ctx.fillStyle = '#0f172a'; ctx.fillRect(0,0,620,620);
  for (let r=0;r<size;r++) for (let c=0;c<size;c++) {
    let color = grid[r][c] ? '#0f172a' : '#dce6ee';
    if (highlighted.has(`${r},${c}`)) color = '#3b82f6';
    if (r===1 && c===1) color = '#c4f66c';
    if (r===size-2 && c===size-2) color = '#facc15';
    ctx.fillStyle = color; ctx.fillRect(c*cell,r*cell,Math.ceil(cell),Math.ceil(cell));
  }
  ctx.fillStyle = '#22d3ee';
  ctx.fillRect(position[1]*cell+cell*.18, position[0]*cell+cell*.18, cell*.64, cell*.64);
}
function stopHold() { clearInterval(hold); hold = null; }
function reset() {
  stopHold(); origin = null; size = Number($('difficulty').value);
  grid = generateMaze(size); position = [1,1]; route = []; won = false; moves = 0;
  tone(380); labels(); draw();
}
function move(direction) {
  if (won) return;
  const [dr,dc] = directions[direction], nr = position[0]+dr, nc = position[1]+dc;
  if (grid[nr]?.[nc] !== 0) return;
  position = [nr,nc]; moves++;
  won = nr===size-2 && nc===size-2;
  tone(won ? 880 : 440); labels(); draw();
}
$('difficulty').onchange = reset; $('reset').onclick = reset;
$('solve').onclick = () => { if (won || route.length) return; route = solveMaze(grid); tone(660); labels(); draw(); };
$('sound').onclick = () => { muted = !muted; labels(); tone(600); };
$('language').onchange = e => { language = e.target.value; try { localStorage.setItem('python-games-language',language); } catch {} labels(); };
document.addEventListener('keydown', e => {
  if (e.target.matches('select,button')) return;
  const direction = {ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right',w:'up',s:'down',a:'left',d:'right'}[e.key.length===1 ? e.key.toLowerCase() : e.key];
  if (direction) { e.preventDefault(); move(direction); }
  if (e.key==='Enter') { e.preventDefault(); $('solve').click(); }
  if (e.key===' ') { e.preventDefault(); reset(); }
});
document.querySelectorAll('[data-move]').forEach(button => {
  button.addEventListener('pointerdown', e => {
    e.preventDefault(); stopHold(); button.setPointerCapture(e.pointerId);
    move(button.dataset.move); hold = setInterval(() => move(button.dataset.move),120);
  });
  // Keyboard-generated clicks have detail=0; pointer input is handled above.
  button.addEventListener('click', e => { if (e.detail===0) move(button.dataset.move); });
});
canvas.addEventListener('pointerdown', e => { canvas.setPointerCapture(e.pointerId); canvas.focus(); origin = [e.clientX,e.clientY]; });
canvas.addEventListener('pointermove', e => {
  if (!origin) return;
  const dx=e.clientX-origin[0], dy=e.clientY-origin[1];
  if (Math.max(Math.abs(dx),Math.abs(dy))<20) return;
  move(Math.abs(dx)>Math.abs(dy) ? dx>0?'right':'left' : dy>0?'down':'up'); origin=[e.clientX,e.clientY];
});
function release() { stopHold(); origin = null; }
for (const event of ['pointerup','pointercancel','lostpointercapture']) document.addEventListener(event, release);
window.addEventListener('blur', release);
document.addEventListener('visibilitychange', () => { if (document.hidden) release(); });
reset();
