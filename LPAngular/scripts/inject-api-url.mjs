/**
 * Vercel/CI: define NG_API_URL (ej. https://lparada-api.onrender.com/api) antes del build.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const raw = process.env.NG_API_URL || process.env.API_URL || 'https://REEMPLAZA-TU-BACKEND.onrender.com/api';
const apiUrl = raw.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
const out = `/** Generado por scripts/inject-api-url.mjs — no edites a mano en CI; usa NG_API_URL. */
export const environment = {
  production: true,
  apiUrl: '${apiUrl}',
};
`;
const target = path.join(__dirname, '..', 'src', 'environments', 'environment.ts');
fs.writeFileSync(target, out, 'utf8');
console.log('inject-api-url:', target, '→', raw);
