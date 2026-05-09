# Guía completa de despliegue — La Parada (Django + Angular)

Repo: https://github.com/benelsma/DespliegueProyectoLaParada
Resultado final:
- Frontend Angular: `https://<tu-proyecto>.vercel.app`
- Backend Django API: `https://lparada-api.onrender.com`
- Base de datos: PostgreSQL en Supabase

> Tu proyecto YA tiene casi toda la configuración hecha (`render.yaml`, `vercel.json`, `requirements.txt`, scripts de migración, `settings.py` con `DATABASE_URL`). Solo te queda crear cuentas, conectar el repo a cada servicio, y poner las variables de entorno.

---

## Fase 0 — Pre-vuelo (2 min)

Abre PowerShell en `C:\Users\Nitropc\Desktop\CURSOR\ProyectoPersonal_TFG` y comprueba que todo está limpio:

```powershell
git status
git pull
```

Si tienes muchos archivos "modificados" sin haberlos tocado, es por los finales de línea de Windows (CRLF). Acabo de añadir un `.gitattributes` que lo arregla; al hacer commit se normalizará.

---

## Fase 1 — Base de datos en Supabase (10 min)

### 1.1 Crear el proyecto

1. Ve a https://supabase.com → **Sign in with GitHub**.
2. **New project**:
   - **Name**: `laparada`
   - **Database Password**: GENERA UNA Y GUÁRDALA (la usarás como contraseña de Postgres). Sin tildes ni caracteres raros, mejor `[A-Za-z0-9]`.
   - **Region**: `West EU (Ireland)` o `Frankfurt` (lo que más cerca te quede).
   - **Plan**: Free.
3. Espera 2 minutos a que termine el provisioning.

### 1.2 Coger la URL de conexión correcta

Importante: Supabase ofrece varias URLs. Tienes que usar la del **Session pooler** (puerto 5432) porque la "directa" suele ser solo IPv6 y falla desde Windows y desde Render.

1. En el panel de Supabase → **Project Settings** (icono engranaje) → **Database** → **Connection string**.
2. Selecciona la pestaña **Session pooler** (NO "Direct connection", NO "Transaction pooler").
3. Copia la URL. Tendrá esta forma:

```
postgresql://postgres.XXXXXXXXXXXX:[YOUR-PASSWORD]@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
```

4. Reemplaza `[YOUR-PASSWORD]` por la contraseña que generaste antes.
5. Guárdala en un sitio seguro: la usarás dos veces (en local y en Render).

### 1.3 Probar la conexión desde local y crear tablas

Edita `LPBackend/.env` para que quede así (si ya tienes valores, sustitúyelos):

```env
SECRET_KEY=pon-aqui-una-cadena-larga-y-aleatoria
DEBUG=True
ALLOWED_HOST=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:4200
DATABASE_URL=postgresql://postgres.XXXXXX:TU_PASSWORD@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
```

Aplica las migraciones contra la base remota (esto crea todas las tablas en Supabase):

```powershell
cd LPBackend
py -3.13 -m pip install -r requirements.txt
py -3.13 manage.py migrate
```

Si funciona, ya tienes la BD remota lista con las tablas vacías.

### 1.4 Migrar los datos de SQLite a Supabase (opcional)

Solo si quieres conservar los datos que tienes en `db.sqlite3`. Si vas a empezar de cero, sáltalo.

```powershell
# 1) Exportar desde SQLite (el script hace una copia de .env y le quita DATABASE_URL temporalmente)
.\scripts\export_sqlite_dump.ps1

# 2) Importar a Postgres (con DATABASE_URL apuntando a Supabase)
.\scripts\import_dump_to_postgres.ps1
```

Luego crea un superusuario en la BD remota para entrar al admin:

```powershell
py -3.13 manage.py createsuperuser
```

---

## Fase 2 — Subir cambios a GitHub (3 min)

