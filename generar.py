"""Arma index.html del portafolio a partir de las capturas de cada proyecto.
Uso: python generar.py

Cada proyecto lee su carpeta capturas/<id>/. El orden de las fotos es el numero del archivo.
Si junto a una foto hay un .mp4 con el mismo nombre, la miniatura reproduce ese clip;
si ademas hay un <nombre>-completo.mp4, el visor grande abre el video completo con audio.
"""
import html, os
from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
e = html.escape

# Cada proyecto tiene el color de su LED en la cabecera; lo identifica en toda la pagina.
PROYECTOS = [
    dict(id='ledkid', nombre='LEDKID', anio='2026', tipo='Proyecto propio', led='#FFB21A',
         desc='Plataforma para enseñar robótica en colegios. El alumno arma circuitos con piezas reales, '
              'los simula con su física, programa la ESP32 en el mismo lugar y avanza por una academia de niveles por grado.',
         tec=['Vue', 'Go', 'MySQL', 'Three.js', 'ESP32'],
         enlace=('Probar LEDKID en vivo', 'https://ledkid.com')),
    dict(id='mesh', nombre='Mesh', anio='2026', tipo='Proyecto en equipo, universidad', led='#3D8BFF',
         desc='Tienda en línea donde varios vendedores ofrecen el mismo producto. Cada una de sus seis bases de datos '
              'guarda lo que mejor maneja, y el sistema detecta fraude en reseñas y en inicios de sesión.',
         tec=['NestJS', 'SvelteKit', 'PostgreSQL', 'MongoDB', 'Redis', 'Neo4j', 'Elasticsearch', 'ClickHouse']),
    dict(id='videos3d', nombre='Edición de videos 3D', corto='Videos 3D', anio='2026', tipo='Proyecto propio', led='#FF4FB4',
         desc='Intros de logo y videos animados en 3D hechos por código. Cada escena es un script de Python que arma '
              'los modelos, las luces, la cámara y el sonido, y se renderiza con la tarjeta gráfica.',
         tec=['Blender', 'Python', 'ffmpeg']),
    dict(id='reservas', nombre='Sistema de reservas de viajes', corto='Reservas', anio='2026', tipo='Proyecto en equipo, universidad', led='#2BD47D',
         desc='Tres sistemas que se conectan entre sí, una aerolínea, una cadena de hoteles y una agencia que vende '
              'vuelos, hoteles y paquetes de los dos. Cada uno tiene su propia API, su base de datos y pruebas automáticas.',
         tec=['C# .NET', 'Java', 'Go', 'Svelte', 'Vue', 'SQL Server', 'Oracle', 'Docker']),
    dict(id='camaras', nombre='Sistema de múltiples cámaras', corto='Cámaras', anio='2025', tipo='Proyecto en equipo, universidad', led='#FF4438',
         desc='Sigue a varias personas en tiempo real con dos o más cámaras. Detecta a cada persona con YOLO, junta lo '
              'que ve cada cámara y dibuja los recorridos en un mapa del piso medido en metros.',
         tec=['Python', 'YOLO', 'OpenCV']),
    dict(id='pineed', nombre='PINEED', anio='2024', tipo='Proyecto en equipo, universidad', led='#E4EBFF',
         desc='Sistema de escritorio para una distribuidora de alimento para ganado. Lleva camiones, pilotos, clientes, '
              'inventario, pedidos, ventas, planilla y un calendario de viajes.',
         tec=['Java', 'Swing', 'NetBeans']),
    dict(id='pixeles', nombre='PIXELES', anio='2026', tipo='Proyecto propio', led='#7CE04A', otro=True,
         desc='Motor que genera pixel art por código, desde personajes animados hasta edificios y efectos. Con él armé '
              'una ciudad que crece sola y que se puede recorrer en 3D.',
         tec=['Python', 'Pillow', 'JavaScript', 'Three.js']),
    dict(id='mipix', nombre='MIPIX', anio='2025', tipo='Proyecto propio', led='#29D9E8', otro=True,
         desc='Plataforma web de videojuegos con registro de usuarios, panel personal y un centro con varios juegos, '
              'entre ellos un shooter multijugador en tiempo real.',
         tec=['Angular', 'TypeScript', 'Node.js', 'Socket.io', 'MongoDB']),
    dict(id='petchan', nombre='Pet-Chan', anio='2025', tipo='Proyecto en equipo, universidad', led='#A970FF', otro=True,
         desc='Red social de mascotas virtuales. Cada usuario cuida a su mascota de pixel, la viste con lo que compra '
              'en la tienda, publica en foros, entra a comunidades y juega minijuegos.',
         tec=['Node.js', 'Express', 'PostgreSQL', 'EJS']),
]


