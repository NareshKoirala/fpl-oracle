export function getPosString(pos: number): string {
  return pos === 4 ? "FWD" : pos === 3 ? "MID" : pos === 2 ? "DEF" : "GKP";
}
