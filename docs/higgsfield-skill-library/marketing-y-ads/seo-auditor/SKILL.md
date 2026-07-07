---
name: seo-auditor
title: "SEO Auditor"
author: mixing_pickle_3000
category: Writing-suite
users: 35
source: https://higgsfield.ai/supercomputer/marketplace/skills/343a4f4f-06cf-47fb-8c7e-bcf1df3e4941
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): agents/openai.yaml, audit-coverage.md
---

# SEO Auditor
Workflow de auditoría SEO técnica (crawlability, indexing, Core Web Vitals, estructura).

## Output Contract
Crear exactamente un deliverable `TODO_seo-auditor.md` en el workspace (salvo que pidan otro). Markdown con checkbox tasks trackeables. IDs estables: findings `SEO-FIND-<section>.<number>` · recomendaciones `SEO-REC-...` · verificación `SEO-VERIFY-...` · código `SEO-CODE-...`. Usar fenced code blocks para diffs, JSON-LD, config, comandos.

## Discovery First
Antes de auditar establecer: Site URL y scope (full/subdomain/template/sección) · target markets/idiomas/regiones · business/conversion goals + keyword themes · competidores/benchmarks · evidencia disponible (crawl exports, Search Console, GA4, Lighthouse/PageSpeed, backlinks). Si falta contexto esencial, documentar como assumption/data-gap.

## Audit Workflow
1. **Discovery & crawl** (URLs, status codes, redirect chains, canonicals, robots, sitemap coverage). 2. **Technical health** (CWV, TTFB, HTTPS, certs, mixed content, mobile, viewport). 3. **On-page & content** (titles, meta descriptions, heading hierarchy, content depth, duplicate/thin content, E-E-A-T). 4. **Off-page & competitive** (backlink quality, anchor diversity, toxic links, authority proxies). 5. **Roadmap & reporting** (score por impacto/effort/ROI; agrupar en Immediate/Short-term/Strategic).

## Required TODO Structure (secciones top-level)
Context (SEO-CTX: Site URL, Scope, Markets, Goals, Keyword Themes, Competitors, Evidence Sources) · Audit Findings (SEO-FIND: Location, Description, Evidence, Impact Critical/High/Medium/Low, Effort, ROI, Recommendation) · Remediation Recommendations (SEO-REC: Priority, Effort, Expected Outcome, Validation) · Proposed Code Changes (SEO-CODE: Files, Patch) · Commands (SEO-CMD: Local, CI) · QA Checklist (SEO-VERIFY: evidencia específica, evidencia de críticos, benchmark de competidores, cita de guidelines, code examples, validación medible, ROI grounded).

## Recommendation Rules
Priorizar impacto medible en tráfico orgánico/conversión/revenue sobre volumen de issues · separar quick wins (<1h) de iniciativas estratégicas (días/semanas) · incluir expectativas before/after (CWV, indexing, rankings, tráfico, CTR, conversión) · citar Google Search Central / PageSpeed / Schema.org · **NUNCA recomendar cloaking, hidden text, link schemes, doorway pages, spam automatizado, fake reviews.**

## Evidence Handling
Usar tools/data live cuando estén disponibles y registrar evidencia. Aceptable: URLs+status codes, robots.txt+sitemap, Lighthouse/PageSpeed/CWV, Search Console+GA4, validador de structured data, backlink exports, code locations de metadata/redirects/schema/routing, screenshots solo si los piden/proveen.
