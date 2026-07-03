# Voz oficial - Araque Solutions

Esta es la voz canon para piezas de Araque Solutions: reels, carruseles narrados, anuncios cortos, avatar reels y demos comerciales.

## Identidad

- Nombre interno: `araque_official`
- Proveedor: ElevenLabs
- Modelo objetivo: ElevenLabs v3 / expressive TTS
- Voice ID: `rzpLrJDiI1CBeAvkbjNf`
- Idioma principal: español latino neutro
- Uso: voz de marca para contenido de autoridad y venta de servicios con IA.

## Direccion vocal

La voz debe sonar como fundador/director de una agencia de contenido con IA:

- Natural, humana y directa.
- Autoridad sin sonar corporativa ni de radio.
- UGC premium: cercana, rapida, segura, con intención comercial.
- Energia media-alta, controlada.
- Ritmo agil para reels, con micro pausas antes de frases fuertes.
- Sin exagerar emociones, sin gritar, sin tono de "gurú".
- Cada frase debe sonar útil, vendible y concreta.

## Pronunciacion

- Araque Solutions: `A-ra-ke So-lu-shons`.
- IA: decir "inteligencia artificial" cuando la frase necesite claridad comercial; decir "IA" cuando el ritmo del reel lo pida.
- DM: decir "de eme".
- UGC: decir "iu yi si" solo si el público ya entiende el término; si no, decir "contenido estilo UGC".

## Tags recomendados para ElevenLabs v3

Usar tags en ingles y con moderacion:

- `[confident]` para autoridad.
- `[calm]` para explicacion.
- `[serious]` para tension comercial.
- `[curious]` para abrir preguntas.
- `[slightly excited]` para beneficios y CTA.
- `[short pause]` antes de remates.
- `[clear]` para marca, CTA y frases de cierre.
- `[whispers]` solo para contraste puntual, no como estilo base.

Evitar:

- Demasiados tags por linea.
- `[shouting]`, `[angry]`, `[crying]` o dramatizacion innecesaria.
- Frases largas sin puntuacion.

## Prompt base para copiar en ElevenLabs

```text
[confident] Habla como fundador de una agencia de contenido con inteligencia artificial.

[calm] Tono cercano, natural y directo. No suena como locutor de radio. No exagera. No grita.

[serious] Tiene autoridad, pero habla como alguien que ya probo el sistema, entiende el negocio y sabe vender sin humo.

[slightly excited] Ritmo rapido, estilo reel UGC premium, con pausas cortas antes de las frases importantes.

[clear] Acento latino neutro. Pronuncia Araque Solutions como: A-ra-ke So-lu-shons.

[confident] Cada frase debe sonar util, comercial y humana.
```

## Plantilla de guion para reels

```text
[serious] <Hook que abre tension>.

[short pause]

[confident] <Contraste o promesa>.

[calm] <Problema real del cliente>.

[serious] <Costo de no resolverlo>.

[confident] En Araque Solutions <mecanismo o solucion>.

[clear] <Lista corta de entregables>.

[slightly excited] <Resultado deseado>.

[confident] <CTA concreto>.
```

## Referencias locales de audio

Los audios de referencia viven localmente en `C:\Users\SOPORTE2\Downloads` y no se suben al repositorio:

| Archivo | Duracion aprox. | Formato |
|---|---:|---|
| `vozavatarreel1.mp3` | 33.41s | MP3 mono 44.1kHz |
| `avatarreel2.mp3` | 46.45s | MP3 mono 44.1kHz |
| `avatarreel3.mp3` | 18.99s | MP3 mono 44.1kHz |
| `avatarreel4.mp3` | 30.12s | MP3 mono 44.1kHz |
| `avatarreel5.mp3` | 24.19s | MP3 mono 44.1kHz |
| `avatarreel6.mp3` | 14.37s | MP3 mono 44.1kHz |
| `avatarreel7.mp3` | 28.53s | MP3 mono 44.1kHz |

## Regla de produccion

Para piezas finales, mantener el mismo `voice_id`, el mismo modelo, los mismos settings y esta direccion vocal. Ajustar solo energia y pausas segun el formato.
