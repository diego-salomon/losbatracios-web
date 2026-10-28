"""Web de Los Batracios, v5.
Genera dos cosas desde el mismo contenido:
  sitio/   la web lista para publicar en un dominio (ES en /, EN en /en/, privacidad, SEO completo)
  vista/   la vista previa para el artifact de Claude (una sola página con botón de idioma)
"""
from PIL import Image
import base64, json, pathlib, shutil

R = pathlib.Path(__file__).resolve().parent


def _copia(src, dst):
    """Copia un archivo; si falta (fuentes con licencia, press kits), avisa y sigue."""
    src = pathlib.Path(src)
    if not src.exists():
        print('aviso: falta', src.relative_to(R), '(se omite)')
        return
    shutil.copy(src, dst)


def _lee(path):
    path = pathlib.Path(path)
    return path.read_bytes() if path.exists() else b''
DOM = 'https://losbatracios.com'
UMAMI_ID = 'd8a1574c-2c2b-450b-9d00-d00bf395b85f'
BUTTONDOWN = 'los_batracios'
HOY = '2026-10-14'
TURNSTILE_SITEKEY = '0x4AAAAAAFWlssqC16mA5Eh2'  # la Site Key pública del widget de Turnstile; vacía = sin Turnstile

LB = 'https://letterboxd.com/film/the-batrachians/'
TR = {'es': 'https://youtu.be/5gL_O2GYxDU', 'en': 'https://www.youtube.com/watch?v=iKg7xyXAgCs'}
IG = 'https://www.instagram.com/batraciospeli/'
TT = 'https://www.tiktok.com/@batraciospeli'
XX = 'https://x.com/batraciospeli'
FB = 'https://www.facebook.com/profile.php?id=61595381789779'
MAIL = 'losbatraciospeli@gmail.com'

TXT = {
 'titulo': {'es': 'los batracios', 'en': 'the batrachians'},
 'title_tag': {'es': 'Los Batracios (2025), película de Diego Salomon', 'en': 'The Batrachians (2025), a film by Diego Salomon'},
 'meta': {'es': 'Una comedia sobre cómo nos tratamos, con Sofía Ciffoni, Jósbel Lobo, Andreina Crepsac y Oscar Belloso. Premio del Público, Mammoth Lakes 2025.',
          'en': "They're just trying to stay afloat. With Sofía Ciffoni, Jósbel Lobo, Andreina Crepsac and Oscar Belloso. Audience Award, Mammoth Lakes 2025."},
 'sinopsis': {'es': 'Una velada entre amigos se convierte en un campo de batalla emocional cuando las tensiones de una pareja los llevan a todos a cuestionar la solidez de sus vínculos.',
              'en': "An evening among friends turns into an emotional battlefield when a couple's tension leads everyone to question the strength of their bonds."},
 'h_sin': {'es': 'sinopsis', 'en': 'synopsis'},
 'h_eq': {'es': 'reparto y equipo', 'en': 'cast and crew'},
 'h_pr': {'es': 'prensa', 'en': 'press'},
 'pk': {'es': 'descargar press kit', 'en': 'download press kit'},
 'h_fu': {'es': 'próxima función', 'en': 'next screening'},
 'fu_fecha': {'es': '22 al 27 de noviembre de 2026', 'en': 'November 22 to 27, 2026'},
 'h_su': {'es': 'sigue a la película', 'en': 'follow the film'},
 'su_txt': {'es': 'Te avisamos de cualquier novedad.', 'en': 'We will let you know about anything new.'},
 'su_btn': {'es': 'avísame', 'en': 'keep me posted'},
 'su_baja': {'es': 'Escribimos poco. Te das de baja cuando quieras.', 'en': 'We write rarely. Unsubscribe anytime.'},
 'lb_txt': {'es': '¿Ya la viste?', 'en': 'Seen it?'},
 'lb_btn': {'es': 'cuéntalo en letterboxd', 'en': 'review on letterboxd'},
 'privacidad': {'es': 'privacidad', 'en': 'privacy'},
 'firma': {'es': 'una película de diego salomon', 'en': 'a film by diego salomon'},
 'otro_idioma': {'es': 'English', 'en': 'Español'},
 'alt_casa': {'es': 'Dibujo de una sala vista desde arriba: cuatro amigos en un sofá, una lámpara, una librería y una mesa con bancos',
              'en': 'Drawing of a living room seen from above: four friends on a sofa, a lamp, a bookshelf and a table with benches'},
}
GLOBOS = [  # clase, destino, texto, evento de medición
 ('g1', 'trailer', {'es': 'mira el tráiler', 'en': 'watch the trailer'}, 'burbuja-trailer'),
 ('g2', LB, {'es': 'guárdala en letterboxd', 'en': 'save it on letterboxd'}, 'burbuja-letterboxd'),
 ('g3', '#suscribir', {'es': 'avísame de las funciones', 'en': 'tell me about screenings'}, 'burbuja-funciones'),
 ('g4', IG, {'es': 'síguenos', 'en': 'follow us'}, 'burbuja-instagram'),
]
CREDITOS = [
 ({'es': 'guion y dirección', 'en': 'writer-director'}, 'Diego Salomon'),
 ({'es': 'con', 'en': 'with'}, 'Sofía Ciffoni, Jósbel Lobo, Andreina Crepsac, Oscar Belloso &amp; Mochi'),
 ({'es': 'producción', 'en': 'producers'}, 'Samuel Rotter, Carolina Perelman, José Daniel Bort &amp; Rodolfo Cova'),
 ({'es': 'fotografía', 'en': 'cinematography'}, 'Jordan Tetewsky'),
 ({'es': 'edición', 'en': 'editing'}, 'Mayra Morán'),
 ({'es': 'sonido', 'en': 'sound'}, 'Isabella Salvo &amp; Daniel Rincón García'),
 ({'es': 'música', 'en': 'music'}, 'Pedro Fraguela'),
]
PRENSA = [
 ("Film Carnage", "https://filmcarnage.com/2025/05/29/review-the-batrachians-los-batracios/"),
 ("Cinemathon", "https://cinemathon.wordpress.com/2025/09/29/diego-salomon-me-gustaria-pensar-que-mi-pelicula-es-un-arbol-de-mango-sembrado-en-espana/"),
 ("El Universal", "https://www.eluniversal.com/el-universal/209078/los-batracios"),
 ("Correo Cultural", "https://correocultural.com/2025/06/reflejos-de-la-realidad-los-batracios-capturan-el-corazon-del-publico/"),
]
LAURELES = [
 ('mammoth', '', {'es': 'Mammoth Lakes Film Festival, Premio del Público', 'en': 'Mammoth Lakes Film Festival, Audience Award'}),
 ('not', ' class="alto"', {'es': 'Nòt Film Fest, Mención Especial del Jurado Shooting Stars por Interpretación', 'en': 'Nòt Film Fest, Shooting Stars Special Jury Mention for Performance'}),
 ('kyiv', '', {'es': 'Molodist Kyiv International Film Festival, Selección Oficial', 'en': 'Molodist Kyiv International Film Festival, Official Selection'}),
 ('elco', '', {'es': 'Festival de Cine ELCO, Selección Oficial', 'en': 'ELCO Film Festival, Official Selection'}),
]

