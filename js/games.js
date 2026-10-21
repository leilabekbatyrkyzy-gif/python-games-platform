// Every game owns its event listeners/timers and returns a cleanup function.
export function snake({stage,status,t,directionPad}) {
const canvas=document.createElement('canvas');canvas.width=400;canvas.height=400;canvas.setAttribute('aria-label',t('snake'));canvas.setAttribute('role','img');stage.append(canvas);
const ctx=canvas.getContext('2d');let body=[{x:8,y:10},{x:7,y:10},{x:6,y:10}],dir={x:1,y:0},next=dir,food,score=0,timer=null,done=false,queued=false;
function placeFood(){const free=[];for(let y=0;y<20;y++)for(let x=0;x<20;x++)if(!body.some(p=>p.x===x&&p.y===y))free.push({x,y});food=free[Math.floor(Math.random()*free.length)];}
function draw(){ctx.fillStyle='#14231c';ctx.fillRect(0,0,400,400);ctx.strokeStyle='#ffffff06';for(let i=0;i<=400;i+=20){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,400);ctx.moveTo(0,i);ctx.lineTo(400,i);ctx.stroke();}body.forEach((p,i)=>{ctx.fillStyle=i?'#9dce59':'#c4f66c';ctx.fillRect(p.x*20+2,p.y*20+2,16,16);});if(food){ctx.fillStyle='#ba9bea';ctx.fillRect(food.x*20+3,food.y*20+3,14,14);}}
function finish(won=false){done=true;clearInterval(timer);status.textContent=`${t(won?'win':'over')} · ${t('score')}: ${score}`;}
function step(){dir=next;queued=false;const head={x:body[0].x+dir.x,y:body[0].y+dir.y};const eat=head.x===food.x&&head.y===food.y;const collision=(eat?body:body.slice(0,-1)).some(p=>p.x===head.x&&p.y===head.y);if(head.x<0||head.x>=20||head.y<0||head.y>=20||collision){finish();return;}body.unshift(head);if(eat){score++;if(body.length===400){draw();finish(true);return;}placeFood();}else body.pop();status.textContent=`${t('score')}: ${score}`;draw();}
const directions={up:{x:0,y:-1},down:{x:0,y:1},left:{x:-1,y:0},right:{x:1,y:0}};
function move(name){if(done||queued)return;const d=directions[name];if(!d||d.x===-dir.x&&d.y===-dir.y)return;next=d;queued=true;if(!timer)timer=setInterval(step,140);}
function key(e){const name={ArrowUp:'up',w:'up',ArrowDown:'down',s:'down',ArrowLeft:'left',a:'left',ArrowRight:'right',d:'right'}[e.key];if(name){e.preventDefault();move(name);}}
function click(e){const b=e.target.closest('[data-direction]');if(b)move(b.dataset.direction);}
function visibility(){if(document.hidden&&timer){clearInterval(timer);timer=null;queued=false;}}
placeFood();draw();status.textContent=t('ready');directionPad.hidden=false;document.addEventListener('keydown',key);document.addEventListener('visibilitychange',visibility);directionPad.addEventListener('click',click);
return()=>{clearInterval(timer);document.removeEventListener('keydown',key);document.removeEventListener('visibilitychange',visibility);directionPad.removeEventListener('click',click);directionPad.hidden=true;};
}
export function memory({stage,status,t}) {
const symbols=['✦','●','◆','♥','☀','♣','☂','♫'];const cards=[...symbols,...symbols];for(let i=cards.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[cards[i],cards[j]]=[cards[j],cards[i]];}
const board=document.createElement('div');board.className='memory-board';stage.append(board);let opened=[],pairs=0,moves=0,locked=false,timeout;const buttons=[];
function update(){status.textContent=`${pairs===8?t('win')+' · ':''}${t('pairs')}: ${pairs}/8 · ${t('moves')}: ${moves}`;}
cards.forEach((symbol,i)=>{const b=document.createElement('button');b.className='memory-card';b.textContent='?';b.setAttribute('aria-label',`${t('memory')} ${i+1}`);b.addEventListener('click',()=>{if(locked||b.disabled||opened.includes(i))return;b.textContent=symbol;b.setAttribute('aria-label',symbol);opened.push(i);if(opened.length===2){moves++;const [a,c]=opened;if(cards[a]===cards[c]){for(const index of opened){buttons[index].disabled=true;buttons[index].classList.add('matched');}pairs++;opened=[];update();}else{locked=true;update();timeout=setTimeout(()=>{for(const index of opened){buttons[index].textContent='?';buttons[index].setAttribute('aria-label',`${t('memory')} ${index+1}`);}opened=[];locked=false;},750);}}});buttons.push(b);board.append(b);});update();return()=>clearTimeout(timeout);
}
export function tic({stage,status,t}) {
const board=document.createElement('div');board.className='tic-board';stage.append(board);const cells=Array(9).fill('');let player='X',ended=false;const buttons=[];const lines=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
status.textContent=`${t('turn')}: X`;
cells.forEach((_,i)=>{const b=document.createElement('button');b.className='tic-cell';b.setAttribute('aria-label',`${t('tic')} ${i+1}`);b.addEventListener('click',()=>{if(ended||cells[i])return;cells[i]=player;b.textContent=player;b.setAttribute('aria-label',`${i+1}: ${player}`);b.disabled=true;if(lines.some(line=>line.every(n=>cells[n]===player))){status.textContent=`${t('win')} ${player}`;ended=true;}else if(cells.every(Boolean)){status.textContent=t('draw');ended=true;}else{player=player==='X'?'O':'X';status.textContent=`${t('turn')}: ${player}`;}if(ended)buttons.forEach(button=>button.disabled=true);});buttons.push(b);board.append(b);});return()=>{};
}
