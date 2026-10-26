// Registry contract: stable ID, translation key, category, runtime and lazy loader or href.
export const games = [
{id:'snake',category:'arcade',runtime:'javascript',art:'snake-art',load:()=>import('./games.js').then(m=>m.snake)},
{id:'memory',category:'puzzle',runtime:'javascript',art:'memory-art',load:()=>import('./games.js').then(m=>m.memory)},
{id:'tic',category:'puzzle',runtime:'javascript',art:'tic-art',load:()=>import('./games.js').then(m=>m.tic)},
{id:'kylyshKalkan',category:'arcade',runtime:'web',art:'sword-art',href:'games/kylysh-kalkan/index.html'},
{id:'shakhmatAI',category:'puzzle',runtime:'web',art:'chess-art',href:'games/shakhmat-ai/index.html'},
{id:'pong',category:'arcade',runtime:'web',art:'pong-art',href:'games/pong/index.html'}
];
export function artwork(id) {
if(id==='pong')return '<svg class="pong-icon" viewBox="0 0 180 140" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M90 10v120" stroke="#ffffff30" stroke-width="3" stroke-dasharray="6 8"/><rect x="20" y="48" width="12" height="62" rx="4" fill="#c4f66c"/><rect x="148" y="20" width="12" height="62" rx="4" fill="#b69ae9"/><circle cx="111" cy="80" r="9" fill="#fff"/></svg>';

if(id==='shakhmatAI')return '<svg class="chess-piece" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M80 16v30M67 29h26" stroke="#d9c5ff" stroke-width="9" stroke-linecap="round"/><path d="M51 52h58l-9 24H60Z" fill="#b69ae9"/><path d="M65 79h30l8 37H57Z" fill="#d9c5ff"/><path d="M51 117h58l8 17H43Z" fill="#b69ae9"/><rect x="38" y="135" width="84" height="12" rx="5" fill="#d9c5ff"/></svg>';

if(id==='kylyshKalkan')return '<svg class="sword-shield" viewBox="0 0 180 140" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 27 145 43v38c0 21-22 36-45 46-23-10-45-25-45-46V43Z" fill="#53624b" stroke="#c4f66c" stroke-width="4"/><path d="M100 39v73" stroke="#c4f66c" stroke-width="3"/><path d="m38 101 65-75 15-5-2 16-65 75Z" fill="#ece4cf" stroke="#d4c5a2" stroke-width="3"/><path d="m34 91 27 24M43 105l-16 18" stroke="#d7b76e" stroke-width="9" stroke-linecap="round"/></svg>';

if(id==='snake')return '<div class="mini-snake">'+ '<i></i>'.repeat(7)+'</div>';
if(id==='memory')return '<div class="mini-memory">'+['✦','?','●','?','✦','?'].map(x=>`<i>${x}</i>`).join('')+'</div>';
return '<div class="mini-tic">'+['×','○','','','×','○','○','','×'].map(x=>`<i>${x}</i>`).join('')+'</div>';
}
