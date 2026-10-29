// Iterative randomized DFS generation and breadth-first search, as in labirint.py.
export function generateMaze(size, random = Math.random) {
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
