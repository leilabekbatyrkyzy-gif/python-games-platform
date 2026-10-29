export const choices = ['rock', 'paper', 'scissors'];
export const counters = { rock:'paper', paper:'scissors', scissors:'rock' };
export function winner(player, opponent) {
  if (!choices.includes(player) || !choices.includes(opponent)) throw new Error('Invalid move');
  return player === opponent ? 'draw' : counters[opponent] === player ? 'win' : 'lose';
}
// Mirrors RPS_AI: predict from the previous two moves, then counter the prediction.
export class LearningAI {
  constructor(random = Math.random) { this.random = random; this.history = []; this.patterns = new Map(); }
  predict() {
    const stats = this.patterns.get(this.history.slice(-2).join(','));
    if (this.history.length < 2 || !stats) return choices[Math.floor(this.random() * 3)];
    let predicted = choices[0];
    for (const move of choices) if (stats[move] > stats[predicted]) predicted = move;
    return counters[predicted];
  }
  learn(move) {
    if (!choices.includes(move)) throw new Error('Invalid move');
    if (this.history.length >= 2) {
      const key = this.history.slice(-2).join(',');
      if (!this.patterns.has(key)) this.patterns.set(key, {rock:0,paper:0,scissors:0});
      this.patterns.get(key)[move]++;
    }
    this.history.push(move);
  }
}