def capturas(pid):
    carpeta = os.path.join(RAIZ, 'capturas', pid)
    salida = []
    for f in sorted(os.listdir(carpeta)):
        if not f.lower().endswith(('.jpg', '.png')):
            continue
        w, h = Image.open(os.path.join(carpeta, f)).size
        base = os.path.splitext(f)[0]
        existe = lambda n: os.path.exists(os.path.join(carpeta, n))
        os.makedirs(os.path.join(carpeta, 'mini'), exist_ok=True)
        mini = os.path.join(carpeta, 'mini', base + '.jpg')
        if not os.path.exists(mini) or os.path.getmtime(mini) < os.path.getmtime(os.path.join(carpeta, f)):
            im = Image.open(os.path.join(carpeta, f)).convert('RGB')
            im.thumbnail((320, 200), Image.LANCZOS)
            im.save(mini, quality=82, optimize=True)
        salida.append(dict(
            src=f'capturas/{pid}/{f}', mini=f'capturas/{pid}/mini/{base}.jpg', w=w, h=h,
            alt=base.split('-', 1)[-1].replace('-', ' '),
            clip=f'capturas/{pid}/{base}.mp4' if existe(base + '.mp4') else '',
            completo=f'capturas/{pid}/{base}-completo.mp4' if existe(base + '-completo.mp4') else ''))
    return salida


def led_html(p, i):
    return (f'<a class="led" href="#{p["id"]}" style="--c:{p["led"]};--i:{i}">'
            f'<span class="bombillo" aria-hidden="true"></span><span class="patas" aria-hidden="true"></span>'
            f'<span class="nom">{e(p.get("corto", p["nombre"]))}</span></a>')


def modulo(p, lado):
    fotos = capturas(p['id'])
    f0 = fotos[0]
    if f0['clip']:
        escena = (f'<video class="vista" src="{f0["clip"]}" poster="{f0["src"]}" autoplay muted loop playsinline '
                  f'width="{f0["w"]}" height="{f0["h"]}"></video>')
    else:
        escena = (f'<img class="vista" src="{f0["src"]}" width="{f0["w"]}" height="{f0["h"]}" '
                  f'alt="{e(p["nombre"])}, {e(f0["alt"])}">')
    tira = ''.join(
        f'<button type="button" class="cuadro{" activo" if i == 0 else ""}{" mueve" if f["clip"] else ""}" '
        f'data-i="{i}" data-clip="{f["clip"]}" aria-label="Ver {e(f["alt"])}"'
        f'{" aria-current=\"true\"" if i == 0 else ""}>'
        f'<img src="{f["mini"]}" data-grande="{f["src"]}" width="160" height="100" alt="" loading="lazy" decoding="async"></button>'
        for i, f in enumerate(fotos))
    datos = ';'.join(f'{f["src"]}|{e(f["alt"])}|{f["completo"] or f["clip"]}|{"1" if f["completo"] else ""}'
                     for f in fotos)
    enlace = ''
    if p.get('enlace'):
        enlace = f'<a class="vivo" href="{p["enlace"][1]}" target="_blank" rel="noopener">{e(p["enlace"][0])}</a>'
    ver = 'Ver los videos completos con sonido' if any(f['completo'] for f in fotos) else 'Ver en grande'
    return f'''
  <article class="modulo {lado}" id="{p["id"]}" style="--c:{p["led"]}" data-fotos="{datos}">
    <div class="galeria">
      <button type="button" class="pantalla" aria-label="{e(ver)}, {e(p["nombre"])}">{escena}<span class="ampliar">{e(ver)}</span></button>
      <div class="tira">{tira}</div>
    </div>
    <div class="ficha">
      <h3><span class="punto" aria-hidden="true"></span>{e(p["nombre"])}</h3>
      <p class="meta">{p["anio"]}, {e(p["tipo"].lower())}</p>
      <p class="desc">{e(p["desc"])}</p>
      <ul class="tec">{"".join(f"<li>{e(t)}</li>" for t in p["tec"])}</ul>
      {enlace}
    </div>
  </article>'''


