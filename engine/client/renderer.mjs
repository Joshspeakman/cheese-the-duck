// Fixed-cell glyph engine: rasterize each glyph once, then composite cached tiles.
export const CELL_W = 10, CELL_H = 18;
export function decodeLine(runs, cols) {
  const cells = [];
  for (const [text, foreground, background, flags] of runs) {
    let fg = foreground, bg = background;
    if (flags & 4) [fg, bg] = [bg, fg];
    for (const char of text) {
      if (cells.length === cols) return cells;
      cells.push([char, fg, bg, flags]);
    }
  }
  return cells;
}
export class GlyphRenderer {
  constructor(canvas) {
    this.canvas = canvas; this.ctx = canvas.getContext('2d', { alpha: false });
    this.atlas = new Map(); this.previous = []; this.scale = 1; this.frames = 0;
  }
  resize(cols, rows, scale) {
    const dpr = window.devicePixelRatio || 1;
    this.scale = Math.max(.25, scale);
    const w = Math.round(cols * CELL_W * this.scale * dpr), h = Math.round(rows * CELL_H * this.scale * dpr);
    this.canvas.style.width = `${cols * CELL_W * this.scale}px`; this.canvas.style.height = `${rows * CELL_H * this.scale}px`;
    if (w === this.canvas.width && h === this.canvas.height) return;
    this.canvas.width = w; this.canvas.height = h; this.sx = w / cols; this.sy = h / rows;
    this.previous = []; this.atlas.clear(); this.ctx.fillStyle = '#101b19'; this.ctx.fillRect(0, 0, w, h);
  }
  tile(char, fg, flags) {
    const key = `${char}:${fg}:${flags}`;
    if (this.atlas.has(key)) return this.atlas.get(key);
    if (this.atlas.size > 8192) this.atlas.clear();
    const tile = document.createElement('canvas'); tile.width = Math.ceil(this.sx); tile.height = Math.ceil(this.sy);
    const ctx = tile.getContext('2d'); ctx.fillStyle = fg; ctx.globalAlpha = flags & 2 ? .65 : 1;
    ctx.font = `${flags & 1 ? 'bold ' : ''}${this.sy * .80}px Menlo, monospace`;
    ctx.textBaseline = 'middle'; ctx.textAlign = 'center';
    ctx.fillText(char, tile.width / 2, tile.height * .52, tile.width); this.atlas.set(key, tile); return tile;
  }
  draw(frame) {
    const { cols, rows, lines } = frame, next = [];
    for (let y = 0; y < rows; y++) {
      const cells = decodeLine(lines[y] || [], cols);
      for (let x = 0; x < cols; x++) {
        const [char, fg, bg, flags] = cells[x] || [' ', '#e2dfca', '#101b19', 0];
        const i = y * cols + x, key = `${char}:${fg}:${bg}:${flags}`; next[i] = key;
        if (key === this.previous[i]) continue;
        const left = Math.round(x * this.sx), top = Math.round(y * this.sy);
        const w = Math.round((x + 1) * this.sx) - left, h = Math.round((y + 1) * this.sy) - top;
        this.ctx.fillStyle = bg; this.ctx.fillRect(left, top, w, h);
        if (char !== ' ') this.ctx.drawImage(this.tile(char, fg, flags), left, top, w, h);
      }
    }
    this.previous = next; this.frames++;
  }
}
