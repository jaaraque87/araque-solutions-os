# Adaptación a Araque Solutions — Hook Machine (Kane Kallaway)

Fuente: skill oficial distribuida gratis por Kallaway en su video "How To Create Irresistible Hooks With Claude" (youtube.com/watch?v=a7VjpIqq8Xk, mayo 2026). Prompt original para Cowork en `references/hook-machine-prompt-cowork-original.txt`.

## Qué hace y qué requiere

Investiga canales reales (IG/TikTok/YT Shorts) vía **Sandcastles MCP**: separa winners de losers con datos, extrae los hooks hablados de los transcripts, saca patrones (psicología, trigger words, gramática), construye rúbrica personalizada + librería de fórmulas mad-lib, y genera/califica/reescribe hooks A-F por tema.

**Requisitos para el flujo completo:**
1. Suscripción Sandcastles plan Pro+ ($49/mes) — analizar cada video gasta créditos.
2. Plugin MCP de Sandcastles instalado (https://help.sandcastles.ai/mcp).
3. Sin el MCP, los pasos de research (1-4) no corren; la rúbrica universal y el grading (pasos 7-10) SÍ funcionan standalone.

## Cómo se integra con hook-lab (división de trabajo)

- **hook-machine** = motor de research con datos reales + grading A-F. Responde "¿qué está funcionando YA en este nicho?"
- **hook-lab** = capa de conversión y producción. Aporta lo que hook-machine no tiene: niveles de conciencia de Schwartz (diagnóstico del cliente con bajas ventas), modos ALCANCE vs CONVERSIÓN, intake comercial, y export a `render-batch.mjs`.

**Flujo combinado para cliente nuevo:** intake (hook-lab) → research con hook-machine sobre los canales top del nicho del cliente → volcar format library y custom principles al `swipe.md` del cliente en `tools/hook-lab/clients/<cliente>/` → generar batería con fórmulas ganadoras + filtro de nivel de conciencia → hooks.json → batch render.

## Reglas de la casa

1. Los gates de gasto aplican: analizar videos gasta créditos Sandcastles — autorización del dueño antes de cada tanda.
2. **Idioma**: la skill es anglocéntrica. Los hooks para clientes salen en el idioma y registro del avatar comprador (español normalmente); las fórmulas mad-lib se adaptan, no se traducen literal.
3. El paso 6.5 (auto-actualizar el SKILL.md con datos personalizados) se REDIRIGE: los datos personalizados por cliente van al `swipe.md`/`hooks.json` del cliente, NO a este archivo — este skill file se mantiene limpio porque sirve a N clientes.
4. Atribución: es material de Kallaway distribuido gratis para uso propio. Se usa como herramienta interna de la agencia. NO se revende ni se rebrandea como producto white-label nuestro.
