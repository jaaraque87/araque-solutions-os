---
name: hf-humanizer
title: "Humanizer"
category: Writing-suite
version: 2.5.1
license: MIT
compatibility: claude-code opencode
users: 116
source: https://higgsfield.ai/supercomputer/marketplace/skills/8de9250f-4cab-79da-201f-734f47ef0d87
extracted: modal SKILL.md (via claude-in-chrome) — single file
relevante: alto — quitar el "AI look" de textos (basado en Wikipedia:Signs of AI writing)
description: "Elimina el 'AI look' de textos con 29 patrones detectables de escritura IA. Usar para pulir guiones, captions y copys antes de publicar."
---

# Humanizer: Remove AI Writing Patterns
Editor que identifica y quita señales de texto generado por IA para que suene humano.

## Task
1. Identificar patrones IA. 2. Reescribir secciones problemáticas. 3. Preservar el mensaje. 4. Mantener la voz/tono. 5. **Add soul** (no solo quitar patrones malos — inyectar personalidad). 6. Final anti-AI pass: preguntar "What makes the below so obviously AI generated?" → responder los tells restantes → "Now make it not obviously AI generated."

## Voice Calibration (opcional)
Si el usuario da una muestra de su escritura, analizarla antes: largo de oraciones, nivel de word choice, cómo arranca párrafos, hábitos de puntuación, tics recurrentes, transiciones. Reemplazar patrones IA con patrones de la muestra. Sin muestra → default (voz natural, variada, opinada).

## PERSONALITY AND SOUL (evitar escritura sin alma aunque sea "limpia")
Señales de soulless: todas las oraciones del mismo largo/estructura · sin opiniones · sin incertidumbre/sentimientos mezclados · sin primera persona cuando corresponde · sin humor/edge · lee como Wikipedia/press release.
Cómo dar voz: tener opiniones (reaccionar, no solo reportar) · variar el ritmo (cortas punchy + largas) · reconocer complejidad ("impressive but also kind of unsettling") · usar "I" cuando encaja · dejar algo de mess (tangentes, asides) · ser específico con los sentimientos.

## Los 29 patrones a eliminar
**CONTENIDO:** 1. Énfasis indebido en significancia/legado ("stands/serves as", "is a testament", "pivotal moment"). 2. Énfasis indebido en notabilidad/cobertura mediática (listar fuentes sin contexto). 3. Análisis superficial con "-ing" ("highlighting", "underscoring", "reflecting"). 4. Lenguaje promocional ("boasts a", "vibrant", "nestled", "stands as a vibrant"). 5. Atribuciones vagas/weasel words ("Experts argue", "Observers have cited"). 6. Secciones formulaicas "Challenges and Future Prospects".
**LENGUAJE/GRAMÁTICA:** 7. Vocabulario IA sobreusado ("delve", "crucial", "enhance", "fostering", "garner", "align with"). 8. Evitar "is/are" (copula avoidance: "serves as/marks/represents"). 9. Parallelismos negativos ("Not only...but", "It's not just X, it's Y"). 10. Rule of Three sobreusado. 11. Elegant variation (synonym cycling). 12. Falsos rangos ("from X to Y" sin escala real). 13. Voz pasiva y fragmentos sin sujeto.
**ESTILO:** 14. Em dash sobreusado (—). 15. Boldface mecánico. 16. Listas con headers inline+colon. 17. Title Case en headings. 18. Emojis decorativos. 19. Comillas curvas (""). 
**COMUNICACIÓN:** 20. Artefactos de chatbot ("I hope this helps", "Certainly!", "Would you like..."). 21. Disclaimers de knowledge-cutoff ("as of [date]", "While specific details are limited"). 22. Tono sicofántico/servil ("Great question!", "You're absolutely right!").
**FILLER/HEDGING:** 23. Frases filler ("In order to"→"To", "Due to the fact that"→"Because", "At this point in time"→"Now"). 24. Hedging excesivo ("could potentially possibly"). 25. Conclusiones positivas genéricas ("the future looks bright"). 26. Pares con guion sobreusados ("data-driven", "cross-functional", "client-facing"). 27. Tropos de autoridad persuasiva ("The real question is", "At its core", "what really matters"). 28. Signposting ("Let's dive in", "here's what you need to know"). 29. Headers fragmentados (heading + oración que restatea el heading).

## Process
Leer input → identificar patrones → reescribir → asegurar (suena natural en voz alta, estructura variada, detalles específicos, tono apropiado, is/are donde corresponde) → draft → "What makes this obviously AI?" (bullets breves) → "Now make it not obviously AI" → final.

## Output Format
Draft rewrite · "What makes the below so obviously AI generated?" (bullets) · Final rewrite · resumen de cambios (opcional).

## Referencia
Basado en **Wikipedia:Signs of AI writing** (WikiProject AI Cleanup). Insight clave: "LLMs use statistical algorithms to guess what should come next" → el resultado tiende a lo genérico/inflado.
