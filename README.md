# 🦤 BePelican — Meta Ads Dashboard Web App

Dashboard seguro y compartible para tu equipo. Autenticación con contraseña. Actualización automática diaria.

## 📋 Archivos incluidos

- `index-secure.html` — Dashboard seguro con login (lo que tu equipo ve)
- `update_data.py` — Script que jala datos de Meta Ads (server-side, seguro)
- `data.json` — Datos actualizados (se genera automáticamente)
- `.github/workflows/update.yml` — Automatización diaria en GitHub
- `generate_password_hash.py` — Genera hash seguro de contraseña
- `encrypt_token.py` — Configuración de token (informativo)
- `README.md` — Este archivo

## 🔐 Seguridad (IMPORTANTE)

Este dashboard implementa **múltiples capas de seguridad:**

1. **Password Hashing**: Tu contraseña se valida con SHA-256 (no se almacena en texto plano)
2. **Session-based Auth**: Sesión válida solo durante la navegación (se limpia al cerrar navegador)
3. **Server-side Token**: Tu Meta API token **nunca sale del servidor**
4. **GitHub Actions Secrets**: El token se almacena de forma segura en GitHub (no en el código)
5. **Static Frontend**: El dashboard solo lee un archivo JSON estático (no accede API directamente)

## 🚀 Instalación en GitHub Pages

### Paso 1: Genera tu Password Hash

Ejecuta este script para crear un hash seguro de tu contraseña:

```bash
python3 generate_password_hash.py
```

Te pedirá una contraseña. Copia el hash resultante (se verá así):
```
PASSWORD_HASH = "a1b2c3d4e5f6..."
```

### Paso 2: Actualiza index-secure.html

1. Abre `index-secure.html` en un editor de texto
2. Busca la línea: `const PASSWORD_HASH = "8f4e3c8d..."`
3. Reemplaza el valor con tu hash generado en el Paso 1

### Paso 3: Actualiza update_data.py

1. Abre `update_data.py`
2. En la línea 12, reemplaza: `TOKEN = "EAF..."`
3. Con tu Meta API token real (comienza con `EA`)

### Paso 4: Crea repositorio en GitHub

```bash
mkdir bepelican-ads-dashboard
cd bepelican-ads-dashboard
git init
```

### Paso 5: Sube a GitHub

1. En https://github.com/new crea un repositorio público: `bepelican-ads-dashboard`
2. En tu carpeta local:

```bash
git add .
git commit -m "Initial setup"
git remote add origin https://github.com/TU-USUARIO/bepelican-ads-dashboard.git
git branch -M main
git push -u origin main
```

### Paso 6: Configura GitHub Actions

1. En GitHub → Repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `META_TOKEN`
4. Value: Tu Meta API token
5. Click **Add secret**

### Paso 7: Crea workflow automatizado

1. En tu repo, crea carpeta: `.github/workflows/`
2. Crea archivo: `.github/workflows/update.yml`
3. Copia el contenido de `.github-workflows-update.yml`
4. Modifica la línea 22 para usar el secret:
   ```yaml
   env:
     META_TOKEN: ${{ secrets.META_TOKEN }}
   ```
5. En `update_data.py`, cambia la línea 12 a:
   ```python
   TOKEN = os.getenv("META_TOKEN", "")
   ```

### Paso 8: Habilita GitHub Pages

1. **Settings** → **Pages**
2. Branch: `main` → Folder: `/ (root)`
3. Click **Save**

🎉 Tu dashboard estará en: `https://TU-USUARIO.github.io/bepelican-ads-dashboard`

## 🔄 Actualización manual de datos

Sin esperar al día siguiente:

```bash
python3 update_data.py
git add data.json
git commit -m "Manual data update"
git push
```

O en GitHub: **Actions** → **Update Meta Ads Data** → **Run workflow**

## 📊 ¿Qué ve tu equipo?

- ✅ Dashboard con métricas (gasto, alcance, CTR, mensajes)
- ✅ Campañas activas y pausadas con detalles
- ✅ Login con contraseña
- ✅ Datos actualizados automáticamente cada día
- ✅ Accesible desde cualquier dispositivo

## ⚙️ Personalización

### Cambiar contraseña

1. Ejecuta: `python3 generate_password_hash.py`
2. Ingresa tu nueva contraseña
3. Copia el nuevo hash
4. Actualiza `index-secure.html` línea ~207:
   ```javascript
   const PASSWORD_HASH = "tu-nuevo-hash";
   ```
5. Push a GitHub

### Cambiar hora de actualización

En `.github/workflows/update.yml`, línea 5:
```yaml
cron: '0 9 * * *'  # 9 AM UTC
# Cambia a:
cron: '0 14 * * *'  # 2 PM UTC (por ejemplo)
```

### Agregar nuevos usuarios

Comparte la URL: `https://TU-USUARIO.github.io/bepelican-ads-dashboard`
Contraseña: La que configuraste

Todos usan la MISMA contraseña. Para autenticación individual, necesitarías un backend.

## ⚠️ Notas de seguridad importantes

- **Meta API Token**: Se almacena en GitHub Secrets, nunca se expone publicamente
- **Contraseña**: Se hashea con SHA-256. Nadie puede recuperar la contraseña original
- **Datos**: Solo se actualizan en GitHub Actions (servidor seguro de GitHub)
- **Sesión**: Se limpia automáticamente cuando cierras el navegador
- **URL**: Cualquiera que conozca la URL + contraseña puede acceder (protección básica)

Para máxima seguridad en equipos grandes, considera:
- GitHub Teams (control de acceso a repo)
- Contraseñas diferentes por usuario (requiere backend)
- IP whitelisting (GitHub Enterprise)

## 📱 Acceso desde cualquier dispositivo

- ✅ Chrome, Safari, Firefox, Edge
- ✅ Mac, Windows, Linux
- ✅ iPhone, Android, tablets

Solo necesitan: **URL + contraseña**

## 🐛 Troubleshooting

**"Contraseña incorrecta"**
- Verifica que el PASSWORD_HASH en index-secure.html sea el correcto
- Ejecuta `generate_password_hash.py` nuevamente

**"Error al cargar datos"**
- Espera 5-10 minutos a que GitHub Actions ejecute el workflow
- Verifica que `update_data.py` esté en la raíz del repo
- En GitHub Actions → Workflows, verifica que no haya errores

**Datos no se actualizan**
- Verifica el workflow en GitHub → Actions → Update Meta Ads Data
- Revisa los logs para errores
- Asegúrate que META_TOKEN esté en Secrets

---

**Soporte**: Lee docs de GitHub Pages: https://pages.github.com
