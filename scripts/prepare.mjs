import { mkdir, readFile, writeFile } from 'node:fs/promises';
await mkdir('public/data', { recursive: true });
for (const name of [
  'object',
  'observations',
  'ephemeris',
  'frames',
  'animations',
  'status',
]) {
  const raw = JSON.parse(await readFile(`data/${name}.json`, 'utf8'));
  await writeFile(`public/data/${name}.json`, JSON.stringify(raw));
}
