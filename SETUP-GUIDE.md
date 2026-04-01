# 🦤 BePelican Dashboard — Setup Guide

Guía paso a paso para configurar tu dashboard seguro en 10 minutos.

## ✅ Checklist de configuración

### Paso 1: Crear password hash seguro (2 min)

```bash
python3 generate_password_hash.py
```

Ingresa tu contraseña dos veces. Copia el resultado:
```
PASSWORD_HASH = "a1b2c3d4e5f6..."
```

### Paso 2: Actualizar index-secure.html (1 min)

1. Abre `index-secure.html` con un editor (VS Code, Sublime, etc)
2. Busca línea ~207: `const PASSWORD_HASH = "8f4e3c8d..."`
3. Reemplaza con tu hash del Paso 1
4. Guarda el archivo

✅ Tu dashboard ahora tiene tu contraseña personalizada

### Paso 3: Obtener Meta API Token (2 min)

Si aún no lo tienes:
1. Ve a https://business.facebook.com/settings/apps
2. Selecciona tu aplicación
3. Roles → Sistema de usuario → Crea token
4. Copia el token (comienza con `EA`)

### Paso 4: Crear repositorio en GitHub (3 min)

1. Ve a https://github.com/new
2. Repository name: `bepelican-ads-dashboard`
3. Description: "BePelican Meta Ads Dashboard"
4. Public (importante para GitHub Pages)
5. Click "Create repository"

### Paso 5: Subir archivos a GitHub (2 min)

En tu carpeta local `bepelican-ads-dashboard`:

```bash
git init
git add .
git commit -m "Initial setup - BePelican dashboard"
git remote add origin https://github.com/TU-USUARIO/bepelican-ads-dashboard.git
git branch -M main
git push -u origin main
```

### Paso 6: Guardar token en GitHub Secrets (1 min)

1. En GitHub → Settings → Secrets and variables → Actions
2. "New repository secret"
3. Name: `META_TOKEN`
4. Value: Tu token de Meta
5. "Add secret" ✅

### Paso 7: Crear workflow (2 min)

1. En tu repo crea carpeta: `.github/workflows/`
2. Crea archivo: `.github/workflows/update.yml`
3. Copia todo el contenido de `.github-workflows-update.yml` aquí
4. Commit y push:
   ```bash
   git add .github/workflows/update.yml
   git commit -m "Add auto-update workflow"
   git push
   ```

### Paso 8: Habilitar GitHub Pages (1 min)

1. Settings → Pages
2. Build and deployment:
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)
3. Click "Save"

Espera 2-3 minutos. Tu dashboard estará en:
```
https://TU-USUARIO.github.io/bepelican-ads-dashboard
```

## ✅ Verificación

1. **¿El dashboard carga?**
   - Ve a tu URL
   - Deberías ver pantalla de login
   - Si no: espera 5 min, GitHub Pages tarda en actualizar

2. **¿El login funciona?**
   - Ingresa tu contraseña
   - Si funciona: verás el dashboard ✅

3. **¿Los datos se actualizan?**
   - En GitHub → Actions → Update Meta Ads Data
   - Debe mostrar "completed" en verde
   - Si falla: revisa el log de errores

## 🐛 Problemas comunes

### "Contraseña incorrecta"
```bash
python3 generate_password_hash.py
# Copia el hash nuevamente a index-secure.html
git add index-secure.html
git commit -m "Fix password hash"
git push
```

### "Error al cargar datos" en el dashboard
- Espera a que el workflow se ejecute (9 AM UTC o click manual en Actions)
- Verifica que GitHub Actions haya terminado sin errores

### Dashboard en blanco o 404
- Espera 5 minutos a que GitHub Pages actualice
- Verifica que settings → Pages apunte a `main` / `root`

## 🚀 Próximos pasos

**Tu dashboard está funcionando. Ahora:**

1. **Comparte con tu equipo**
   - URL: `https://TU-USUARIO.github.io/bepelican-ads-dashboard`
   - Contraseña: La que creaste
   - Todos usan la MISMA contraseña

2. **Personaliza**
   - Cambiar hora de actualización: `.github/workflows/update.yml` línea 5
   - Cambiar contraseña: ejecuta `generate_password_hash.py` nuevamente

3. **Monitorea**
   - Revisa Actions en GitHub para ver cuándo se actualizan los datos
   - Verifica que no haya errores en los logs

---

¿Dudas? Revisa `README.md` para más detalles de cada paso.
