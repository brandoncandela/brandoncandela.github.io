import { execFileSync } from 'node:child_process';
import { cpSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
execFileSync('npm', ['run','build'], {cwd: root+'theme', stdio:'inherit', env:{...process.env,ASTRO_TELEMETRY_DISABLED:'1'}});
cpSync(root+'theme/dist/index.html',root+'index.html');
cpSync(root+'theme/dist/_astro',root+'_astro',{recursive:true});
console.log('Static GitHub Pages output updated. Existing notes and assets preserved.');
