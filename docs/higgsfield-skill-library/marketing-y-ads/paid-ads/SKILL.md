---
name: paid-ads
title: "Paid Ads"
category: Creative-marketing
version: 1.2.0
users: 385
source: https://higgsfield.ai/supercomputer/marketplace/skills/a83f614f-516b-2ede-2386-8a0f52744117
extracted: modal SKILL.md (via claude-in-chrome)
references (NO extraídas): ad-copy-templates.md, audience-targeting.md, conversion-tracking.md, platform-setup-checklists.md
---

# Paid Ads
Performance marketer para campañas en Google Ads, Meta, LinkedIn, TikTok, X.

## Before Starting
Chequear `.agents/product-marketing-context.md`. Gather: **Campaign Goals** (objetivo: awareness/traffic/leads/sales/installs; target CPA o ROAS; budget; constraints) · **Product & Offer** (qué se promociona, landing URL, por qué es compelling) · **Audience** (ICP, problema que resuelve, qué buscan, data para lookalikes) · **Current State** (ads previos, pixel/conversion data, funnel conversion rate).

## Platform Selection
| Plataforma | Mejor para | Usar cuando |
|---|---|---|
| Google Ads | tráfico high-intent de búsqueda | buscan activamente tu solución |
| Meta | demand gen, productos visuales | crear demanda, buenos creativos |
| LinkedIn | B2B, decision-makers | job title/company targeting importa, precio alto |
| Twitter/X | tech, thought leadership | audiencia activa en X |
| TikTok | 18-34, creativo viral | capacidad de video |

## Campaign Structure
Account → Campaign ([Objective]-[Audience/Product]) → Ad Set ([targeting]) → 3 Ads ([creative A/B/C]). **Naming:** `[Platform]_[Objective]_[Audience]_[Offer]_[Date]` (ej. `META_Conv_Lookalike-Customers_FreeTrial_2024Q1`).
**Budget:** testing (2-4 semanas) 70% proven / 30% test. Scaling: consolidar en ganadores, subir 20-30% por vez, esperar 3-5 días entre subidas (learning del algoritmo).

## Ad Copy Frameworks
PAS (Problem→Agitate→Solve→CTA) · BAB (Before→After→Bridge) · Social Proof Lead (stat/testimonial→qué hacés→CTA).

## Audience Targeting
Google: keywords/search intent. Meta: interests/behaviors/lookalikes. LinkedIn: job titles/companies/industries. **Lookalikes:** basar en mejores clientes (por LTV), no todos. **Retargeting:** segmentar por funnel stage. **Exclusions:** excluir clientes actuales y convertidos recientes.

## Creative Best Practices
**Image:** screenshots de UI, before/after, stats como focal, caras reales (no stock), texto bold <20%. **Video (15-30s):** Hook(0-3s pattern interrupt) → Problem(3-8s) → Solution(8-20s) → CTA(20-30s). Captions siempre (85% sin sonido), vertical para Stories/Reels, native > pulido, primeros 3s deciden. **Testing hierarchy:** concepto/ángulo (mayor impacto) > hook/headline > visual > body > CTA.

## Optimization
Métricas por objetivo: Awareness (CPM, reach, view rate) · Consideration (CTR, CPC, time on site) · Conversion (CPA, ROAS, conv rate).
- **CPA alto:** chequear landing page, tighten targeting, nuevos ángulos, mejorar quality score, ajustar bid.
- **CTR bajo:** creativo no resuena (nuevos hooks), audience mismatch, ad fatigue (refresh).
- **CPM alto:** audiencia muy narrow (expandir), competencia (otros placements), relevance baja.
- **Bid progression:** manual/cost caps → juntar 50+ conversiones → automated con targets → monitorear.

## Retargeting
Top (blog/video viewers → educacional/social proof) · Middle (pricing/feature visitors → case studies/demos) · Bottom (cart abandoners/trial → urgencia/objeciones). Windows: Hot 1-7d, Warm 7-30d (3-5x/sem), Cold 30-90d (1-2x/sem). Exclusiones: clientes, convertidos recientes (7-14d), bounced (<10s), páginas irrelevantes.

## Reporting
Weekly: spend vs budget, CPA/ROAS vs target, top/bottom ads, audience breakdown, frequency (fatiga), landing conv rate. **Atribución:** la de plataforma está inflada; usar UTMs consistentes, comparar con GA4, mirar blended CAC no solo platform CPA.

## Pre-Launch Checklist
Conversion tracking testeado con conversión real · landing <3s · mobile-friendly · UTMs funcionando · budget correcto · targeting matchea audiencia.

## Common Mistakes
Lanzar sin conversion tracking · muchas campañas (fragmenta budget) · no dar tiempo de learning · optimizar métrica equivocada · audiencias muy narrow/broad · no excluir clientes · un solo ad por ad set · no refrescar creativo · mismatch ad↔landing · cambios grandes de budget durante learning.

## Related Skills
ad-creative · copywriting · analytics-tracking · ab-test-setup · page-cro.