principales = [p for p in PROYECTOS if not p.get('otro')]
otros = [p for p in PROYECTOS if p.get('otro')]
leds = ''.join(led_html(p, i) for i, p in enumerate(PROYECTOS))
html_principales = ''.join(modulo(p, 'izq' if i % 2 == 0 else 'der') for i, p in enumerate(principales))
html_otros = ''.join(modulo(p, 'izq' if i % 2 == 0 else 'der') for i, p in enumerate(otros))

CSS = r'''
  :root {
    --cobalto:#16337A; --cobalto-2:#1C3F93; --tinta:#0E1A33; --pizarra:#4A5670;
    --fondo:#EEF1F5; --papel:#FFFFFF; --linea:#D5DBE5;
    --ambar:#FFB21A; --riel-rojo:#E0303F; --riel-azul:#2266E8;
    --titulo:"Bricolage Grotesque", "Segoe UI", sans-serif;
    --texto:"Atkinson Hyperlegible", "Segoe UI", sans-serif;
  }
  * { box-sizing:border-box; margin:0; padding:0; }
  html { scroll-behavior:smooth; }
  body { font-family:var(--texto); font-size:17px; line-height:1.6; color:var(--tinta); background:var(--fondo); }
  a { color:inherit; }
  :focus-visible { outline:3px solid var(--ambar); outline-offset:3px; border-radius:4px; }
  .ancho { max-width:1200px; margin:0 auto; padding:0 24px; }

  /* Cabecera: la placa */
  .placa { background:var(--cobalto); color:#fff; position:relative; overflow:hidden; }
  .placa::before { content:""; position:absolute; inset:0; pointer-events:none; opacity:.55;
    background:
      radial-gradient(circle at 1px 1px, rgba(255,255,255,.10) 1.2px, transparent 1.6px) 0 0/22px 22px; }
  .placa .ancho { position:relative; padding-top:64px; padding-bottom:40px; }
  .placa h1 { font-family:var(--titulo); font-weight:800; font-size:clamp(42px,7.6vw,118px); line-height:.95;
              letter-spacing:-.02em; font-variation-settings:"wdth" 92; }
  .placa h1 span { display:block; }
  .placa .quien { margin-top:22px; max-width:56ch; font-size:19px; line-height:1.55; color:#DCE5FA; }
  .enlaces { margin-top:26px; display:flex; flex-wrap:wrap; gap:10px 22px; font-size:16px; }
  .enlaces a { color:#fff; text-decoration-color:rgba(255,178,26,.7); text-decoration-thickness:2px; text-underline-offset:5px; }
  .enlaces a:hover { color:var(--ambar); }

  /* La protoboard con un LED por proyecto */
  .proto { margin-top:46px; background:#E9EDF3; border-radius:10px; padding:16px 18px 14px; color:var(--tinta);
           box-shadow:0 1px 0 rgba(255,255,255,.4) inset, 0 18px 40px rgba(5,14,40,.35); }
  .riel { height:4px; border-radius:2px; }
  .riel.rojo { background:var(--riel-rojo); } .riel.azul { background:var(--riel-azul); }
  .agujeros { height:12px; margin:6px 0;
              background:radial-gradient(circle, #9AA6B8 2px, transparent 2.6px) 0 50%/16px 12px repeat-x; }
  .leds { display:grid; grid-template-columns:repeat(9,minmax(0,1fr)); gap:4px; padding:14px 0 6px;
          background:radial-gradient(circle, #B6C0CF 2px, transparent 2.6px) 0 0/16px 16px; }
  .led { display:flex; flex-direction:column; align-items:center; text-decoration:none; color:var(--tinta); padding:4px 2px; border-radius:8px; }
  .bombillo { width:30px; height:38px; border-radius:15px 15px 4px 4px; position:relative;
              background:color-mix(in srgb, var(--c) 30%, #6b7383); box-shadow:inset 0 -6px 0 rgba(0,0,0,.18);
              outline:1px solid rgba(14,26,51,.18); outline-offset:-1px;
              animation:encender .5s ease-out forwards; animation-delay:calc(.35s + var(--i) * .16s); }
  .bombillo::after { content:""; position:absolute; left:7px; top:6px; width:7px; height:12px; border-radius:4px; background:rgba(255,255,255,.55); }
  .patas { width:12px; height:16px; border-left:2px solid #8E99A9; border-right:2px solid #8E99A9; margin-top:-2px; }
  .led .nom { margin-top:6px; font-family:var(--titulo); font-size:13.5px; font-weight:600; line-height:1.15; text-align:center; }
  .led:hover .bombillo, .led:focus-visible .bombillo { box-shadow:inset 0 -6px 0 rgba(0,0,0,.12), 0 0 26px 8px color-mix(in srgb, var(--c) 70%, transparent); }
  @keyframes encender {
    to { background:var(--c); box-shadow:inset 0 -6px 0 rgba(0,0,0,.12), 0 0 18px 4px color-mix(in srgb, var(--c) 55%, transparent); }
  }

  /* Secciones */
  .seccion { padding:72px 0 8px; }
  .seccion > .ancho > h2 { font-family:var(--titulo); font-weight:800; font-size:clamp(32px,4.6vw,52px); letter-spacing:-.025em;
                            line-height:1; display:flex; align-items:flex-end; gap:18px; }
  .seccion > .ancho > h2::after { content:""; flex:1; height:4px; margin-bottom:10px; border-radius:2px;
    background:linear-gradient(var(--riel-rojo) 0 0) top/100% 1.5px no-repeat, linear-gradient(var(--riel-azul) 0 0) bottom/100% 1.5px no-repeat; }
  .seccion .intro { margin-top:12px; color:var(--pizarra); max-width:60ch; }

  /* Modulos de proyecto */
  .modulo { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(0,1fr); gap:44px; align-items:start;
            padding:44px 0; border-bottom:1px solid var(--linea); scroll-margin-top:12px; }
  .modulo.der { grid-template-columns:minmax(0,1fr) minmax(0,1.5fr); }
  .modulo.der .galeria { order:2; }
  .seccion .modulo:last-child { border-bottom:0; }
  .pantalla { display:block; width:100%; aspect-ratio:16/10; background:var(--tinta); border:0; border-radius:12px; padding:10px;
              position:relative; cursor:zoom-in; box-shadow:0 22px 46px -22px rgba(14,26,51,.55); }
  .pantalla .vista { width:100%; height:100%; object-fit:contain; display:block; border-radius:5px; background:#0A1326; }
  .ampliar { position:absolute; right:18px; bottom:18px; background:rgba(14,26,51,.82); color:#fff; font-size:13.5px;
             padding:6px 12px; border-radius:20px; opacity:0; transform:translateY(4px); transition:opacity .2s, transform .2s; }
  .pantalla:hover .ampliar, .pantalla:focus-visible .ampliar { opacity:1; transform:none; }
  .tira { display:flex; gap:10px; margin-top:14px; overflow-x:auto; padding:2px 2px 6px; scrollbar-width:thin; }
  .cuadro { flex:0 0 auto; width:96px; aspect-ratio:16/10; border:0; padding:0; border-radius:6px; overflow:hidden; cursor:pointer;
            background:var(--tinta); position:relative; opacity:.6; transition:opacity .15s;
            box-shadow:0 0 0 2px transparent; }
  .cuadro img { width:100%; height:100%; object-fit:cover; display:block; }
  .cuadro:hover { opacity:.9; }
  .cuadro.activo { opacity:1; box-shadow:0 0 0 2px var(--fondo), 0 0 0 4px var(--c); }
  .cuadro.mueve::after { content:""; position:absolute; left:50%; top:50%; transform:translate(-35%,-50%);
    border-style:solid; border-width:8px 0 8px 13px; border-color:transparent transparent transparent #fff; filter:drop-shadow(0 0 3px rgba(0,0,0,.8)); }

  .ficha { padding-top:6px; }
  .ficha h3 { font-family:var(--titulo); font-weight:700; font-size:clamp(28px,3.2vw,40px); line-height:1.05; letter-spacing:-.02em;
              display:flex; align-items:baseline; gap:14px; }
  .punto { flex:0 0 auto; width:14px; height:14px; border-radius:50%; background:var(--c); transform:translateY(-3px);
           box-shadow:0 0 0 1px rgba(14,26,51,.22), 0 0 0 4px color-mix(in srgb, var(--c) 25%, transparent), 0 0 14px color-mix(in srgb, var(--c) 80%, transparent); }
  .meta { margin-top:10px; color:var(--pizarra); font-size:15.5px; }
  .desc { margin-top:16px; max-width:46ch; }
  .tec { list-style:none; display:flex; flex-wrap:wrap; gap:8px; margin-top:20px; }
  .tec li { font-size:14px; padding:3px 12px; border-radius:6px; background:var(--papel); border:1px solid var(--linea); }
  .vivo { display:inline-block; margin-top:24px; background:var(--ambar); color:var(--tinta); font-weight:700; text-decoration:none;
          padding:11px 20px; border-radius:8px; box-shadow:0 0 0 0 rgba(255,178,26,.5); transition:box-shadow .2s; }
  .vivo:hover { box-shadow:0 0 0 6px rgba(255,178,26,.28); }

  footer { margin-top:72px; background:var(--tinta); color:#C9D3E6; }
  footer .ancho { padding-top:40px; padding-bottom:44px; display:flex; flex-wrap:wrap; gap:14px 32px; align-items:baseline; justify-content:space-between; }
  footer strong { font-family:var(--titulo); color:#fff; font-size:22px; font-weight:700; }
  footer a { color:#fff; text-underline-offset:4px; }

  /* Visor */
  .visor { position:fixed; inset:0; z-index:20; background:rgba(8,14,30,.95); display:none; flex-direction:column;
           align-items:center; justify-content:center; padding:56px 72px 64px; }
  .visor.abierto { display:flex; }
  .visor .lugar { display:flex; align-items:center; justify-content:center; width:100%; height:100%; min-height:0; }
  .visor .lugar img, .visor .lugar video { max-width:100%; max-height:100%; object-fit:contain; border-radius:6px; background:#000;
                                           box-shadow:0 20px 60px rgba(0,0,0,.6); }
  .visor .pie { position:absolute; bottom:20px; left:0; right:0; text-align:center; color:#C9D3E6; font-size:15px; }
  .visor button { position:absolute; width:52px; height:52px; border-radius:50%; border:0; cursor:pointer;
                  background:rgba(255,255,255,.10); color:#fff; font-size:26px; line-height:1; }
  .visor button:hover { background:rgba(255,255,255,.22); }
  .visor .cerrar { top:14px; right:16px; font-size:22px; }
  .visor .ant { left:14px; top:50%; transform:translateY(-50%); }
  .visor .sig { right:14px; top:50%; transform:translateY(-50%); }

  @media (max-width:900px) {
    body { font-size:16px; }
    .ancho { padding:0 16px; }
    .placa .ancho { padding-top:44px; padding-bottom:28px; }
    .leds { grid-template-columns:repeat(5,minmax(0,1fr)); row-gap:14px; }
    .modulo, .modulo.der { grid-template-columns:minmax(0,1fr); gap:22px; padding:34px 0; }
    .modulo.der .galeria { order:0; }
    .ampliar { opacity:1; transform:none; font-size:12.5px; }
    .visor { padding:56px 8px 60px; }
    .visor .ant, .visor .sig { display:none; }
  }
  @media (prefers-reduced-motion:reduce) {
    html { scroll-behavior:auto; }
    .bombillo { animation-duration:0s; animation-delay:0s; }
  }
'''

