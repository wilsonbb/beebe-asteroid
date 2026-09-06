import { readdir, mkdir, copyFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
// Vinext exports flat .html files. Directory indexes also work on plain static hosts.
async function walk(dir) {
  const files = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) files.push(...(await walk(p)));
    else files.push(p);
  }
  return files;
}
for (const file of await walk('dist/client')) {
  if (
    !file.endsWith('.html') ||
    ['index.html', '404.html'].includes(path.basename(file))
  )
    continue;
  const target = file.slice(0, -5);
  await mkdir(target, { recursive: true });
  await copyFile(file, path.join(target, 'index.html'));
}
await writeFile('dist/client/.nojekyll', '');
// A project Pages artifact is mounted at /repository by GitHub. Vinext already
// nests a basePath export there; flatten that directory in the upload artifact.
const base = (process.env.BASE_PATH || '').replace(/^\/+|\/+$/g, '');
if (base) {
  const { rename, rm, access } = await import('node:fs/promises');
  if (
    base
      .split('/')
      .some(
        (part) =>
          !/^[A-Za-z0-9_.-]+$/.test(part) || part === '.' || part === '..',
      )
  )
    throw new Error('Invalid BASE_PATH');
  const nested = path.join('dist/client', base);
  await access(path.join(nested, 'index.html'));
  for (const name of ['404.html', 'vinext-client-entry-manifest.json']) {
    try {
      await copyFile(path.join('dist/client', name), path.join(nested, name));
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
  }
  await rename(nested, 'dist/normalized-export');
  await rm('dist/client', { recursive: true });
  await rename('dist/normalized-export', 'dist/client');
  await writeFile('dist/client/.nojekyll', '');
}
