---
name: writing-shape
title: "Writing Shape"
category: Writing-suite
users: 8
source: https://higgsfield.ai/supercomputer/marketplace/skills/c3f2e268-24d2-1b95-142e-6500931a11e1
extracted: modal SKILL.md (via claude-in-chrome) — single file
---

# Writing Shape
Tomar un markdown de material crudo (el "pile") y moldearlo en un artículo mediante una sesión conversacional. NO editar el archivo crudo — producir un documento de artículo separado. Si el usuario no dijo dónde guardarlo, preguntar una vez y recordar el path.

## The Loop
1. **Read the pile:** leer el input completo, formar sentido de lo que hay.
2. **Draft 2–3 candidate openings:** cada opening implica una tesis/ángulo distinto; mostrar todas, forzar al usuario a elegir.
3. **Grow paragraph by paragraph:** tras aterrizar el opening, preguntar "dado este opening, ¿qué necesita oír el lector ahora?" y traer material del pile.
4. **Append al archivo del artículo a medida:** no batchear; escribir cada párrafo/bloque acordado inmediatamente para que el usuario vea el artículo tomando forma.
5. Loop del paso 3 hasta terminar (el usuario decide cuándo).

## Conversational feel (grilling invertido)
Moves a usar: "¿Qué hace este párrafo por el lector que el anterior no hizo?" · "Si corto esto, ¿qué se rompe?" · "¿Es prosa, o debería ser lista? ¿Por qué prosa?" · "Esta oración hace dos trabajos — partila o elegí uno." · "El opening prometió X, derivamos a Y — re-threadealo o cambiá el opening."

## Pulling from the pile (cantera, no script)
Sacar un fragmento, reworkearlo para el contexto. Si el pile carece de algo que el artículo necesita, nombrar el gap explícito ("We need an example here and the pile doesn't have one").

## Format arguments (discutir tradeoffs en voz alta)
- **Prosa vs lista:** prosa lleva argumento; listas llevan items paralelos (si no son verdaderamente paralelos, prosa).
- **Inline vs callout:** tips/warnings/asides en callouts (`> [!TIP]`, `> [!NOTE]`) solo si descarrilarían el argumento principal.
- **Table vs estructura repetida:** si la misma forma se repite 3+ veces con los mismos fields, tabla; si no, prosa con bold leads.
- **Quote vs paraphrase:** citar cuando el wording original ES el punto; parafrasear cuando solo importa la idea.
- **Code block vs inline:** multi-línea/runnable/ilustrativo → block; single token/identifier → inline.

## Writing rhythm
Append al archivo a medida que se acuerda cada bloque. **Re-leer el archivo desde disco antes de cada escritura.**

## Out of scope
No minar fragmentos nuevos que no están en el pile (si está incompleto, nombrar el gap) · no editar el archivo crudo · no publicar/formatear para plataforma ni agregar frontmatter no pedido.