JS = r'''
(function () {
  var visor = document.querySelector('.visor'), lugar = visor.querySelector('.lugar'), pie = visor.querySelector('.pie');
  var lista = [], pos = 0, nombre = '', origen = null;
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clip(src, poster) {
    var v = document.createElement('video');
    v.src = src; v.poster = poster; v.muted = true; v.loop = true; v.playsInline = true;
    v.setAttribute('playsinline', ''); v.setAttribute('muted', '');
    if (!quieto) { v.autoplay = true; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    else { v.controls = true; }
    return v;
  }
  function mostrar() {
    var f = lista[pos].split('|'), el;
    if (f[2]) {
      el = document.createElement('video');
      el.src = f[2]; el.poster = f[0]; el.controls = true; el.playsInline = true;
      if (f[3]) { el.muted = false; } else { el.muted = true; el.loop = true; }
      var p = el.play(); if (p && p.catch) p.catch(function () {});
    } else {
      el = document.createElement('img'); el.src = f[0]; el.alt = nombre + ', ' + f[1];
    }
    lugar.innerHTML = ''; lugar.appendChild(el);
    pie.textContent = nombre + ', ' + (pos + 1) + ' de ' + lista.length;
  }
  function abrir(art, i, boton) {
    lista = art.dataset.fotos.split(';'); pos = i; nombre = art.querySelector('h3').textContent; origen = boton;
    document.querySelectorAll('.modulo video.vista').forEach(function (v) { v.pause(); });
    mostrar(); visor.classList.add('abierto'); document.body.style.overflow = 'hidden';
    visor.querySelector('.cerrar').focus();
  }
  function cerrar() {
    visor.classList.remove('abierto'); lugar.innerHTML = ''; document.body.style.overflow = '';
    if (!quieto) document.querySelectorAll('.modulo video.vista').forEach(function (v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); });
    if (origen) origen.focus();
  }
  function mover(d) { pos = (pos + d + lista.length) % lista.length; mostrar(); }

  document.querySelectorAll('.modulo').forEach(function (art) {
    var pantalla = art.querySelector('.pantalla'), actual = 0;
    art.querySelectorAll('.cuadro').forEach(function (b) {
      b.addEventListener('click', function () {
        actual = +b.dataset.i;
        art.querySelectorAll('.cuadro').forEach(function (x) {
          x.classList.toggle('activo', x === b);
          if (x === b) x.setAttribute('aria-current', 'true'); else x.removeAttribute('aria-current');
        });
        var poster = b.querySelector('img').dataset.grande, nuevo;
        if (b.dataset.clip) { nuevo = clip(b.dataset.clip, poster); }
        else { nuevo = document.createElement('img'); nuevo.src = poster; nuevo.alt = ''; }
        nuevo.className = 'vista';
        var viejo = pantalla.querySelector('.vista'); pantalla.replaceChild(nuevo, viejo);
      });
    });
    pantalla.addEventListener('click', function () { abrir(art, actual, pantalla); });
  });
  if (quieto) document.querySelectorAll('.modulo video.vista').forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.controls = true; });

  visor.querySelector('.cerrar').addEventListener('click', cerrar);
  visor.querySelector('.ant').addEventListener('click', function () { mover(-1); });
  visor.querySelector('.sig').addEventListener('click', function () { mover(1); });
  visor.addEventListener('click', function (ev) { if (ev.target === visor || ev.target === lugar) cerrar(); });
  document.addEventListener('keydown', function (ev) {
    if (!visor.classList.contains('abierto')) return;
    if (ev.key === 'Escape') cerrar();
    else if (ev.key === 'ArrowLeft') mover(-1);
    else if (ev.key === 'ArrowRight') mover(1);
    else if (ev.key === 'Tab') {
      var b = Array.prototype.filter.call(visor.querySelectorAll('button, video'), function (x) { return x.offsetParent !== null; });
      var i = b.indexOf(document.activeElement);
      if (ev.shiftKey && i <= 0) { ev.preventDefault(); b[b.length - 1].focus(); }
      else if (!ev.shiftKey && i === b.length - 1) { ev.preventDefault(); b[0].focus(); }
    }
  });
  var x0 = null;
  visor.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
  visor.addEventListener('touchend', function (ev) {
    if (x0 === null) return;
    var dx = ev.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 45) mover(dx < 0 ? 1 : -1);
  });
})();
'''