# íconos de Simple Icons (CC0) para enlazar a las redes
ICONOS = {'facebook': 'M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z', 'instagram': 'M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077', 'tiktok': 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z', 'x': 'M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z'}

CSS = """
/* Dos pantallas. 1: la sala del afiche y una conversación de Habbo Hotel: cada personaje dice adónde ir.
   2: la película (azul) y seguirla (blanco). En el teléfono, seguirla va justo después de la sinopsis.
   Globos y botones con la forma de los de Habbo, lisos, sin píxel. */
:root{
  --papel:#ffffff; --tinta:#1f2340; --azul:#263e99; --rojo:#b12025; --gris:#5e6385; --noche-etq:#c3c8e6;
  --sans:'Aeonik','Instrument Sans','Helvetica Neue',Arial,sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);font-family:var(--sans);font-size:17px;line-height:1.45;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block;height:auto}
p,h1,h2,dl,dd,dt{margin:0;padding:0}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1.5px}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--azul);outline-offset:3px}

.idioma{position:absolute;top:18px;right:24px;z-index:6;font:inherit;font-size:14px;color:var(--gris);background:none;border:0;padding:6px 2px;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.idioma:hover{color:var(--azul)}

/* cabecera: el título como en el afiche. Se queda fija arriba y la segunda pantalla sube hasta ella */
.cabecera{position:fixed;top:0;left:0;right:0;z-index:8;padding:22px 24px 16px;background:var(--papel)}
.cabecera h1{display:inline-block;font-size:clamp(48px,7.4vw,150px);line-height:.9;font-weight:700;letter-spacing:-.045em;color:var(--rojo);text-transform:lowercase;white-space:nowrap}
.cabecera h1 .firma{display:block;text-align:left;margin-top:.12em;margin-left:.05em;font-size:.2em;font-weight:700;letter-spacing:-.005em;line-height:1.1;color:var(--azul)}

/* pantalla 1: el dibujo, quieto mientras sube la segunda pantalla */
.uno{position:sticky;top:0;height:100svh;overflow:hidden;background:var(--papel)}
.escena{--w:min(72vw,calc((95svh - var(--cab,170px)) * 1.2531));position:absolute;left:calc(50vw - var(--w) / 2);top:calc(var(--cab,170px) + 1svh);width:var(--w);z-index:2;font-size:clamp(12px,calc(var(--w) * .0165),17px)}
.escena picture,.escena>img{display:block;width:100%}
.escena picture img{width:100%}
.dos{position:relative;z-index:5;scroll-margin-top:var(--cab,190px);min-height:calc(100svh - var(--cab,190px))}
.der{background:var(--papel)}
.bajar{position:absolute;z-index:4;left:50%;bottom:14px;width:34px;height:34px;margin-left:-17px;display:grid;place-items:center;color:var(--tinta);text-decoration:none}
.bajar svg{width:22px;height:14px}

/* globo de chat de Habbo, liso. La punta del pico cae sobre la cabeza de cada personaje */
.globo-h{position:absolute;z-index:4;display:block;text-decoration:none;color:var(--tinta);filter:drop-shadow(0 3px 0 rgba(31,35,64,.18));transform:translate(calc(-1 * var(--p) - 8px),calc(-100% - var(--cola,11px)))}
.globo-h .caja{display:block;background:var(--papel);border:2px solid var(--tinta);border-radius:9px;padding:.6em .9em;white-space:nowrap}
.globo-h .dice{font-weight:700;font-size:1em;line-height:1}
.globo-h .pico{position:absolute;top:calc(100% - 2px);left:var(--p,14px);width:16px;height:calc(var(--cola,11px) + 2px);overflow:visible}
.globo-h:hover .caja,.globo-h:focus-visible .caja{background:#eef1fb}
.globo-h:hover .dice,.globo-h:focus-visible .dice{color:var(--azul);text-decoration:underline;text-underline-offset:3px}
/* g1 Lorena, g2 Andreína, g3 David, g4 Mauro (en % del dibujo) */
.g1{left:26.5%;top:42.2%;--p:calc(100% - 30px)}
.g2{left:32.2%;top:39.2%;--p:calc(100% - 30px);--cola:3.7em}
.g3{left:38.6%;top:32.6%;--p:14px;--cola:5.5em}
.g4{left:52.6%;top:30.4%;--p:14px}

/* entrada, como en Familiar Touch: el dibujo se materializa, los personajes hablan, aparece el título */
@media (prefers-reduced-motion:no-preference){
  .escena picture,.escena>img{animation:aparece 4.5s ease-out both}
  @keyframes aparece{0%{opacity:0;filter:blur(22px)}100%{opacity:1;filter:blur(0)}}
  .cabecera h1{animation:titulo 2s ease-out 4.2s both}
  @keyframes titulo{0%{opacity:0}100%{opacity:1}}
  .bajar{animation:titulo 1.4s ease-out 7s both}
  .bajar svg{animation:respira 2.4s ease-in-out infinite}
  @keyframes respira{0%,100%{transform:translateY(0);opacity:.55}50%{transform:translateY(6px);opacity:1}}
  .escena.vivo .globo-h{opacity:0;translate:0 6px;pointer-events:none;transition:opacity .35s ease,translate .35s ease}
  .escena.vivo .globo-h.ve,.escena.vivo .globo-h:focus-visible{opacity:1;translate:0 0;pointer-events:auto}
  .globo-h.habla{animation:habla .5s steps(3)}
  /* cuando el dibujo está nítido, los globos flotan un poco */
  .flota .globo-h{animation:flota 3.8s ease-in-out infinite}
  .flota .g2{animation-delay:-1s;animation-duration:4.3s}.flota .g3{animation-delay:-2.1s;animation-duration:3.5s}.flota .g4{animation-delay:-.6s;animation-duration:4.6s}
  @keyframes flota{0%,100%{translate:0 0}50%{translate:0 -5px}}
  @keyframes habla{0%,100%{translate:0 0}40%{translate:0 -6px}}
}

/* botones y campos con el volumen de los de Habbo */
.boton-h{display:inline-block;border:2px solid var(--tinta);border-radius:9px;text-decoration:none;font:inherit;cursor:pointer;align-self:flex-start;padding:0;background:none;box-shadow:0 3px 0 rgba(31,35,64,.25);transition:transform .12s,box-shadow .12s}
.boton-h>span{display:block;font-weight:700;font-size:17px;line-height:1;padding:12px 18px;border-radius:7px;background:var(--fondo,var(--rojo));color:var(--letra,var(--papel));box-shadow:inset 0 3px 0 rgba(255,255,255,.28),inset 0 -3px 0 rgba(0,0,0,.18)}
.boton-h:hover{transform:translateY(-3px);box-shadow:0 6px 0 rgba(31,35,64,.35)}
.boton-h:hover>span,.boton-h:focus-visible>span{background:var(--hover,var(--papel));color:var(--letra-h,var(--rojo))}
.izq .boton-h:hover>span{box-shadow:inset 0 0 0 2px var(--papel)}
.boton-h:active{transform:translateY(2px);box-shadow:0 1px 0 rgba(31,35,64,.25)}
.campo-h{display:block;flex:1 1 220px;min-width:0}
.campo-h input{display:block;width:100%;border:2px solid var(--tinta);border-radius:9px;font:inherit;font-size:16px;padding:11px 12px;background:var(--papel);color:var(--tinta);box-shadow:inset 0 3px 0 rgba(31,35,64,.10)}
.campo-h input:focus{outline:none;background:#eef1fb}

/* pantalla 2 */
.dos{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);grid-template-rows:auto 1fr;grid-template-areas:"a c" "b c"}
.bloque{display:flex;flex-direction:column;gap:clamp(16px,3svh,28px);padding:0 clamp(24px,4.5vw,72px)}
.bloque>*{max-width:560px}
.bloque h2{font-size:15px;font-weight:700;text-transform:lowercase;margin-bottom:8px}
.izq{background:var(--azul);color:var(--papel)}
.izq h2{color:var(--noche-etq)}
.a{grid-area:a;padding-top:clamp(28px,5svh,64px)}
.b{grid-area:b;padding-top:clamp(16px,3svh,28px);padding-bottom:clamp(20px,4svh,64px)}
.c{grid-area:c;justify-content:flex-start;padding-top:clamp(28px,5svh,64px);padding-bottom:clamp(20px,4svh,64px)}
.c h2{color:var(--rojo)}
.sinopsis{font-size:clamp(20px,1.75vw,25px);line-height:1.3;font-weight:700;text-wrap:balance}
.laureles{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:nowrap;margin-top:clamp(12px,2svh,22px)}
.laureles{--gl:clamp(56px,5vw,80px)}
/* tamaño óptico: cada laurel se escala por su forma y por cuánta tinta tiene, no por el tamaño del archivo */
.laureles img{width:auto;min-width:0;height:calc(var(--gl) * var(--f))}
.l-mammoth{--f:.718}.l-not{--f:.957}.l-kyiv{--f:.70}.l-elco{--f:.52}
.equipo{display:grid;grid-template-columns:auto minmax(0,1fr);gap:3px 16px;font-size:16px}
.equipo dt{color:var(--noche-etq)}
.equipo dd{text-transform:lowercase}
.prensa{display:flex;flex-wrap:wrap;gap:4px clamp(10px,1.3vw,18px);font-size:clamp(14px,1.2vw,16px)}
.izq .boton-h{--fondo:var(--papel);--letra:var(--azul);--hover:var(--azul);--letra-h:var(--papel)}
.izq .boton-h{border-color:var(--papel)}
.material{display:flex;flex-direction:column;gap:12px}
.material .boton-h{--fondo:var(--papel);--letra:var(--azul);--hover:var(--azul);--letra-h:var(--papel);border-color:var(--azul)}

.suscribir form{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.nota{font-size:14px;color:var(--gris)}
.suscribir .baja{margin-top:8px}
.resena{margin-top:clamp(14px,2.6svh,26px);display:flex;flex-direction:column;gap:10px}
.funcion b{display:block}
.pie{display:flex;flex-direction:column;gap:clamp(12px,2.2svh,22px);margin-top:auto}
.contacto{display:flex;align-items:center;flex-wrap:wrap;gap:12px 22px}
.contacto .nota a{color:var(--tinta)}
.legal{font-size:13px}
.prensa a,.contacto .nota a,.legal a{display:inline-block;padding:3px 0}
.redes{display:flex;gap:18px;align-items:center}
.redes a{display:block;color:var(--tinta);padding:4px;margin:-4px}
.redes a:hover{color:var(--azul)}
.redes svg{display:block;width:auto;height:calc(22px * var(--f));fill:currentColor}
.logos{display:flex;justify-content:space-between;gap:24px;align-items:center;flex-wrap:wrap;max-width:420px}
.logos{--go:52px}.logos img{width:auto}.logos .nau{height:calc(var(--go) * .706)}.logos .oma{height:calc(var(--go) * .66)}.logos .genuino{height:calc(var(--go) * .88)}

/* botones, opción C (elegida el 13 oct 2026): avísame es un bloque rojo plano;
   cuéntalo y press kit son enlaces editoriales, texto grande con subrayado grueso y flecha */
.boton-h,.boton-h:hover,.boton-h:active{border:0;border-radius:0;box-shadow:none;transform:none;transition:none}
.boton-h>span{border-radius:0;box-shadow:none;transition:background-color .15s,color .15s,background-size .15s}
form .boton-h>span{background:var(--rojo);color:var(--papel);padding:13px 22px}
form .boton-h:hover>span,form .boton-h:focus-visible>span{background:var(--tinta);color:var(--papel)}
.campo-h input{border:0;border-bottom:2px solid var(--tinta);border-radius:0;box-shadow:none;padding:12px 0;background:transparent}
#suscribir .campo-h input{padding-left:0;padding-right:0}
.campo-h input:focus{background:transparent;border-bottom-color:var(--azul);box-shadow:0 1px 0 var(--azul)}
.resena .boton-h>span,.pk-b .boton-h>span{display:inline-flex;align-items:baseline;gap:.4em;padding:4px 0 9px;font-size:20px;letter-spacing:-.02em;line-height:1.15;
  background:linear-gradient(currentColor,currentColor) left bottom / 100% 3px no-repeat!important}
.resena .boton-h>span{color:var(--azul)!important}.pk-b .boton-h>span{color:var(--tinta)!important}
.resena .boton-h>span::after,.pk-b .boton-h>span::after{content:"↗";font-weight:400;font-size:.85em}
.resena .boton-h:hover>span,.pk-b .boton-h:hover>span,.resena .boton-h:focus-visible>span,.pk-b .boton-h:focus-visible>span{background-size:100% 6px!important}
/* prensa: los cuatro enlaces siempre en una línea; la letra se ajusta al ancho disponible */
.prensa-b{container-type:inline-size}
.prensa{flex-wrap:nowrap;white-space:nowrap;gap:0 .9em;font-size:min(15px,3.95cqi)}
/* el campo del correo titila cuando llegan desde "avísame de las funciones" */
@keyframes llama{0%,100%{border-bottom-color:var(--tinta);box-shadow:none}50%{border-bottom-color:var(--rojo);box-shadow:0 2px 0 var(--rojo)}}
#suscribir.llama .campo-h input{animation:llama 1s ease-in-out 5}
#suscribir.llama .campo-h input::placeholder{color:var(--rojo)}
#suscribir .campo-h input{caret-color:var(--rojo)}
@media (max-width:820px){
  .cabecera{position:relative;padding:56px 16px 0}
  .cabecera h1{font-size:clamp(44px,13.4vw,110px);white-space:normal}
  .uno{position:relative;height:auto;min-height:calc(100svh - var(--cab,150px));padding:0 16px 20px;display:flex;flex-direction:column}
    .bajar{display:none}
  .cabecera h1 .firma{font-size:15px;margin-top:6px}
  /* el dibujo a todo lo ancho y los globos encima de cada personaje, como en el ordenador */
  .escena{position:relative;left:auto;top:auto;width:calc(100% + 32px);margin:0 -16px;font-size:clamp(10px,2.8vw,12px)}
  .uno{min-height:0;padding-top:var(--aire,40px);padding-bottom:12px}
  .globo-h .caja{padding:.55em .75em}
  .g1{--p:calc(100% - 22px);--cola:10px}
  .g2{--p:calc(100% - 27px);--cola:46px}
  .g3{--p:12px;--cola:84px}
  .g4{--p:12px;--cola:10px}
  .idioma{top:12px;right:16px}
  /* orden en el teléfono: qué es, cuándo se ve, qué dicen, quiénes son, avísame, los dos botones
     y al fondo logos, redes, correo y privacidad */
  .dos{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .a,.b,.c,.material,.suscribir,.resena,.pk-b{display:contents}
  .dos>*>*,.c>*>*,.suscribir>*,.resena>*,.pk-b>*{grid-column:1/-1}
  .a>div,.b>div,.funcion,.prensa-b,.suscribir>*,.resena>p,.pie{padding-left:16px;padding-right:16px}
  .a>div,.b>div{background:var(--azul)}
  .a>div{order:1;padding-top:44px;padding-bottom:44px}
  .funcion{order:2;padding-top:40px}
  .prensa-b{order:3;padding-top:32px;padding-bottom:44px}
  .b>div{order:4;padding-top:40px;padding-bottom:44px}
  .suscribir>*{order:5}
  .suscribir>h2{padding-top:40px}
  .suscribir>form{margin-top:12px}
  .resena>p{order:6;padding-top:32px;padding-bottom:12px;color:var(--tinta)}
  /* cuéntalo y press kit: mismo tamaño, uno al lado del otro */
  .resena>.boton-h,.pk-b>.boton-h{grid-column:auto;align-self:stretch;justify-self:stretch;display:flex}
  .resena>.boton-h{order:7;margin:0 12px 0 16px}
  .pk-b>.boton-h{order:8;margin:0 16px 0 12px}
  .resena>.boton-h>span,.pk-b>.boton-h>span{flex:1;display:flex;align-items:flex-end;justify-content:space-between;text-align:left;font-size:18px;padding:8px 0 10px;min-height:48px}
  .pie{order:9;margin-top:0;padding-top:48px;padding-bottom:40px;gap:24px}
  .pie .logos{order:1}.pie .contacto{order:2}
  /* pie en el teléfono: redes a la izquierda; correo arriba y privacidad abajo a la derecha, a la altura de los iconos */
  .contacto{display:grid;grid-template-columns:auto minmax(0,1fr);align-items:center;column-gap:12px;row-gap:0}
  .contacto .redes{grid-row:1/3;gap:18px}
  .contacto .nota{grid-column:2;justify-self:end;text-align:right;font-size:clamp(11.5px,3.4vw,14px);line-height:1.1}
  .pie .contacto .nota a{display:block;padding:3px 0}
  .logos{max-width:none;--go:54px}
  .prensa a,.legal a,.contacto .nota a{padding:9px 0}
  .redes{gap:22px}.redes a{padding:11px;margin:-11px}
  .laureles{display:grid;grid-template-columns:1fr 1fr;justify-items:center;align-items:center;gap:28px 16px;margin-top:26px}
  .laureles{--gl:min(104px,calc((100vw - 48px) / 3.3))}.laureles img{max-width:100%}
}
/* en ordenador la segunda pantalla encaja de un golpe bajo el título */
@media (min-width:821px){
  html{scroll-snap-type:y mandatory}.tope{position:absolute;top:0;left:0;width:1px;height:1px;scroll-snap-align:start}.dos{scroll-snap-align:start}
  /* mitad azul, mitad blanca; cada columna usa todo su ancho */
  .bloque>*{max-width:none}
  .a{padding-bottom:0}
  /* sinopsis y laureles comparten una sola medida: los laureles van de borde a borde del texto */
  .a>div{max-width:min(100%,34em);font-size:clamp(20px,1.6vw,30px)}
  .sinopsis{font-size:1em;line-height:1.3;letter-spacing:-.01em;text-wrap:pretty}
  .laureles{justify-content:space-between;margin-top:clamp(18px,3svh,34px)}
  .laureles img{object-fit:contain}
  /* reparto centrado en el espacio azul que queda; ¿ya la viste? abajo, a la altura de redes y correo */
  .b{justify-content:space-between}.b>div:first-child{margin-block:auto}
  /* reparto y equipo: la letra crece con la pantalla para que la línea más larga llegue al borde de los laureles */
  .equipo{grid-template-columns:auto minmax(0,1fr);font-size:clamp(15px,1.07vw,24px);gap:.3em 1.1em}
  /* ya la viste?, en blanco sobre azul */
  .resena{flex-direction:row;flex-wrap:wrap;align-items:baseline;gap:10px 16px;margin-top:0}.resena>p{flex:0 0 auto;margin:0}
  .izq .resena .boton-h>span{color:var(--papel)!important}
  .resena .boton-h:hover>span,.resena .boton-h:focus-visible>span{box-shadow:none!important}
  /* columna derecha: función, prensa y press kit, avísame, productoras, redes y correo, privacidad */
  .c{display:flex}
  .funcion{order:1}.material{order:2;display:flex;flex-direction:column;gap:14px}.suscribir{order:3}.pie{order:4;margin-top:auto}
  /* más aire entre función, prensa y avísame, para que el hueco no se junte todo sobre los logos;
     la próxima función, que es el dato que buscan, con letra de lectura */
  .c{gap:clamp(28px,5.5svh,64px)}
  .funcion p{font-size:clamp(16px,1.2vw,21px);line-height:1.35}
  /* press kit en la misma línea que las notas de prensa, alineado a la derecha; si no cabe, baja */
  .material{flex-direction:row;flex-wrap:wrap;align-items:last baseline;justify-content:space-between;gap:12px 24px}
  .prensa-b{flex:1 1 0;min-width:min(100%,330px)}.pk-b{align-self:last baseline;flex:0 0 auto}
  .pie{gap:18px}.pie .logos{order:1}.pie .contacto{order:2}
  .contacto{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:12px 22px}
  .contacto .legal{justify-self:end}
  .logos{max-width:none;justify-content:space-between;--go:clamp(60px,9.4svh,112px)}
  .laureles{--gl:clamp(64px,10.5svh,124px)}
  .prensa{font-size:min(16px,3.6cqi)}
}
/* pantallas de ordenador bajas: todo un poco más compacto para que la segunda pantalla quepa entera */
@media (min-width:821px) and (max-height:900px){
  .a>div{font-size:clamp(19px,1.5vw,26px)}
  .laureles{--gl:clamp(54px,8.5svh,84px)}
  .c{gap:clamp(20px,3.6svh,40px)}
  .equipo{font-size:clamp(15px,1.07vw,24px)}
  .boton-h>span{padding:10px 16px}
  .campo-h input{padding:9px 12px}
  .funcion p{font-size:clamp(15px,1.1vw,18px)}
  .c{padding-top:clamp(24px,4svh,64px)}
  .pie{gap:12px}
}
/* portátiles muy bajos (720-760 px de alto) */
@media (min-width:821px) and (max-height:760px){
  .a>div{font-size:clamp(18px,1.4vw,22px)}
  .c{gap:16px}
  .equipo{font-size:clamp(14px,1.05vw,18px);gap:.15em 1em}
  .laureles{--gl:56px}
  .bloque{gap:14px}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

# caja real de cada icono (lo que ocupa el dibujo dentro de su lienzo de 24) y su factor óptico
CAJA = {'instagram': ('0 0 24 24', '1.02', '1'), 'facebook': ('0 0.04 24 23.91', '.904', '24/23.91'),
        'tiktok': ('1.57 0 20.85 24', '1.104', '20.85/24'), 'x': ('0 1.15 24 21.69', '.96', '24/21.69')}

PICO = ('<svg class="pico" viewBox="0 0 16 100" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M1.5 0 L8 97 L14.5 0" fill="#fff" stroke="#1f2340" stroke-width="2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>')


def body(L, preview):
    """Cuerpo de la página. En la vista previa los textos llevan data-en para el botón de idioma."""
    def t(key_or_dict, tag='span', cls='', extra=''):
        d = TXT[key_or_dict] if isinstance(key_or_dict, str) else key_or_dict
        c = (' class="%s"' % cls) if cls else ''
        en = (' data-en="%s"' % d['en'].replace('"', '&quot;')) if preview else ''
        return '<%s%s%s%s>%s</%s>' % (tag, c, extra, en, d[L], tag)
    pre = '' if L == 'es' else '../'
    globos = ''
    for c, dest, txt, ev in GLOBOS:
        href = TR[L] if dest == 'trailer' else dest
        extra = (' data-href-en="%s"' % TR['en']) if (preview and dest == 'trailer') else ''
        globos += '<a class="globo-h %s" href="%s" data-umami-event="%s"%s><span class="caja">%s</span>%s</a>' % (c, href, ev, extra, t(txt, cls='dice'), PICO)
    if preview:
        idioma = '<button class="idioma" id="idioma" type="button" lang="en">English</button>'
    else:
        otro = '/en/' if L == 'es' else '/'
        idioma = '<a class="idioma" href="%s" hreflang="%s" lang="%s">%s</a>' % (otro, 'en' if L == 'es' else 'es', 'en' if L == 'es' else 'es', TXT['otro_idioma'][L])
    imagen = ('<picture><source srcset="%simg/casa-800.webp 800w, %simg/casa.webp 1600w" sizes="(max-width: 820px) 100vw, 62vw" type="image/webp"><img src="%simg/casa.jpg" width="1600" height="1277" fetchpriority="high" alt="%s"%s></picture>'
              % (pre, pre, pre, TXT['alt_casa'][L], (' data-alt-en="%s"' % TXT['alt_casa']['en']) if preview else ''))
    if preview:  # en el artifact no hay webp aparte: se usa el jpg
        imagen = '<img src="img/casa.jpg" width="2000" height="1596" fetchpriority="high" alt="%s" data-alt-en="%s">' % (TXT['alt_casa']['es'], TXT['alt_casa']['en'])
    TAM = {'mammoth': (200, 115), 'not': (200, 166), 'kyiv': (200, 95), 'elco': (200, 111)}
    laureles = ''.join('<img class="l-%s" src="%simg/laurel-%s-blanco.png" width="%d" height="%d" loading="lazy" alt="%s">' % (k, pre, k, TAM[k][0], TAM[k][1], alt[L]) for k, cls, alt in LAURELES)
    creditos = ''.join('<dt>%s</dt><dd>%s</dd>' % (t(r), n) for r, n in CREDITOS)
    prensa = ''.join('<a href="%s">%s</a>' % (u, m) for m, u in PRENSA)
    if preview:
        form = ('<form id="suscribir" data-umami-event="suscripcion">'
                '<label class="campo-h"><input id="correo" type="email" autocomplete="email" required placeholder="tu@correo.com" aria-label="correo"></label>'
                '<button class="boton-h" type="submit">%s</button></form>') % t('su_btn')
        presskit = '<a class="boton-h" href="#" id="presskit" data-umami-event="press-kit">%s</a>' % t('pk')
        privacidad = '<a href="#" id="privacidad">%s</a>' % t('privacidad')
    else:
        form = ('<form id="suscribir" action="https://buttondown.com/api/emails/embed-subscribe/%s" method="post" data-umami-event="suscripcion">'
                '<input type="hidden" name="tag" value="web-%s">'
                '<label class="campo-h"><input id="correo" name="email" type="email" autocomplete="email" required placeholder="%s" aria-label="%s"></label>'
                '<button class="boton-h" type="submit"><span>%s</span></button>%s</form>') % (
                BUTTONDOWN, L, 'tu@correo.com' if L == 'es' else 'you@email.com', 'correo' if L == 'es' else 'email', TXT['su_btn'][L],
                ('<div class="cf-turnstile" data-sitekey="%s" data-appearance="interaction-only" data-language="%s" style="flex-basis:100%%"></div>' % (TURNSTILE_SITEKEY, L)) if TURNSTILE_SITEKEY else '')
        presskit = '<a class="boton-h" href="/%s?v=2026-10-14" data-umami-event="press-kit"><span>%s</span></a>' % ('press-kit.pdf' if L == 'es' else 'press-kit-en.pdf', TXT['pk'][L])
        privacidad = '<a href="%s">%s</a>' % ('/privacidad/' if L == 'es' else '/en/privacy/', TXT['privacidad'][L])
    # en la vista previa los botones envuelven el texto en <span> igual que en el sitio
    if preview:
        form = form.replace('<button class="boton-h" type="submit">', '<button class="boton-h" type="submit"><span>').replace('</button></form>', '</span></button></form>')
        presskit = presskit.replace('id="presskit" data-umami-event="press-kit">', 'id="presskit" data-umami-event="press-kit"><span>').replace('</a>', '</span></a>', 1)
    lb_btn = '<a class="boton-h" href="%s" data-umami-event="letterboxd-resena" style="--fondo:var(--azul);--hover:var(--papel);--letra-h:var(--azul)"><span>%s</span></a>' % (LB, t('lb_btn'))
    titulo_h1 = t('titulo', 'span')
    h1 = '<h1>%s %s</h1>' % (titulo_h1, t('firma', 'span', 'firma'))
    return """
<main lang="%(L)s" id="pagina">
<div class="tope" aria-hidden="true"></div>
<header class="cabecera" id="cabecera">
  %(idioma)s
  %(h1)s
</header>
<section class="uno" aria-label="Los Batracios">
  <div class="escena" id="escena">
    %(imagen)s
    %(globos)s
  </div>
  <a class="bajar" href="#mas" aria-label="%(aria_bajar)s"><svg viewBox="0 0 22 14" aria-hidden="true"><path d="M2 2 L11 11.5 L20 2" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/></svg></a>
</section>

<div class="dos" id="mas">
  <section class="bloque izq a" aria-label="%(aria_peli)s">
    <div>%(h_sin)s%(sinopsis)s<div class="laureles">%(laureles)s</div></div>
  </section>
  <section class="bloque der c" aria-label="%(aria_seguir)s">
    <div class="funcion">%(h_fu)s<p>%(fu_fecha)s<b>Festival del Cine Venezolano</b>Margarita, Venezuela</p></div>
    <div class="suscribir" id="suscribir-bloque">
      %(h_su)s%(su_txt)s
      %(form)s
      <p class="nota" id="su-nota" data-confirmar="%(su_conf)s" role="status" hidden>%(su_nota)s</p>
    </div>
    <div class="material"><div class="prensa-b">%(h_pr)s<p class="prensa">%(prensa)s</p></div><div class="pk-b">%(presskit)s%(pk_nota)s</div></div>
    <div class="pie">
      <div class="contacto"><p class="redes">%(redes)s</p><p class="nota"><a href="mailto:%(mail)s">%(mail)s</a></p><p class="nota legal">%(privacidad)s</p></div>
      <div class="logos"><img class="nau" src="%(pre)simg/logo-nau-azul.png" width="185" height="104" loading="lazy" alt="Producciones NAU"><img class="oma" src="%(pre)simg/logo-oma-azul.png" width="240" height="85" loading="lazy" alt="Omni Media Arts"><img class="genuino" src="%(pre)simg/logo-genuino-azul.png" width="109" height="104" loading="lazy" alt="Genuino Films"></div>
    </div>
  </section>
  <section class="bloque izq b" aria-label="%(aria_equipo)s">
    <div>%(h_eq)s<dl class="equipo">%(creditos)s</dl></div>
    <div class="resena">%(lb_txt)s%(lb_btn)s</div>
  </section>
</div>
</main>
""" % dict(L=L, idioma=idioma, h1=h1, imagen=imagen, globos=globos, pre=pre,
           aria_peli={'es': 'La película', 'en': 'The film'}[L], aria_seguir={'es': 'Seguir la película', 'en': 'Follow the film'}[L],
           aria_equipo={'es': 'Equipo y prensa', 'en': 'Team and press'}[L],
           h_sin=t('h_sin', 'h2'), sinopsis=t('sinopsis', 'p', 'sinopsis'), laureles=laureles,
           h_fu=t('h_fu', 'h2'), fu_fecha=t('fu_fecha', 'span', '', ' style="display:block;color:var(--gris)"'),
           h_su=t('h_su', 'h2'), su_txt=t('su_txt', 'p'), form=form, aria_bajar={'es': 'bajar', 'en': 'scroll down'}[L], redes=''.join('<a href="%s" aria-label="%s"><svg viewBox="%s" style="--f:%s;aspect-ratio:%s" aria-hidden="true"><path d="%s"/></svg></a>' % (u, n, CAJA[k][0], CAJA[k][1], CAJA[k][2], ICONOS[k]) for k, u, n in [('instagram', IG, 'Instagram'), ('facebook', FB, 'Facebook'), ('tiktok', TT, 'TikTok'), ('x', XX, 'X')]),
           su_nota=t({'es': 'Esto es una maqueta. Todavía no guarda tu correo.', 'en': 'This is a mockup. It does not save your email yet.'}) if preview else {'es': 'Listo, ya estás en la lista.', 'en': 'Done, you are on the list.'}[L],
           su_conf={'es': 'Listo. Te mandamos un correo para confirmar.', 'en': 'Done. Check your inbox to confirm.'}[L],
           lb_txt=t('lb_txt', 'p'), lb_btn=lb_btn, mail=MAIL, tt=TT, xx=XX, privacidad=privacidad,
           h_eq=t('h_eq', 'h2'), creditos=creditos, h_pr=t('h_pr', 'h2'), prensa=prensa, presskit=presskit,
           pk_nota=('<p class="nota" id="pk-nota" style="color:var(--noche-etq)" hidden>%s</p>' % t({'es': 'En esta maqueta el press kit todavía no descarga.', 'en': 'In this mockup the press kit does not download yet.'})) if preview else '')


PREMIOS = {
  'es': ["Premio del Público a Mejor Largometraje Narrativo Internacional, Mammoth Lakes Film Festival 2025",
         "Mención Honorífica del Jurado en Largometraje Narrativo Internacional, Mammoth Lakes Film Festival 2025",
         "Mención Especial del Jurado Shooting Stars por Interpretación, Nòt Film Fest 2025"],
  'en': ["Audience Award, Best International Narrative Feature, Mammoth Lakes Film Festival 2025",
         "Jury Honorable Mention, International Narrative Feature, Mammoth Lakes Film Festival 2025",
         "Shooting Stars Special Jury Mention for Performance, Nòt Film Fest 2025"]}
SELECCIONES = {
  'es': ["Selección Oficial, Largometrajes Venezolanos en el Extranjero, Festival de Cine ELCO 2025",
         "Molodist Means Youth, Molodist Kyiv International Film Festival 2025",
         "Selección Oficial, VENEZCINE México 2025"],
  'en': ["Official Selection, Venezuelan Features Abroad, ELCO Film Festival 2025",
         "Molodist Means Youth, Molodist Kyiv International Film Festival 2025",
         "Official Selection, VENEZCINE México 2025"]}
CLAVES = {
  'es': "Los Batracios, The Batrachians, película venezolana, cine venezolano, cine independiente, comedia dramática, película de 2025, Diego Salomon, Sofía Ciffoni, Jósbel Lobo, Andreina Crepsac, Oscar Belloso, Mammoth Lakes Film Festival, Nòt Film Fest, Molodist, Festival de Cine ELCO, VENEZCINE México, Festival del Cine Venezolano, Margarita",
  'en': "The Batrachians, Los Batracios, Venezuelan film, Venezuelan cinema, independent film, comedy-drama, 2025 film, Diego Salomon, Sofía Ciffoni, Jósbel Lobo, Andreina Crepsac, Oscar Belloso, Mammoth Lakes Film Festival, Nòt Film Fest, Molodist, ELCO Film Festival, VENEZCINE México, Festival del Cine Venezolano, Margarita"}
TRAILER = {
  'es': {"id": "5gL_O2GYxDU", "name": "Los Batracios, tráiler oficial", "desc": "Tráiler oficial de Los Batracios (2025), una película de Diego Salomon.", "fecha": "2025-05-12T23:50:56-07:00"},
  'en': {"id": "iKg7xyXAgCs", "name": "The Batrachians (Los Batracios), official trailer with English subtitles", "desc": "Official trailer of The Batrachians (Los Batracios, 2025), a film by Diego Salomon, with English subtitles.", "fecha": "2025-05-12T23:52:35-07:00"}}


def jsonld(L):
    pid = DOM + '/#pelicula'
    tr = TRAILER[L]
    peli = {
      "@type": "Movie", "@id": pid,
      "name": "Los Batracios", "alternateName": "The Batrachians",
      "url": DOM + ('/' if L == 'es' else '/en/'),
      "image": DOM + '/img/compartir-%s.jpg' % L,
      "description": TXT['sinopsis'][L],
      "genre": ["Comedia", "Drama"] if L == 'es' else ["Comedy", "Drama"],
      "keywords": CLAVES[L],
      "inLanguage": "es", "subtitleLanguage": "en", "duration": "PT77M",
      "datePublished": "2025-05-24",
      "countryOfOrigin": [{"@type": "Country", "name": "España" if L == 'es' else "Spain"}, {"@type": "Country", "name": "Venezuela"}],
      "director": {"@type": "Person", "name": "Diego Salomon", "sameAs": ["https://www.imdb.com/name/nm15935024/"]},
      "author": {"@type": "Person", "name": "Diego Salomon"},
      "actor": [{"@type": "Person", "name": n} for n in ["Sofía Ciffoni", "Jósbel Lobo", "Andreina Crepsac", "Oscar Belloso"]],
      "producer": [{"@type": "Person", "name": n} for n in ["Samuel Rotter", "Carolina Perelman", "José Daniel Bort", "Rodolfo Cova"]],
      "musicBy": {"@type": "Person", "name": "Pedro Fraguela"},
      "productionCompany": [{"@type": "Organization", "name": n} for n in ["Producciones NAU", "Omni Media Arts", "Genuino Films"]],
      "award": PREMIOS[L] + SELECCIONES[L],
      "trailer": {"@type": "VideoObject", "name": tr['name'], "description": tr['desc'],
                  "thumbnailUrl": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % tr['id'], "uploadDate": tr['fecha'], "duration": "PT2M14S",
                  "embedUrl": "https://www.youtube.com/embed/%s" % tr['id'], "url": "https://www.youtube.com/watch?v=%s" % tr['id'], "inLanguage": "es"},
      "subjectOf": {"@type": "DigitalDocument", "name": "Press kit", "url": DOM + ('/press-kit.pdf' if L == 'es' else '/press-kit-en.pdf'), "encodingFormat": "application/pdf", "inLanguage": L},
      "sameAs": ["https://www.wikidata.org/wiki/Q141681370", "https://www.imdb.com/title/tt31797714/", "https://www.themoviedb.org/movie/1433125", LB,
                 "https://www.filmaffinity.com/es/film432719.html", "https://www.molodist.com/films-eng-2025/the-batrachians", IG, FB, TT, XX],
    }
    funcion = {
      "@type": "ScreeningEvent",
      "name": ("Los Batracios en el Festival del Cine Venezolano" if L == 'es' else "The Batrachians at Festival del Cine Venezolano"),
      "startDate": "2026-11-22", "endDate": "2026-11-27",
      "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "location": {"@type": "Place", "name": "Festival del Cine Venezolano",
                   "address": {"@type": "PostalAddress", "addressLocality": "Isla de Margarita", "addressRegion": "Nueva Esparta", "addressCountry": "VE"}},
      "workPresented": {"@id": pid}, "inLanguage": "es", "subtitleLanguage": "en",
      "organizer": {"@type": "Organization", "name": "Festival del Cine Venezolano"},
    }
    web = {"@type": "WebSite", "@id": DOM + '/#web', "name": "Los Batracios", "alternateName": "The Batrachians",
           "url": DOM + '/', "inLanguage": L, "about": {"@id": pid}}
    return '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": [peli, funcion, web]}, ensure_ascii=False)


def head(L, titulo, desc, ruta_es, ruta_en, og_img, robots_extra='', og_type='video.movie', enlaces=True):
    url = DOM + (ruta_es if L == 'es' else ruta_en)
    return """<!doctype html>
<html lang="%(L)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
%(enlaces)s<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="Los Batracios">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(dom)s/img/%(og)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%(titulo)s">
<meta property="og:locale" content="%(loc)s">
<meta property="og:locale:alternate" content="%(loc2)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@batraciospeli">
<link rel="icon" href="/img/icono-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/img/icono-180.png">
<meta name="theme-color" content="#ffffff">
%(robots)s<link rel="preload" href="/fonts/Aeonik-Bold.otf" as="font" type="font/otf" crossorigin>
<style>
@font-face{font-family:'Aeonik';font-weight:400;font-style:normal;font-display:swap;src:url(/fonts/AeonikRegular.otf) format('opentype')}
@font-face{font-family:'Aeonik';font-weight:700;font-style:normal;font-display:swap;src:url(/fonts/Aeonik-Bold.otf) format('opentype')}
""" % dict(L=L, titulo=titulo, desc=desc, url=url, dom=DOM, ruta_es=ruta_es, ruta_en=ruta_en, og=og_img,
           loc='es_ES' if L == 'es' else 'en_US', loc2='en_US' if L == 'es' else 'es_ES', robots=robots_extra, og_type=og_type,
           enlaces=('<link rel="canonical" href="%s">\n<link rel="alternate" hreflang="es" href="%s%s">\n<link rel="alternate" hreflang="en" href="%s%s">\n<link rel="alternate" hreflang="x-default" href="%s%s">\n'
                    % (url, DOM, ruta_es, DOM, ruta_en, DOM, ruta_es)) if enlaces else '')

UMAMI = '<script defer src="https://cloud.umami.is/script.js" data-website-id="%s" data-domains="losbatracios.com,www.losbatracios.com"></script>\n' % UMAMI_ID


def pagina_sitio(L):
    h = head(L, TXT['title_tag'][L], TXT['meta'][L], '/', '/en/', 'compartir-%s.jpg' % L)
    envio = '<script>' + ENVIO + '</script>'
    ts = '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>\n' if TURNSTILE_SITEKEY else ''
    return h + CSS + '</style>\n' + jsonld(L) + '\n' + UMAMI + ts + '</head>\n<body>\n' + body(L, False) + envio + CONVERSA + '\n</body>\n</html>\n'


ENVIO = """
/* Suscripción. Primero la web (sin doble confirmación, vía la API de Buttondown).
   Si la web todavía no tiene la clave, se usa el formulario normal de Buttondown, que pide confirmar. */
(function(){
  var f=document.getElementById('suscribir'), nota=document.getElementById('su-nota');
  function listo(confirmar){ f.hidden=true; if(confirmar) nota.textContent=nota.getAttribute('data-confirmar'); nota.hidden=false; }
  f.addEventListener('submit',function(e){
    e.preventDefault(); var datos=new FormData(f);
    fetch('/api/suscribir',{method:'POST',body:datos}).then(function(r){
      if(r.ok) return listo(false);
      return fetch(f.action,{method:'POST',body:new FormData(f),mode:'no-cors'}).then(function(){ listo(true); });
    }).catch(function(){ fetch(f.action,{method:'POST',body:new FormData(f),mode:'no-cors'}).then(function(){ listo(true); }); });
  });
  /* "avísame de las funciones" lleva al formulario y el campo titila para que se note */
  function llamar(){ var i=document.getElementById('correo'); f.classList.remove('llama'); void f.offsetWidth; f.classList.add('llama'); try{ i.focus({preventScroll:true}); }catch(x){ i.focus(); } }
  document.addEventListener('click',function(e){
    var a=e.target.closest && e.target.closest('a[href="#suscribir"]'); if(!a) return;
    e.preventDefault();
    var ancho=window.matchMedia('(min-width: 821px)').matches;
    if(ancho) scrollTo({top:document.documentElement.scrollHeight,behavior:'smooth'});
    else f.scrollIntoView({behavior:'smooth',block:'center'});
    setTimeout(llamar, 700);
  });
  if(location.hash==='#suscribir') setTimeout(llamar, 400);
  /* laureles a la medida de la sinopsis: de su borde izquierdo al final de su línea más larga (solo en ordenador) */
  function medida(){
    var s=document.querySelector('.sinopsis'), l=document.querySelector('.laureles'); if(!s||!l) return;
    if(!window.matchMedia('(min-width: 821px)').matches){ l.style.maxWidth=''; return; }
    var r=document.createRange(); r.selectNodeContents(s); var m=0, x=s.getBoundingClientRect().left;
    [].forEach.call(r.getClientRects(),function(c){ if(c.right>m) m=c.right; });
    if(m>x) l.style.maxWidth=Math.ceil(m-x)+'px';
  }
  medida(); addEventListener('resize',medida); if(document.fonts&&document.fonts.ready) document.fonts.ready.then(medida);
})();
"""

CONVERSA = """<script>
/* Portada. Mientras el dibujo se materializa (6 s, como en Familiar Touch) cada personaje
   dice su frase y se calla. Cuando el dibujo está nítido quedan los cuatro globos a la vista.
   Con movimiento reducido todo aparece de una vez. */
(function(){
  var cab=document.getElementById('cabecera'), dos=document.getElementById('mas'), pend=false;
  function medir(){ document.documentElement.style.setProperty('--cab',cab.offsetHeight+'px'); }
  function fondo(){ pend=false; cab.classList.toggle('fondo', dos.getBoundingClientRect().top <= cab.offsetHeight+24); }
  function pedir(){ if(!pend){ pend=true; requestAnimationFrame(fondo); } }
  medir(); fondo();
  addEventListener('resize',function(){ medir(); fondo(); });
  addEventListener('scroll',fondo,{passive:true}); addEventListener('wheel',pedir,{passive:true}); addEventListener('touchmove',pedir,{passive:true});

  /* en ordenador, la rueda o el trackpad pasan de una pantalla a la otra de un solo golpe */
  var ancho=window.matchMedia('(min-width: 821px)'), quieto=window.matchMedia('(prefers-reduced-motion: reduce)'), hasta=0;
  addEventListener('wheel',function(e){
    if(!ancho.matches || e.ctrlKey || Math.abs(e.deltaY)<Math.abs(e.deltaX)) return;
    var max=document.documentElement.scrollHeight-innerHeight, y=scrollY, t=Date.now();
    if(max<=0) return;
    if(e.deltaY>0 && y<max-2){ e.preventDefault(); if(t>hasta){ hasta=t+900; scrollTo({top:max,behavior:quieto.matches?'auto':'smooth'}); } }
    else if(e.deltaY<0 && y>2){ e.preventDefault(); if(t>hasta){ hasta=t+900; scrollTo({top:0,behavior:quieto.matches?'auto':'smooth'}); } }
  },{passive:false});

  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var esc=document.getElementById('escena'), gs={};
  [].forEach.call(esc.querySelectorAll('.globo-h'),function(g){ gs[g.classList[1]]=g; });
  function ver(id,si){ gs[id].classList.toggle('ve',si); }
  esc.classList.add('vivo');
  [['g1',2200],['g3',3000],['g4',3700],['g2',4400]].forEach(function(x){
    setTimeout(function(){ ver(x[0],true); },x[1]);
    setTimeout(function(){ ver(x[0],false); },x[1]+1000);
  });
  ['g1','g2','g3','g4'].forEach(function(id,n){ setTimeout(function(){ ver(id,true); },5600+n*140); });
  setTimeout(function(){ esc.classList.remove('vivo'); esc.classList.add('flota'); },6600);
})();
</script>
"""

PRIV = {
 'es': {
  'titulo': 'Privacidad, Los Batracios',
  'h1': 'privacidad',
  'cuerpo': """
<p>Esta web es de la película <i>Los Batracios</i>. Aquí explicamos qué datos se recogen y para qué. Última actualización: 13 de octubre de 2026.</p>
<h2>Responsable</h2>
<p>Diego Salomon. Contacto: <a href="mailto:losbatraciospeli@gmail.com">losbatraciospeli@gmail.com</a>.</p>
<h2>Estadísticas de visitas</h2>
<p>Medimos cuánta gente visita la web con Umami, una herramienta que no usa cookies y no guarda datos que te identifiquen. Solo vemos cifras de conjunto: país y ciudad aproximada, desde qué página llegas, tipo de dispositivo, navegador, idioma y en qué botones se hace clic. Lo hacemos para saber qué funciona al dar a conocer la película (interés legítimo). Los servidores están en la Unión Europea y estos datos se borran como máximo a los 25 meses.</p>
<h2>Lista de correo</h2>
<p>Si nos dejas tu correo, lo usamos solo para contarte novedades de la película, como funciones y estrenos. La base legal es tu consentimiento. La lista la gestiona Buttondown, que puede guardar los datos fuera de la Unión Europea con las garantías que exige la ley. Guardamos tu correo hasta que te des de baja. Cada correo trae un enlace para hacerlo. Para frenar a los bots, el formulario usa Cloudflare Turnstile, que revisa datos técnicos de la conexión (como la IP y el navegador) solo para eso y no usa cookies publicitarias. En los correos contamos los clics en los enlaces, por ejemplo a Letterboxd o a una función, para saber qué interesa. No medimos si abres el correo.</p>
<h2>Enlaces a otras webs</h2>
<p>Los enlaces a YouTube, Letterboxd, Instagram, Facebook, TikTok y X te llevan a esas webs, que tienen sus propias políticas de privacidad.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir acceso, corrección o borrado de tus datos, oponerte a su uso, limitarlo o pedir una copia, escribiendo a <a href="mailto:losbatraciospeli@gmail.com">losbatraciospeli@gmail.com</a>. Si crees que no los tratamos bien, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es">aepd.es</a>).</p>
""", 'volver': 'volver a la película', 'home': '/'},
 'en': {
  'titulo': 'Privacy, The Batrachians',
  'h1': 'privacy',
  'cuerpo': """
<p>This is the website of the film <i>Los Batracios</i> (<i>The Batrachians</i>). Here we explain what data we collect and why. Last updated: October 13, 2026.</p>
<h2>Controller</h2>
<p>Diego Salomon. Contact: <a href="mailto:losbatraciospeli@gmail.com">losbatraciospeli@gmail.com</a>.</p>
<h2>Visit statistics</h2>
<p>We count visits with Umami, a tool that uses no cookies and stores no data that identifies you. We only see totals: approximate country and city, the page you came from, device type, browser, language and which buttons get clicked. We do this to learn what works in promoting the film (legitimate interest). The servers are in the European Union and this data is deleted after 25 months at most.</p>
<h2>Mailing list</h2>
<p>If you leave us your email, we use it only to send you news about the film, such as screenings and releases. The legal basis is your consent. The list is managed by Buttondown, which may store data outside the European Union with the safeguards the law requires. We keep your email until you unsubscribe. Every email has a link to do so. To stop bots, the form uses Cloudflare Turnstile, which checks technical connection data (such as IP address and browser) only for that purpose and uses no advertising cookies. In our emails we count clicks on links, for example to Letterboxd or to a screening, to learn what people care about. We do not track whether you open an email.</p>
<h2>Links to other websites</h2>
<p>Links to YouTube, Letterboxd, Instagram, Facebook, TikTok and X take you to those websites, which have their own privacy policies.</p>
<h2>Your rights</h2>
<p>You can ask to access, correct or delete your data, object to its use, restrict it or get a copy by writing to <a href="mailto:losbatraciospeli@gmail.com">losbatraciospeli@gmail.com</a>. If you think we handle it badly, you can complain to the Spanish Data Protection Agency (<a href="https://www.aepd.es">aepd.es</a>).</p>
""", 'volver': 'back to the film', 'home': '/en/'},
}
PRIV_CSS = """
:root{--papel:#ffffff;--tinta:#1f2340;--azul:#263e99;--rojo:#b12025;--gris:#5e6385;--sans:'Aeonik','Helvetica Neue',Arial,sans-serif;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);font-family:var(--sans);font-size:17px;line-height:1.55;padding-inline:24px}
main{max-width:640px;margin:0 auto;padding-block:56px 72px;display:flex;flex-direction:column;gap:14px}
h1{font-size:clamp(44px,8vw,80px);line-height:.9;letter-spacing:-.04em;color:var(--rojo);margin:0 0 10px}
h2{font-size:15px;color:var(--rojo);margin:18px 0 0;text-transform:lowercase}
p{margin:0}
a{color:var(--azul);text-underline-offset:3px}
.volver{font-size:15px;color:var(--gris)}
"""


PRIV_DESC = {'es': 'Qué datos recoge la web de Los Batracios y para qué: visitas sin cookies con Umami y la lista de correo en Buttondown.',
             'en': 'What data the Los Batracios website collects and why: cookie-free visit counts with Umami and the mailing list on Buttondown.'}


def pagina_privacidad(L):
    P = PRIV[L]
    h = head(L, P['titulo'], PRIV_DESC[L], '/privacidad/', '/en/privacy/', 'compartir-%s.jpg' % L, og_type='website')
    return (h + PRIV_CSS + '</style>\n' + UMAMI + '</head>\n<body>\n<main>\n<a class="volver" href="%s">%s</a>\n<h1>%s</h1>\n%s\n</main>\n</body>\n</html>\n'
            % (P['home'], P['volver'], P['h1'], P['cuerpo']))


def pagina_404():
    h = head('es', 'Página no encontrada, Los Batracios', 'Esta página no existe.', '/', '/en/', 'compartir-es.jpg', '<meta name="robots" content="noindex">\n', og_type='website', enlaces=False)
    return (h + PRIV_CSS + '</style>\n</head>\n<body>\n<main>\n<h1>aquí no hay nadie</h1>\n'
            '<p>Esta página no existe. <a href="/">Volver a la película</a>. <span lang="en">This page does not exist. <a href="/en/">Back to the film</a>.</span></p>\n</main>\n</body>\n</html>\n')


WORKER = r"""// Los Batracios: sirve la web, recibe las suscripciones y manda la bienvenida.
// Con la variable BUTTONDOWN_API_KEY puesta en Cloudflare, el suscriptor entra directo (sin doble confirmación).
const CORTOS = {
  '/ig': '/?utm_source=instagram&utm_medium=bio', '/ig-historias': '/?utm_source=instagram&utm_medium=historias',
  '/tt': '/?utm_source=tiktok&utm_medium=bio', '/x': '/?utm_source=x&utm_medium=bio', '/fb': '/?utm_source=facebook&utm_medium=pagina',
  '/yt': '/?utm_source=youtube&utm_medium=descripcion', '/pk': '/?utm_source=presskit&utm_medium=pdf',
  '/prensa': '/?utm_source=prensa&utm_medium=email', '/boletin': '/?utm_source=boletin&utm_medium=email',
  '/qr': '/?utm_source=qr&utm_medium=afiche', '/wa': '/?utm_source=whatsapp&utm_medium=mensaje',
  '/resena': 'https://letterboxd.com/film/the-batrachians/'
};
const BD = 'https://api.buttondown.com/v1';
const GIF = 'https://losbatracios.com/img/besitos.gif?v=2';  // ?v=2: Gmail guarda en caché la imagen por URL
const LB = 'https://letterboxd.com/film/the-batrachians/';
const BIENVENIDA = {
  es: { subject: 'bienvenuti a los batracios', body:
    'hola!\n\ngracias por sumarte. te escribiremos cuando haya una función o algo que valga la pena contar.\n\n' +
    '![Lorena le da besitos a Mochi](' + GIF + ')\n\n' +
    'mientras tanto, agréganos en [letterboxd](' + LB + ') para apoyar la causa.\n\n' +
    'más besos,  \nel equipo de los batracios' },
  en: { subject: 'bienvenuti to the batrachians', body:
    'hi!\n\nthanks for joining. we will write when there is a screening or something worth telling.\n\n' +
    '![Lorena gives Mochi a lot of kisses](' + GIF + ')\n\n' +
    'in the meantime, add us on [letterboxd](' + LB + ') to support the cause.\n\n' +
    'more kisses,  \nthe batrachians team' }
};
// correos de bienvenida ya creados en Buttondown (importados, fuera del archivo). Si se cambia el texto, borrar estos ids y el correo viejo.
const IDS = { es: 'em_63smnjrfyy871sx51jp94qrq19', en: 'em_1fkc6a881t8mfannyy54877s06' };
async function bienvenida(env, email, lang) {
  const h = { 'Authorization': 'Token ' + env.BUTTONDOWN_API_KEY, 'Content-Type': 'application/json' };
  const m = BIENVENIDA[lang];
  let id = IDS[lang];
  if (!id) {
    const l = await fetch(BD + '/emails?status=imported', { headers: h });
    if (l.ok) { const e = ((await l.json()).results || []).find(x => x.subject === m.subject && String(x.body || '').includes(GIF)); if (e) id = e.id; }
  }
  if (!id) {
    const c = await fetch(BD + '/emails', { method: 'POST', headers: h,
      body: JSON.stringify({ subject: m.subject, body: m.body, status: 'imported', archival_mode: 'disabled' }) });
    if (!c.ok) { console.log('bienvenida: crear', c.status, await c.text()); return; }
    id = (await c.json()).id;
  }
  IDS[lang] = id;
  const s = await fetch(BD + '/subscribers/' + encodeURIComponent(email) + '/emails/' + id, { method: 'POST', headers: h });
  if (!s.ok) console.log('bienvenida: enviar', s.status, await s.text());
}
// Correo válido sin expresiones que se atasquen: primero el largo, después una revisión lineal.
function correoValido(e) {
  if (e.length < 6 || e.length > 200 || /\s/.test(e)) return false;
  const at = e.indexOf('@');
  if (at < 1 || at !== e.lastIndexOf('@')) return false;
  const dom = e.slice(at + 1), punto = dom.lastIndexOf('.');
  return punto > 0 && dom.length - punto > 2 && !dom.startsWith('.') && !dom.includes('..');
}
// Límite: 10 suscripciones por hora desde una misma conexión (contado por centro de datos de Cloudflare).
async function demasiadas(ip) {
  if (!ip) return false;
  try {
    const clave = new Request('https://limite.losbatracios.com/' + encodeURIComponent(ip) + '/' + Math.floor(Date.now() / 3600000));
    const prev = await caches.default.match(clave);
    const n = prev ? Number(await prev.text()) || 0 : 0;
    if (n >= 10) return true;
    await caches.default.put(clave, new Response(String(n + 1), { headers: { 'Cache-Control': 'max-age=3600' } }));
  } catch (e) {}
  return false;
}
// Turnstile (verificación invisible de Cloudflare). Solo se exige si TURNSTILE_SECRET_KEY está puesta.
async function humano(env, token, ip) {
  if (!token) return false;
  const d = new FormData(); d.append('secret', env.TURNSTILE_SECRET_KEY); d.append('response', token); if (ip) d.append('remoteip', ip);
  try { const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: d }); return !!(await r.json()).success; }
  catch (e) { return true; }
}
export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    const corto = CORTOS[u.pathname.replace(/\/$/, '')];
    if (corto) return Response.redirect(corto.startsWith('http') ? corto : u.origin + corto, 302);
    if (u.pathname === '/api/suscribir') {
      if (req.method !== 'POST') return new Response('', { status: 405 });
      if (!env.BUTTONDOWN_API_KEY) return new Response('sin clave', { status: 503 });
      if (Number(req.headers.get('Content-Length') || 0) > 4000) return new Response('grande', { status: 413 });
      const ip = req.headers.get('CF-Connecting-IP') || '';
      if (await demasiadas(ip)) return new Response('espera', { status: 429 });
      const f = await req.formData();
      const email = String(f.get('email') || '').trim().toLowerCase();
      const tag = /^web-(es|en)$/.test(String(f.get('tag'))) ? String(f.get('tag')) : 'web';
      if (!correoValido(email)) return new Response('correo', { status: 400 });
      if (env.TURNSTILE_SECRET_KEY && !(await humano(env, String(f.get('cf-turnstile-response') || ''), ip))) return new Response('verificacion', { status: 403 });
      // ip_address: la IP real de quien se suscribe, para que el firewall de Buttondown no confunda a todos con la IP de Cloudflare
      const alta = (conTag) => fetch(BD + '/subscribers', {
        method: 'POST',
        headers: { 'Authorization': 'Token ' + env.BUTTONDOWN_API_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.assign({ email_address: email, type: 'regular', ip_address: req.headers.get('CF-Connecting-IP') || undefined,
          referrer_url: req.headers.get('Referer') || '' }, conTag ? { tags: [tag] } : {}))
      });
      let r = await alta(true);
      if (r.status === 403) r = await alta(false);  // plan gratis: si la etiqueta no existe, entra sin etiqueta
      if (r.status === 201) { ctx.waitUntil(bienvenida(env, email, tag === 'web-en' ? 'en' : 'es')); return new Response('ok', { status: 200 }); }
      if (r.ok) return new Response('ok', { status: 200 });
      const t = await r.text();
      if (r.status === 409 || /already|exists|ya existe/i.test(t)) return new Response('ok', { status: 200 });
      console.log('suscribir', r.status, t);
      return new Response('error', { status: 502 });  // texto generico: el detalle queda solo en el log
    }
    const res = await env.ASSETS.fetch(req);
    if (u.hostname.endsWith('.pages.dev')) {  // la copia de pruebas no sale en Google
      const r = new Response(res.body, res);
      r.headers.set('X-Robots-Tag', 'noindex');
      return r;
    }
    return res;
  }
};
"""


LLMS = """# Los Batracios (The Batrachians)