```powershell
cd C:\Users\Nitropc\Desktop\CURSOR\ProyectoPersonal_TFG
git add .gitattributes LPAngular/vercel.json LPAngular/.vercelignore DEPLOY_PASO_A_PASO.md
git add -u
git commit -m "Configuracion final de despliegue Render + Vercel"
git push origin main
```

VERIFICAR que **NO** se ha subido `.env` ni `db.sqlite3` (están en `.gitignore`):

```powershell
git ls-files | findstr /R "\.env$ db\.sqlite3$"
```

Si ese comando no devuelve nada, perfecto.

---

## Fase 3 — Desplegar el backend en Render (10 min)

### 3.1 Crear servicio con Blueprint

1. Ve a https://render.com → **Sign in with GitHub** → autoriza el repo.
2. **New** → **Blueprint**.
3. Selecciona el repo `DespliegueProyectoLaParada`. Render detectará el `render.yaml` que ya tienes.
4. Click **Apply**. Verás que crea el servicio `lparada-api`.

### 3.2 Añadir las variables de entorno

En el panel del servicio `lparada-api` → **Environment** → añade estos secretos (los del `render.yaml` con `sync: false`):

| Clave | Valor |
|---|---|
| `DATABASE_URL` | La URI Session pooler de Supabase (la misma que en local) |
| `ALLOWED_HOST` | `lparada-api.onrender.com` (sin `https://`) |
| `CSRF_TRUSTED_ORIGINS` | `https://lparada.vercel.app` (la URL final del front; se actualiza más tarde) |

`SECRET_KEY` y `DEBUG=False` ya se generan/establecen solos por el `render.yaml`.

### 3.3 Lanzar el deploy

- Click **Manual Deploy** → **Deploy latest commit** (o espera al automático).
- Sigue los logs. Verás `pip install`, `collectstatic`, y al final `gunicorn ... Listening on 0.0.0.0:10000`.
- Cuando esté `Live`, abre `https://lparada-api.onrender.com/admin` y prueba con el superusuario que creaste antes.

> Si falla "no DATABASE_URL", revisa que la pegaste sin saltos de línea ni espacios.
> Si falla con error de TLS / SSL, asegúrate de usar la URL del Session pooler (puerto 5432).

### 3.4 Anota la URL final del API

Será `https://lparada-api.onrender.com` (o lo que diga Render). El front lo necesita.

---

## Fase 4 — Desplegar el frontend en Vercel (8 min)

### 4.1 Importar el proyecto

1. Ve a https://vercel.com → **Sign in with GitHub**.
2. **Add New** → **Project** → importa `DespliegueProyectoLaParada`.
3. Configuración:
   - **Framework Preset**: Other
   - **Root Directory**: `LPAngular` ← MUY IMPORTANTE
   - **Build Command**: ya viene de `vercel.json` (`npm run build:vercel`)
   - **Output Directory**: ya viene de `vercel.json` (`dist/TemplateAngular/browser`)
4. **Environment Variables** → añade UNA sola:
   - **Name**: `NG_API_URL`
   - **Value**: `https://lparada-api.onrender.com/api` (con `/api` al final, OJO)
   - **Environments**: Production, Preview, Development (las tres)

### 4.2 Deploy

- Click **Deploy**. Tarda 2-3 minutos.
- Cuando acabe te dará una URL tipo `https://lparada-xxxx.vercel.app`. Ábrela.

### 4.3 Cerrar el círculo de CORS/CSRF

Vuelve a Render → tu servicio → **Environment** y actualiza:

- `CSRF_TRUSTED_ORIGINS` = `https://lparada-xxxx.vercel.app` (la URL real que te dio Vercel)

Render hará un redeploy automático en ~1 min.

---

## Fase 5 — Verificación (5 min)

1. Abre `https://lparada-api.onrender.com/admin` → login con superuser → ves los datos.
2. Abre tu URL de Vercel → la web carga, navega entre páginas.
3. Abre la consola del navegador (F12) → no debe haber errores rojos de CORS ni 500.
4. Prueba registrarte / iniciar sesión / añadir al carrito → todo debería funcionar.