PAGINA = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proyectos de José Manuel González Corado</title>
<meta name="description" content="Portafolio de José Manuel González Corado, estudiante de Ingeniería en Sistemas y profesor de robótica en Guatemala.">
<meta name="theme-color" content="#16337A">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="placa">
  <div class="ancho">
    <h1><span>José Manuel</span> <span>González Corado</span></h1>
    <p class="quien">Estudio tercer año de Ingeniería en Sistemas y doy clases de robótica. Hago proyectos de software y de hardware que la gente usa de verdad.</p>
    <nav class="enlaces" aria-label="Enlaces">
      <a href="https://ledkid.com" target="_blank" rel="noopener">ledkid.com</a>
      <a href="https://tunuba.github.io/certificaciones/">Certificaciones</a>
      <a href="https://github.com/Tunuba">GitHub</a>
      <a href="mailto:memitoscorado@gmail.com">memitoscorado@gmail.com</a>
    </nav>
    <div class="proto" role="navigation" aria-label="Ir a un proyecto">
      <div class="riel rojo"></div><div class="agujeros"></div>
      <div class="leds">{leds}</div>
      <div class="agujeros"></div><div class="riel azul"></div>
    </div>
  </div>
</header>
<main>
  <section class="seccion" aria-labelledby="t-principales">
    <div class="ancho">
      <h2 id="t-principales">Proyectos</h2>
      <p class="intro">Todas las capturas son reales, tomadas de cada proyecto funcionando. Toca una imagen para verla en grande.</p>
      {html_principales}
    </div>
  </section>
  <section class="seccion" aria-labelledby="t-otros">
    <div class="ancho">
      <h2 id="t-otros">Otros proyectos</h2>
      {html_otros}
    </div>
  </section>
</main>
<footer>
  <div class="ancho">
    <strong>José Manuel González Corado</strong>
    <span>San José Pinula, Guatemala. Escríbeme a <a href="mailto:memitoscorado@gmail.com">memitoscorado@gmail.com</a></span>
  </div>
</footer>
<div class="visor" role="dialog" aria-modal="true" aria-label="Vista en grande">
  <div class="lugar"></div>
  <div class="pie" aria-live="polite"></div>
  <button type="button" class="cerrar" aria-label="Cerrar">&#x2715;</button>
  <button type="button" class="ant" aria-label="Anterior">&#x2039;</button>
  <button type="button" class="sig" aria-label="Siguiente">&#x203A;</button>
</div>
<script>{JS}</script>
</body>
</html>
'''

with open(os.path.join(RAIZ, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(PAGINA)
with open(os.path.join(RAIZ, 'README.md'), 'w', encoding='utf-8') as f:
    f.write('# Proyectos\n\nPortafolio de José Manuel González Corado, con capturas reales de cada proyecto.\n\n'
            'Verlo en https://tunuba.github.io/proyectos/\n\n'
            'La página se arma con `python generar.py` a partir de las carpetas de `capturas/`.\n')
print('index.html listo,', len(PROYECTOS), 'proyectos')