> Los Batracios (English title: The Batrachians) is a 2025 feature film from Spain and Venezuela, written and directed by Diego Salomon. A comedy-drama, 77 minutes, in Spanish with English subtitles. Starring Sofía Ciffoni, Jósbel Lobo, Andreina Crepsac and Oscar Belloso.

Synopsis: An evening among friends turns into an emotional battlefield when a couple's tension leads everyone to question the strength of their bonds.

## Awards
- Audience Award, Best International Narrative Feature, Mammoth Lakes Film Festival 2025 (world premiere, 24 May 2025)
- Jury Honorable Mention, International Narrative Feature, Mammoth Lakes Film Festival 2025
- Shooting Stars Special Jury Mention for Performance, Nòt Film Fest 2025

## Festival selections
- Official Selection, Venezuelan Features Abroad, ELCO Film Festival 2025
- Molodist Means Youth, Molodist Kyiv International Film Festival 2025
- Official Selection, VENEZCINE México 2025

## Where to watch
- Festival screenings for now. Next: Festival del Cine Venezolano, Isla de Margarita, Venezuela, 22 to 27 November 2026.
- Not on streaming platforms yet. Sign up at https://losbatracios.com to hear about screenings and releases.

## Credits
- Written and directed by Diego Salomon
- Produced by Samuel Rotter, Carolina Perelman, José Daniel Bort and Rodolfo Cova
- Cinematography: Jordan Tetewsky. Editing: Mayra Morán. Sound: Isabella Salvo and Daniel Rincón García. Music: Pedro Fraguela
- Production companies: Producciones NAU, Omni Media Arts, Genuino Films

