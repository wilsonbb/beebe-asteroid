import frames from '@/data/frames.json';
import { sequences } from './data';
import type { Night } from './archive';
const byNight = new Map<string, Night>();
for (const f of frames) {
  let n = byNight.get(f.night);
  if (!n) {
    const seq = sequences.find((s) => s.night === f.night);
    n = {
      night: f.night,
      count: 0,
      bands: [],
      availability: f.quality === 'rejected' ? 'rejected' : 'untried',
      poster: seq?.poster.url || null,
      n_frames: seq?.n_frames || 0,
      published_at: seq?.published_at || null,
    };
    byNight.set(f.night, n);
  }
  n.count++;
  if (!n.bands.includes(f.band)) n.bands.push(f.band);
  if (n.availability === 'rejected' && f.quality !== 'rejected') {
    n.availability = 'untried';
  }
  if (f.availability === 'pending') n.availability = 'pending';
  if (n.poster) n.availability = 'available';
}
export const nights = [...byNight.values()];
