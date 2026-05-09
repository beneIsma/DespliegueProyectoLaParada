/** En Vercel el build ejecuta scripts/inject-api-url.mjs (variable NG_API_URL). En local, edita apiUrl antes de `ng build`. */
export const environment = {
  production: true,
  apiUrl: 'https://REEMPLAZA-TU-BACKEND.onrender.com/api',
};
