---
name: ARAQUE SOLUTIONS — Sistema IA Completo
description: Agencia de influencers IA con pipeline UGC automatizado + modelo white label para vender a otras agencias
type: project
originSessionId: 3e0c87e5-a84e-40d4-94af-35693ec06c7e
---
ARAQUE SOLUTIONS es el nombre provisional de la agencia del usuario. Sistema de producción de videos UGC con influencers virtuales, con visión de convertirse en un producto white label / franquicia para otras agencias.

**Why:** Construir un sistema escalable, demostrable, ejecutable y vendible a otras agencias.
**How to apply:** Cuando el usuario pida trabajo sobre el pipeline, la guía, el dashboard, los scripts o el modelo de negocio — este es el contexto completo.

---

## Stack técnico (producción interna)

1. **Kenza UGC Pipeline** — 12 scripts Python en `C:\Users\SOPORTE2\Documents\Kenza UGC Pipeline\`
2. **LTX23_Scripts** — 10 scripts bash RunPod en `C:\Users\SOPORTE2\Downloads\LTX23_Scripts\`
3. **NORA** — plataforma interna de gestión (ver project_nora.md)
4. **Guía interactiva** — `docs/guia-araque-solutions.html`

## Modelo de negocio — Servicios al cliente final

### Servicio A: Influencer Virtual "llave en mano"
- Setup único: $1,500 (personaje custom + LoRA + voz)
- Mantenimiento: $497/mes (60 videos/mes)

### Servicio B: UGC Videos IA para marca existente ← ANCLA
- $297/mes (30 videos) / $497/mes (60 videos)
- Sin setup fee — entrega en 48h

### Servicio C: Pack único
- $15-25/video, mínimo 20 videos

### Costos reales por video:
- Sin opcionales: ~$3.27 | Con todo: ~$3.87
- Margen neto Servicio B ($497/60 videos): ~$270-370/mes por cliente

---

## Modelo ESCALABLE — White Label / Franquicia para otras agencias

### Visión (decidida 2026-05-19):
Convertir todo el stack en un producto vendible a otras agencias de marketing que quieran ofrecer UGC con IA sin construir la infraestructura desde cero.

### 3 productos para agencias:

**PRODUCTO 1 — "Agency Starter Kit" (one-time $2,997)**
Todo lo que necesita una agencia para empezar:
- Scripts de instalación RunPod (LTX23_Scripts completo)
- 12 scripts Python del pipeline UGC
- Workflow TODOENUNO + MVC V5.1
- Guía de operador (HTML interactiva)
- Personaje genérico de arranque (no Kenza)
- 1 llamada de onboarding (1h)
- Soporte por 30 días

**PRODUCTO 2 — "Agency OS" (SaaS $197/mes)**
Dashboard NORA white label + infraestructura gestionada:
- Frontend Next.js con su logo/colores
- Backend FastAPI conectado a sus API keys
- Panel de clientes, videos, facturación básica
- Actualizaciones automáticas de modelos
- Soporte continuo

**PRODUCTO 3 — "Done For You" ($4,997 setup + $297/mes)**
Araque Solutions opera TODO por ellos:
- Crean el influencer IA del cliente de la agencia
- Producen los videos
- La agencia revende a precio premium ($997+/mes)
- Markup garantizado: ~3-4x

### Propuesta de valor diferencial:
- No venden prompts ni plantillas → venden infraestructura operativa
- Scripts reproducibles en cualquier pod en el mundo (run_all.sh)
- Costo de producción documentado y auditado ($3.27/video)
- Workflow TODOENUNO analizado y mapeado — no es caja negra
- Personaje Kenza como demo proof-of-concept (con video real)

---

## Roadmap para hacer esto vendible

### FASE 1 — Proof of concept (PENDIENTE)
- [ ] Primer video de Kenza completo con TODOENUNO (I2V + lipsync)
- [ ] Demo reel 60s: 3 videos distintos de Kenza
- [ ] 1 cliente real pagando (valida el pipeline completo)

### FASE 2 — Producto (después del primer cliente)
- [ ] Escribir los 12 scripts Python del pipeline
- [ ] Backend FastAPI wrapping los scripts
- [ ] Frontend Next.js (dark #09090b, accent lime #a3e635)
- [ ] Deploy: Vercel (frontend) + Railway/VPS (backend)

### FASE 3 — Escalabilidad (después de 3 clientes)
- [ ] Documentar el sistema completo como "Agency Starter Kit"
- [ ] Landing page de venta (agencias como target)
- [ ] Onboarding automatizado con el run_all.sh como base
- [ ] Soporte vía comunidad (Discord / Slack)

### FASE 4 — Franquicia (meta 6-12 meses)
- [ ] 10 agencias usando el sistema
- [ ] Marketplace de personajes (Kenza + otros)
- [ ] Revenue share por volumen de videos

---

## Estructura de archivos operativa

```
C:\Users\SOPORTE2\Documents\
├── ARAQUE_SOLUTIONS\
│   ├── _clientes\           (un folder por cliente)
│   ├── _personajes\         (kenza\ + generico_01\)
│   ├── _scripts\            (los 12 scripts Python)
│   └── _reportes\           (métricas mensuales)
├── Kenza UGC Pipeline\      (pipeline activo)
└── LTX23_Scripts\           (scripts RunPod, listos)
```

## Referencias / Inspiración
- Pipeline source: Morfeo Academy / morfeo-engine GitHub (Paul de Lavallaz)
- Competencia: Aitana López (The Clueless, España) — $10K/mes
- Stack UI: Express API + Python pipeline + Next.js (puerto 3336)
