export function hand(move) {
  const paths = {
    rock:'M43 133v-20L26 93q-9-12 0-19 9-7 18 4l9 10V61q0-12 11-12 10 0 11 11v-6q0-12 11-12 11 0 11 12v4q2-11 12-11 11 0 11 12v7q3-7 11-5 10 2 10 13v24q0 18-20 29v6Z M75 62v24m22-26v24m22-16v18M49 87q16-9 28 8l9 13',
    paper:'M45 133v-21L26 83q-7-12 3-18 9-6 17 5l9 11V29q0-12 10-12t10 12v39-48q0-12 10-12t10 12v48-39q0-12 10-12t10 12v42-26q0-11 10-11t10 11v44q0 22-17 35v10Z M75 69v17m20-17v17m20-15v15',
    scissors:'M46 133v-23L31 84q-6-13 5-17 10-4 17 7l7 9-15-55q-3-12 8-15 11-3 14 9l16 49 15-53q4-12 14-8 10 3 7 16l-13 49q14-12 23 0 13-1 14 15v11q0 20-20 32H46Z M83 72l-7 22m31-16-8 22m25-20-7 19'
  };
  return `<svg viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="${paths[move] || paths.rock}" fill="currentColor" stroke="#262938" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}
