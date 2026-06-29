# Sincronizacion entre PCs

Objetivo: poder trabajar desde esta PC y desde la PC de casa sin perder avances.

## Regla principal

GitHub se usa para codigo, documentacion tecnica, prompts, scripts, workflows y configuraciones limpias.

La nube tipo OneDrive, Google Drive o Syncthing se usa para archivos pesados:
videos, audios, imagenes grandes, instaladores, renders, zips, modelos y assets finales.

Las claves y tokens se guardan en Bitwarden o un gestor de contrasenas. Nunca se suben a GitHub.

## Repo principal

Repositorio remoto:

```text
https://github.com/jaaraque87/araque-solutions-os.git
```

Ruta en esta PC:

```text
C:\Users\SOPORTE2\Documents\araque-solutions-os
```

## Flujo diario

Antes de empezar en una PC:

```powershell
git pull
```

Despues de avanzar:

```powershell
git status
git add .
git commit -m "actualiza trabajo"
git push
```

En la otra PC:

```powershell
git clone https://github.com/jaaraque87/araque-solutions-os.git
```

Si ya existe clonado:

```powershell
git pull
```

## No subir a GitHub

- `.env`, `.env.local`, `secrets.sh`
- carpetas `.venv`, `node_modules`, `dist`, `build`
- videos, audios y renders
- modelos `.safetensors`, `.gguf`, `.bin`, `.pt`, `.ckpt`
- instaladores, zips grandes y backups completos

## Nota de orden

Si aparece una carpeta llamada `araque-solutions-os` dentro del mismo repo, normalmente es una copia local anidada. No debe subirse como parte del repo principal.