## Official pages
- [Home, Spanish](https://losbatracios.com/)
- [Home, English](https://losbatracios.com/en/)
- [Press kit, Spanish (PDF)](https://losbatracios.com/press-kit.pdf)
- [Press kit, English (PDF)](https://losbatracios.com/press-kit-en.pdf)

## Elsewhere
- [IMDb](https://www.imdb.com/title/tt31797714/)
- [Letterboxd](https://letterboxd.com/film/the-batrachians/)
- [TMDb](https://www.themoviedb.org/movie/1433125)
- [Wikidata](https://www.wikidata.org/wiki/Q141681370)
- [FilmAffinity](https://www.filmaffinity.com/es/film432719.html)
- [Trailer, Spanish](https://www.youtube.com/watch?v=5gL_O2GYxDU)
- [Trailer, English subtitles](https://www.youtube.com/watch?v=iKg7xyXAgCs)

## Contact
- losbatraciospeli@gmail.com
"""


def construir_sitio():
    S = R / 'sitio'
    if S.exists(): shutil.rmtree(S)
    (S / 'img').mkdir(parents=True); (S / 'fonts').mkdir(); (S / 'en' / 'privacy').mkdir(parents=True); (S / 'privacidad').mkdir()
    (S / 'index.html').write_text(pagina_sitio('es'), encoding='utf-8')
    (S / 'en' / 'index.html').write_text(pagina_sitio('en'), encoding='utf-8')
    (S / 'privacidad' / 'index.html').write_text(pagina_privacidad('es'), encoding='utf-8')
    (S / 'en' / 'privacy' / 'index.html').write_text(pagina_privacidad('en'), encoding='utf-8')
    _copia(R / 'src/extra/casa-1600.jpg', S / 'img/casa.jpg'); _copia(R / 'src/extra/casa.webp', S / 'img/casa.webp'); _copia(R / 'src/extra/casa-800.webp', S / 'img/casa-800.webp')
    for f in ['compartir-es.jpg', 'compartir-en.jpg', 'icono-32.png', 'icono-180.png']: _copia(R / 'src/extra' / f, S / 'img' / f)
    for k in ['mammoth', 'not', 'kyiv', 'elco']: _copia(R / 'src/img' / ('laurel-%s-blanco.png' % k), S / 'img')
    for k in ['nau', 'oma', 'genuino']: _copia(R / 'src/img' / ('logo-%s-azul.png' % k), S / 'img')
    for f in ['AeonikRegular.otf', 'Aeonik-Bold.otf']: _copia(R / 'fonts' / f, S / 'fonts' / f)
    _copia(R / 'src/img/besitos.gif', S / 'img/besitos.gif')  # GIF del correo de bienvenida
    # laureles desde los originales en alta de cada festival (src/hd), en blanco, hasta 900 px de ancho
    for k in ['mammoth', 'not', 'kyiv', 'elco']:
        im = Image.open(R / 'src/hd' / ('%s-blanco.png' % k)).convert('RGBA'); ancho = min(600, im.width)
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
        im.quantize(colors=64, method=Image.FASTOCTREE, dither=Image.NONE).save(S / 'img' / ('laurel-%s-blanco.png' % k), optimize=True)
    # logos de las productoras en la versión de 300 px de alto (nítidos en pantallas de 3x)
    for k in ['nau', 'oma', 'genuino']:
        Image.open(R / 'src/img' / ('logo-%s-azul.png' % k)).convert('RGBA').quantize(colors=64, method=Image.FASTOCTREE, dither=Image.NONE).save(S / 'img' / ('logo-%s-azul.png' % k), optimize=True)
    # press kits del 14 oct (versión liviana, sin screener ni clave, con enlace a fotogramas)
    _copia(R / 'src/pk/press-kit-es.pdf', S / 'press-kit.pdf'); _copia(R / 'src/pk/press-kit-en.pdf', S / 'press-kit-en.pdf')
    (S / 'llms.txt').write_text(LLMS, encoding='utf-8')
    (S / '404.html').write_text(pagina_404(), encoding='utf-8')
    (S / '_redirects').write_text("""# Enlaces cortos por canal (para saber de dónde llega la gente)
/ig            /?utm_source=instagram&utm_medium=bio          302
/ig-historias  /?utm_source=instagram&utm_medium=historias    302
/tt            /?utm_source=tiktok&utm_medium=bio             302
/x             /?utm_source=x&utm_medium=bio                  302
/fb            /?utm_source=facebook&utm_medium=pagina        302
/yt            /?utm_source=youtube&utm_medium=descripcion    302
/pk            /?utm_source=presskit&utm_medium=pdf           302
/prensa        /?utm_source=prensa&utm_medium=email           302
/boletin       /?utm_source=boletin&utm_medium=email          302
/qr            /?utm_source=qr&utm_medium=afiche              302
/wa            /?utm_source=whatsapp&utm_medium=mensaje       302
# Quien sale de una función va directo a Letterboxd a reseñar
/resena        https://letterboxd.com/film/the-batrachians/   302
""")
    (S / '_worker.js').write_text(WORKER)
    (S / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % DOM)
    urls = [('/', '/en/'), ('/privacidad/', '/en/privacy/')]
    items = ''
    for es, en in urls:
        for loc in (es, en):
            items += ('  <url><loc>%s%s</loc><lastmod>%s</lastmod>\n    <xhtml:link rel="alternate" hreflang="es" href="%s%s"/>\n'
                      '    <xhtml:link rel="alternate" hreflang="en" href="%s%s"/>\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>\n  </url>\n') % (DOM, loc, HOY, DOM, es, DOM, en, DOM, es)
    (S / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + items + '</urlset>\n')
    return S


def construir_vista():
    V = R / 'build' / 'v5'
    if V.exists(): shutil.rmtree(V)
    (V / 'img').mkdir(parents=True)
    fonts = ''.join("@font-face{font-family:'Aeonik';font-weight:%d;font-style:normal;font-display:swap;src:url(data:font/otf;base64,%s) format('opentype')}\n"
                    % (w, base64.b64encode(_lee(R / f)).decode()) for w, f in [(400, 'fonts/AeonikRegular.otf'), (700, 'fonts/Aeonik-Bold.otf')])
    js = """
<script>
(function(){
  var en=false, btn=document.getElementById('idioma'), main=document.getElementById('pagina'), esc=document.getElementById('escena');
  document.querySelectorAll('[data-en]').forEach(function(e){ e.setAttribute('data-es',e.innerHTML); });
  var tr=document.querySelector('.g1');
  function poner(v){
    en=v;
    document.querySelectorAll('[data-en]').forEach(function(e){ e.innerHTML=e.getAttribute(en?'data-en':'data-es'); });
    var im=esc.querySelector('img'); if(!im.dataset.altEs) im.dataset.altEs=im.alt; im.alt=en?im.dataset.altEn:im.dataset.altEs;
    tr.href=en?tr.getAttribute('data-href-en'):'%s';
    main.lang=en?'en':'es'; btn.textContent=en?'Español':'English'; btn.lang=en?'es':'en';
    try{ localStorage.setItem('idioma',en?'en':'es'); }catch(e){}
  }
  btn.addEventListener('click',function(){ poner(!en); });
  try{ if(localStorage.getItem('idioma')==='en') poner(true); }catch(e){}
  document.getElementById('suscribir').addEventListener('submit',function(e){ e.preventDefault(); document.getElementById('su-nota').hidden=false; });
  document.getElementById('presskit').addEventListener('click',function(e){ e.preventDefault(); document.getElementById('pk-nota').hidden=false; });
  document.getElementById('privacidad').addEventListener('click',function(e){ e.preventDefault(); });
})();
</script>
""" % TR['es']
    html = ('<title>Los Batracios</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;700&display=swap">\n'
            '<style>\n' + fonts + CSS + '</style>\n' + body('es', True) + js + CONVERSA)
    (V / 'index.html').write_text(html, encoding='utf-8')
    _copia(R / 'src/img/casa.jpg', V / 'img/casa.jpg')
    for k in ['mammoth', 'not', 'kyiv', 'elco']: _copia(R / 'src/img' / ('laurel-%s-blanco.png' % k), V / 'img')
    for k in ['nau', 'oma', 'genuino']: _copia(R / 'src/img' / ('logo-%s-azul.png' % k), V / 'img')
    return V


if __name__ == '__main__':
    s = construir_sitio(); v = construir_vista()
    print('sitio:', sorted(str(p.relative_to(s)) for p in s.rglob('*') if p.is_file()))
    print('vista:', (v / 'index.html').stat().st_size)
