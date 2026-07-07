---
name: writing-fragments
title: "Writing Fragments"
category: Writing-suite
users: 12
source: https://higgsfield.ai/supercomputer/marketplace/skills/7a584501-f6b7-ea23-f0b5-b0f24a4d31f5
extracted: modal SKILL.md (via claude-in-chrome) — single file
nota: parte de la "Writing-suite" — precede a [[writing-shape]] (mina fragmentos → luego se moldean en artículo).
---

# Writing Fragments
Sesión de grilling que produce **fragmentos**. Interrogar al usuario sin piedad sobre lo que estén pensando, capturando nuggets heterogéneos de escritura. A medida que emergen fragmentos (de cualquier lado de la conversación), appendearlos a un único archivo markdown. Si no dieron path, preguntar una vez y recordarlo. Capturar fragmentos desde lo primero que dice el usuario (incluido el prompt inicial). En la primera escritura, poner un H1 con working title y nada más.

## Qué es un fragmento
Cualquier pieza de texto que podría sobrevivir al artículo final. Debe ser **legible por el autor**. Deliberadamente heterogéneos. Ejemplos:
- Una oración filosa que querés deployar pero no sabés dónde.
- Un claim con justificación de una línea.
- Una viñeta: algo que pasó, un code snippet, un escenario, una analogía.
- Un half-thought ("algo sobre cómo X se siente como Y, resolver después").
- Una cita, diálogo, línea escuchada al pasar.
- Una lista de observaciones relacionadas que van juntas por feeling.
- Una queja, confesión, punchline.
Modelo: el diario del novelista — años de noticings no estructurados que luego se minan.

## File format
```
# Working title

Un primer fragmento vive acá.
Puede ser múltiples párrafos, listas, code, quotes.

---

Un segundo fragmento.

---

> Una línea citada que el usuario quiere guardar.
Una reacción a ella.
```
Fragmentos separados por horizontal rule (`\n---\n`). Sin headings dentro del body, sin tags, sin orden más allá del de aparición.

## Writing rhythm
Appendear en silencio (no pedir permiso por cada fragmento; mencionar al pasar). **Antes de cada escritura: re-leer el archivo desde disco** (el usuario puede haber editado/reordenado/borrado). El usuario puede decir "cut the last one", "rewrite that one sharper", "merge those two" en cualquier momento.
