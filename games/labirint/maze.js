// DFS builds the corridors; three extra connections create alternative routes.
export function generateMaze(size, random = Math.random, attempt = 0) {
  const grid = Array.from({ length: size }, () => Array(size).fill(1));
  const stack = [[1, 1]];
  grid[1][1] = 0;
  while (stack.length) {
    const [r, c] = stack[stack.length - 1];
    const choices = [[-2, 0], [2, 0], [0, -2], [0, 2]]
      .map(([dr, dc]) => [r + dr, c + dc])
      .filter(([nr, nc]) => nr > 0 && nr < size - 1 && nc > 0 && nc < size - 1 && grid[nr][nc] === 1);
    if (!choices.length) { stack.pop(); continue; }
    const [nr, nc] = choices[Math.floor(random() * choices.length)];
    grid[(r + nr) / 2][(c + nc) / 2] = 0;
    grid[nr][nc] = 0;
    stack.push([nr, nc]);
  }
  // Open three walls connecting different points on the original entrance-to-exit
  // route. Each connection creates a genuine alternative, not another dead end.
  const route = new Set(solveMaze(grid).map(cell => cell.join(',')));
  const shortcuts = [];
  for (let r = 1; r < size - 1; r++) for (let c = 1; c < size - 1; c++) {
    if (!grid[r][c]) continue;
    if ((r % 2 === 1 && c % 2 === 0 && route.has(`${r},${c-1}`) && route.has(`${r},${c+1}`)) ||
        (r % 2 === 0 && c % 2 === 1 && route.has(`${r-1},${c}`) && route.has(`${r+1},${c}`))) {
      shortcuts.push([r,c]);
    }
  }
  // Reject trees with too few useful shortcuts. The fixed DFS fallback also
  // has three connections for all supported sizes, bounding generation time.
  if (shortcuts.length < 3) {
    if (attempt < 16) return generateMaze(size, random, attempt + 1);
    return generateMaze(size, () => 0, 17);
  }
  for (let i = shortcuts.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [shortcuts[i], shortcuts[j]] = [shortcuts[j], shortcuts[i]];
  }
  for (const [r,c] of shortcuts.slice(0,3)) grid[r][c] = 0;
  const shortest = solveMaze(grid);
  let turns = 0;
  for (let i = 2; i < shortest.length; i++) {
    if (shortest[i][0]-shortest[i-1][0] !== shortest[i-1][0]-shortest[i-2][0] ||
        shortest[i][1]-shortest[i-1][1] !== shortest[i-1][1]-shortest[i-2][1]) turns++;
  }
  if (turns < 3) {
    if (attempt < 16) return generateMaze(size, random, attempt + 1);
    return generateMaze(size, () => 0, 17);
  }
  return grid;
}

export function solveMaze(grid, start = [1, 1]) {
  const end = grid.length - 2;
  const queue = [start], parents = new Map([[start.join(','), null]]);
  for (let i = 0; i < queue.length; i++) {
    const [r, c] = queue[i];
    if (r === end && c === end) {
      const path = [];
      let current = [r, c];
      while (current) { path.push(current); current = parents.get(current.join(',')); }
      return path.reverse();
    }
    for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
      const next = [r + dr, c + dc], key = next.join(',');
      if (grid[next[0]]?.[next[1]] === 0 && !parents.has(key)) {
        parents.set(key, [r, c]); queue.push(next);
      }
    }
  }
  return [];
}
