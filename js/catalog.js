// Registry contract: stable ID, translation key, category, runtime and lazy loader or href.
export const games = [
{id:'snake',category:'arcade',runtime:'javascript',art:'snake-art',load:()=>import('./games.js').then(m=>m.snake)},
{id:'memory',category:'puzzle',runtime:'javascript',art:'memory-art',load:()=>import('./games.js').then(m=>m.memory)},
{id:'tic',category:'puzzle',runtime:'javascript',art:'tic-art',load:()=>import('./games.js').then(m=>m.tic)},
{id:'kylyshKalkan',category:'arcade',runtime:'web',art:'sword-art',href:'games/kylysh-kalkan/index.html'}
];
export function artwork(id) {
if(id==='kylyshKalkan')return '<svg class="sword-shield" viewBox="0 0 180 140" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 27 145 43v38c0 21-22 36-45 46-23-10-45-25-45-46V43Z" fill="#53624b" stroke="#c4f66c" stroke-width="4"/><path d="M100 39v73" stroke="#c4f66c" stroke-width="3"/><path d="m38 101 65-75 15-5-2 16-65 75Z" fill="#ece4cf" stroke="#d4c5a2" stroke-width="3"/><path d="m34 91 27 24M43 105l-16 18" stroke="#d7b76e" stroke-width="9" stroke-linecap="round"/></svg>';

if(id==='snake')return '<div class="mini-snake">'+ '<i></i>'.repeat(7)+'</div>';
if(id==='memory')return '<div class="mini-memory">'+['✦','?','●','?','✦','?'].map(x=>`<i>${x}</i>`).join('')+'</div>';
return '<div class="mini-tic">'+['×','○','','','×','○','○','','×'].map(x=>`<i>${x}</i>`).join('')+'</div>';
}
