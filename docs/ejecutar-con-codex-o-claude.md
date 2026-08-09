# Ejecutar desde cualquier lugar con Codex o Claude

Este repo debe funcionar como centro de mando. La PC actual, la PC de casa, RunPod, un VPS, Codex o Claude Code solo necesitan clonar el repo y tener secretos locales.

## Principio

- GitHub guarda codigo, documentacion, prompts, workflows y plantillas.
- Los secretos viven fuera del repo: `.env`, Bitwarden, variables del sistema, GitHub Actions Secrets o secretos del proveedor cloud.
- Los archivos pesados viven fuera de GitHub: Drive, OneDrive, Supabase Storage, S3, R2, RunPod Volume o Syncthing.

## Setup en una nueva maquina

```powershell
git clone https://github.com/jaaraque87/araque-solutions-os.git
cd araque-solutions-os
Copy-Item .\pipeline\.env.example .\pipeline\.env
```

Luego llenar `.env` con las claves reales desde Bitwarden o el gestor de secretos.

## Probar pipeline portable

```powershell
cd .\pipeline\comfydeploy_hyperframes
python .\run.py --brief .\examples\brief.example.json --mock-assets --skip-render
```

Esto no gasta creditos. Solo crea la estructura de ejecucion.

## Ejecutar con ComfyDeploy real

Configurar en `pipeline/.env`:

```text
COMFYDEPLOY_API_KEY=
COMFYDEPLOY_DEPLOYMENT_ID=
COMFYDEPLOY_API_BASE=https://api.comfydeploy.com/api
COMFYDEPLOY_RUN_URL=
```

Despues:

```powershell
cd .\pipeline\comfydeploy_hyperframes
$env:ARAQUE_ALLOW_GPU_EXECUTION="1"
python .\run.py --brief .\examples\brief.example.json --execute-real --confirm-cost SPEND_COMFYDEPLOY_CREDITS
```

La variable, la bandera y la frase son un gate conjunto. No se definen durante
desarrollo: sin las tres condiciones el runner falla antes de hacer el POST que
puede iniciar una GPU en ComfyDeploy.

## MVP one-click desde una imagen

Desde `pipeline/comfydeploy_hyperframes`:

```powershell
python .\one_click.py ..\..\brand\araque\araque-profile.jpg
```

Esto selecciona tres hooks ya puntuados desde `tools/hook-lab/clients`, genera
`brief.auto.json` y deja un proyecto HyperFrames listo para `check` y `preview`.
El modo predeterminado declara cero llamadas de red, no renderiza y no ejecuta
ComfyDeploy.

## Ejecutar HyperFrames

HyperFrames 0.7.18 requiere Node.js 22 o superior.

Verificar:

```powershell
node --version
npx hyperframes --version
```

Render manual desde una corrida:

```powershell
cd .\pipeline\comfydeploy_hyperframes\runs\<run_id>\hyperframes
npx hyperframes render --output output.mp4
```

## Prompt corto para Codex o Claude

```text
Trabaja en el repo araque-solutions-os. Revisa docs/ejecutar-con-codex-o-claude.md y pipeline/comfydeploy_hyperframes/README.md. Ejecuta primero el modo mock con --skip-render. Si pasa, prepara una corrida real usando las variables COMFYDEPLOY_* del entorno. No subas secretos ni archivos pesados.
```

## Reglas para agentes

- Antes de correr, hacer `git pull`.
- Despues de cambios utiles, hacer commit y push.
- Nunca commitear `.env`, tokens, renders, videos, modelos o zips.
- Si HyperFrames falla por Node, actualizar a Node 22 en esa maquina.
- Si ComfyDeploy cambia su API, ajustar solo `COMFYDEPLOY_RUN_URL` o el adaptador en `pipeline/comfydeploy_hyperframes/run.py`.