Si ves un error CORS:
- Confirma que `CSRF_TRUSTED_ORIGINS` en Render contiene la URL de Vercel **con `https://`**.
- Confirma que `NG_API_URL` en Vercel termina en `/api`.

Si ves 502 / 503 al cargar:
- El plan free de Render duerme tras 15 min de inactividad. La primera petición tarda ~30s en despertar. Es normal.

---

## Fase 6 — (Opcional) Dominio propio

1. Compra un dominio (Namecheap, Porkbun, IONOS).
2. En Vercel → **Settings** → **Domains** → añade `tudominio.com` y sigue las instrucciones DNS.
3. En Render (si quieres `api.tudominio.com`): **Settings** → **Custom Domains** → añade y configura el CNAME.
4. Actualiza `ALLOWED_HOST`, `CSRF_TRUSTED_ORIGINS` en Render y `NG_API_URL` en Vercel con los dominios definitivos.

---

## Resumen de variables de entorno

### En Render (servicio `lparada-api`)
```
DATABASE_URL = postgresql://postgres.XXXX:PASS@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
ALLOWED_HOST = lparada-api.onrender.com
CSRF_TRUSTED_ORIGINS = https://TU-PROYECTO.vercel.app
SECRET_KEY = (auto-generada)
DEBUG = False
PYTHON_VERSION = 3.13.0
```

### En Vercel (proyecto frontend)
```
NG_API_URL = https://lparada-api.onrender.com/api
```

### En tu .env local (no se sube)
```
SECRET_KEY = (la tuya local, distinta de producción)
DEBUG = True
ALLOWED_HOST = localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS = http://localhost:4200
DATABASE_URL = (la misma de Supabase si quieres compartir BD; o vacío para SQLite)
```

---

## Problemas frecuentes y soluciones

| Síntoma | Causa | Solución |
|---|---|---|
| `getaddrinfo failed` al conectar a Supabase | Usaste la URL "Direct" (IPv6) | Usa Session pooler |
| `403 CSRF verification failed` en Vercel | `CSRF_TRUSTED_ORIGINS` mal | Asegura `https://...` exacto |
| `CORS policy` en consola del navegador | `CORS_ALLOW_ALL_ORIGINS` cambió | Está en `True` en `settings.py`; revisa que `corsheaders` esté antes en MIDDLEWARE |
| Imágenes no se ven en producción | `MEDIA_ROOT` se borra al redeploy en Render | Usa Cloudinary o Supabase Storage para subir media. Para TFG, `SERVE_MEDIA_IN_PRODUCTION=True` puede valer temporalmente |
| Render se duerme cada 15 min | Plan free | Usa UptimeRobot.com para hacer ping cada 5 min, o paga $7/mes |
| `relation "auth_user" does not exist` | Migraciones no aplicadas en Supabase | `python manage.py migrate` con DATABASE_URL apuntando a Supabase |

---

## Archivos clave del proyecto (referencia)

| Archivo | Para qué sirve |
|---|---|
| `render.yaml` | Blueprint que Render lee al conectar el repo |
| `LPBackend/Procfile` | Comando de arranque (`gunicorn`) |
| `LPBackend/runtime.txt` | Versión de Python (3.13.0) |
| `LPBackend/requirements.txt` | Dependencias Python (gunicorn, whitenoise, dj-database-url, psycopg) |
| `LPBackend/LaParada/settings.py` | Config dinámica con env vars; ya soporta Postgres y SQLite |
| `LPAngular/vercel.json` | Config Vercel con SPA rewrites |
| `LPAngular/scripts/inject-api-url.mjs` | Inyecta `NG_API_URL` en `environment.ts` antes del build |
| `LPBackend/scripts/export_sqlite_dump.ps1` | Exporta datos SQLite → JSON |
| `LPBackend/scripts/import_dump_to_postgres.ps1` | Importa JSON → Postgres |

---

¿Listo? Sigue las fases en orden. Si te atascas en alguna, dime exactamente en qué fase y qué error ves.
