// Registry contract: stable ID, translation key, category, runtime and lazy loader.
export const games = [
{id:'snake',category:'arcade',runtime:'javascript',art:'snake-art',load:()=>import('./games.js').then(m=>m.snake)},
{id:'memory',category:'puzzle',runtime:'javascript',art:'memory-art',load:()=>import('./games.js').then(m=>m.memory)},
{id:'tic',category:'puzzle',runtime:'javascript',art:'tic-art',load:()=>import('./games.js').then(m=>m.tic)}
];
export function artwork(id) {
if(id==='snake')return '<div class="mini-snake">'+ '<i></i>'.repeat(7)+'</div>';
if(id==='memory')return '<div class="mini-memory">'+['✦','?','●','?','✦','?'].map(x=>`<i>${x}</i>`).join('')+'</div>';
return '<div class="mini-tic">'+['×','○','','','×','○','○','','×'].map(x=>`<i>${x}</i>`).join('')+'</div>';
}
