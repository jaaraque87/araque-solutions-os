---
name: ab-test-setup
title: "A/B Test Setup"
category: Creative-marketing
version: 1.2.0
users: 11
source: https://higgsfield.ai/supercomputer/marketplace/skills/ee76341e-c8b0-8f1c-c605-4cc55c6b31cf
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): sample-size-guide.md, test-templates.md
---

# A/B Test Setup
Diseñar tests que producen resultados accionables y confiables.

## Initial Assessment
Chequear `.agents/product-marketing-context.md`. Entender: Test Context (qué mejorar, qué cambio) · Current State (baseline conversion rate, tráfico) · Constraints (complejidad, timeline, tools).

## Core Principles
1. **Start with a Hypothesis** (predicción específica basada en razón/data, no "a ver qué pasa"). 2. **Test One Thing** (una variable). 3. **Statistical Rigor** (pre-determinar sample size, no peekear ni parar antes). 4. **Measure What Matters** (primary metric = valor de negocio, secondary para contexto, guardrail para prevenir daño).

## Hypothesis Framework
`Because [observation/data], we believe [change] will cause [outcome] for [audience]. We'll know when [metrics].`
Débil: "cambiar color del botón puede subir clicks." Fuerte: "Porque los usuarios reportan dificultad para encontrar el CTA (heatmaps+feedback), creemos que hacerlo más prominente subirá los clicks..."

## Test Types
A/B (dos versiones, un cambio, tráfico moderado) · A/B/n (múltiples variantes, alto) · MVT (combinaciones, muy alto) · Split URL (URLs distintas, moderado).

## Sample Size (quick ref por baseline / lift)
Baseline 5%: 150k/variant (10% lift), 39k (20%), 6k (50%). 10%: 12k (10%), 3k (20%), 550 (50%). Calculadoras: Evan Miller, Optimizely.

## Metrics
**Primary** (una, atada a la hipótesis, para llamar el test) · **Secondary** (explican por qué/cómo funcionó) · **Guardrail** (no deben empeorar; parar si negativo). Ej pricing page: Primary=plan selection rate, Secondary=time on page/plan distribution, Guardrail=support tickets/refund rate.

## Variants
Variar: Headlines/Copy (ángulo, value prop, tono) · Visual (layout, color, imágenes, jerarquía) · CTA (copy, tamaño, placement, número) · Content (info, orden, cantidad, social proof). Un cambio significativo, bold, fiel a la hipótesis.

## Traffic Allocation
Standard 50/50 (default) · Conservative 90/10, 80/20 (limitar riesgo) · Ramping (empezar chico, subir; mitigación de riesgo técnico). Consistencia (mismo variant al volver), exposición balanceada por hora/día.

## Implementation
Client-side (JS post-load, rápido, flicker; PostHog/Optimizely/VWO) vs Server-side (variant antes de render, sin flicker, dev work; PostHog/LaunchDarkly/Split).

## Running
Pre-launch checklist: hipótesis documentada, primary metric, sample size, variantes correctas, tracking verificado, QA. **Durante:** monitorear issues técnicos; NO peekear/parar antes, NO cambiar variantes, NO agregar tráfico de fuentes nuevas. **Peeking problem:** mirar antes del sample size y parar → falsos positivos.

## Analyzing
Significancia: 95% confidence = p<0.05 (<5% chance de random, es threshold no garantía). Checklist: ¿alcanzó sample size? ¿significativo (CIs)? ¿effect size relevante (vs MDE)? ¿secondary consistentes? ¿guardrails ok? ¿diferencias por segmento?
Interpretación: winner→implementar · loser→mantener control+aprender por qué · sin diferencia→más tráfico o test más bold · mixed→profundizar/segmentar.

## Growth Experimentation Program
**Experiment Loop:** generar hipótesis (data/research/competidores/feedback) → priorizar con ICE → diseñar+correr → analizar → promover ganadores a playbook → nuevas hipótesis → repetir.
**ICE Prioritization:** Impact + Confidence + Ease (1-10 c/u) / 3. Correr los de score más alto, re-score mensual.
**Velocity targets:** 4-8 experimentos/mes · win rate 20-30% (mature) · duración 2-4 sem · backlog 20+ hipótesis · cumulative lift.
**Playbook:** por cada ganador documentar el patrón reusable (Hypothesis, Sample, Result+CI+p, Guardrails, Segment deltas, por qué funcionó, Pattern, Apply to, Status).
**Cadence:** weekly (issues+guardrails, no llamar ganadores antes) · bi-weekly (concluir, actualizar playbook, lanzar siguiente) · monthly (velocity/win rate/lift, replenish backlog, re-priorizar ICE) · quarterly (auditar playbook).

## Common Mistakes
Design: cambio muy chico (indetectable), muchas cosas (no aísla), sin hipótesis. Execution: parar antes, cambiar mid-test, no chequear implementación. Analysis: ignorar CIs, cherry-pick segments, sobre-interpretar inconclusos.

## Related Skills
page-cro · analytics-tracking · copywriting.
