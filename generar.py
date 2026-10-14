"""Arma index.html del portafolio a partir de las capturas de cada proyecto.
Uso: python generar.py
"""
import html, os
from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
e = html.escape

PROYECTOS = [
    dict(id='ledkid', nombre='LEDKID', anio='2026', tipo='Proyecto propio',
         desc='Plataforma para enseñar robótica en colegios. El alumno arma circuitos con piezas reales, '
              'los simula con su física, programa la ESP32 en el mismo lugar y avanza por una academia de niveles por grado.',
         tec=['Vue', 'Go', 'MySQL', 'Three.js', 'ESP32'],
         enlace=('Probar en ledkid.com', 'https://ledkid.com')),
    dict(id='mesh', nombre='Mesh', anio='2026', tipo='Proyecto en equipo, universidad',
         desc='Tienda en línea donde varios vendedores ofrecen el mismo producto. Cada una de sus seis bases de datos '
              'guarda lo que mejor maneja, y el sistema detecta fraude en reseñas y en inicios de sesión.',
         tec=['NestJS', 'SvelteKit', 'PostgreSQL', 'MongoDB', 'Redis', 'Neo4j', 'Elasticsearch', 'ClickHouse']),
    dict(id='videos3d', nombre='Edición de videos 3D', anio='2026', tipo='Proyecto propio',
         desc='Intros de logo y videos animados en 3D hechos por código. Cada escena es un script de Python que arma '
              'los modelos, las luces, la cámara y el sonido, y se renderiza con la tarjeta gráfica.',
         tec=['Blender', 'Python', 'ffmpeg'], video='clip-promo.mp4'),
    dict(id='reservas', nombre='Sistema de reservas de viajes', anio='2026', tipo='Proyecto en equipo, universidad',
         desc='Tres sistemas que se conectan entre sí, una aerolínea, una cadena de hoteles y una agencia que vende '
              'vuelos, hoteles y paquetes de los dos. Cada uno tiene su propia API, su base de datos y pruebas automáticas.',
         tec=['C# .NET', 'Java', 'Go', 'Svelte', 'Vue', 'SQL Server', 'Oracle', 'Docker']),
    dict(id='camaras', nombre='Sistema de múltiples cámaras', anio='2025', tipo='Proyecto en equipo, universidad',
         desc='Sigue a varias personas en tiempo real con dos o más cámaras. Detecta a cada persona con YOLO, junta lo '
              'que ve cada cámara y dibuja los recorridos en un mapa del piso medido en metros.',
         tec=['Python', 'YOLO', 'OpenCV']),
    dict(id='pineed', nombre='PINEED', anio='2024', tipo='Proyecto en equipo, universidad',
         desc='Sistema de escritorio para una distribuidora de alimento para ganado. Lleva camiones, pilotos, clientes, '
              'inventario, pedidos, ventas, planilla y un calendario de viajes.',
         tec=['Java', 'Swing', 'NetBeans']),
    dict(id='pixeles', nombre='PIXELES', anio='2026', tipo='Proyecto propio', otro=True,
         desc='Motor que genera pixel art por código, desde personajes animados hasta edificios y efectos. Con él armé '
              'una ciudad que crece sola y que se puede recorrer en 3D.',
         tec=['Python', 'Pillow', 'JavaScript', 'Three.js']),
    dict(id='mipix', nombre='MIPIX', anio='2025', tipo='Proyecto propio', otro=True,
         desc='Plataforma web de videojuegos con registro de usuarios, panel personal y un centro con varios juegos, '
              'entre ellos un shooter multijugador en tiempo real.',
         tec=['Angular', 'TypeScript', 'Node.js', 'Socket.io', 'MongoDB']),
    dict(id='petchan', nombre='Pet-Chan', anio='2025', tipo='Proyecto en equipo, universidad', otro=True,
         desc='Red social de mascotas virtuales. Cada usuario cuida a su mascota de pixel, la viste con lo que compra '
              'en la tienda, publica en foros, entra a comunidades y juega minijuegos.',
         tec=['Node.js', 'Express', 'PostgreSQL', 'EJS']),
]


def capturas(pid):
    carpeta = os.path.join(RAIZ, 'capturas', pid)
    salida = []
    for f in sorted(os.listdir(carpeta)):
        if f.lower().endswith(('.jpg', '.png')):
            w, h = Image.open(os.path.join(carpeta, f)).size
            nombre = os.path.splitext(f)[0].split('-', 1)[-1].replace('-', ' ')
            salida.append(dict(src=f'capturas/{pid}/{f}', w=w, h=h, alt=nombre))
    return salida


def tarjeta(p):
    imgs = capturas(p['id'])
    principal = imgs[0]
    if p.get('video'):
        medio = (f'<video class="principal" src="capturas/{p["id"]}/{p["video"]}" poster="{principal["src"]}" '
                 f'autoplay muted loop playsinline width="{principal["w"]}" height="{principal["h"]}"></video>')
    else:
        medio = (f'<img class="principal" src="{principal["src"]}" width="{principal["w"]}" height="{principal["h"]}" '
                 f'alt="{e(p["nombre"])}, {e(principal["alt"])}" data-i="0">')
    miniaturas = ''.join(
        f'<button class="mini{" activa" if i == 0 else ""}" data-i="{i}" aria-label="Ver {e(im["alt"])}">'
        f'<img src="{im["src"]}" width="{im["w"]}" height="{im["h"]}" alt="" loading="lazy"></button>'
        for i, im in enumerate(imgs))
    datos = ' '.join(f'{im["src"]}|{e(im["alt"])}' for im in imgs)
    enlace = ''
    if p.get('enlace'):
        enlace = f'<a class="boton" href="{p["enlace"][1]}" target="_blank" rel="noopener">{p["enlace"][0]}</a>'
    return f'''
    <article class="proyecto" id="{p["id"]}" data-fotos="{datos}">
      <div class="galeria">
        <div class="marco" role="button" tabindex="0" aria-label="Ver capturas de {e(p["nombre"])} en grande">{medio}</div>
        <div class="miniaturas">{miniaturas}</div>
      </div>
      <div class="texto">
        <div class="arriba"><h3>{e(p["nombre"])}</h3><span class="anio">{p["anio"]}</span></div>
        <span class="tipo">{e(p["tipo"])}</span>
        <p>{e(p["desc"])}</p>
        <div class="tec">{"".join(f"<i>{e(t)}</i>" for t in p["tec"])}</div>
        {enlace}
      </div>
    </article>'''


principales = ''.join(tarjeta(p) for p in PROYECTOS if not p.get('otro'))
otros = ''.join(tarjeta(p) for p in PROYECTOS if p.get('otro'))

CSS = '''
  :root { --oscuro:#3a3035; --oscuro2:#2a2226; --gris:#58585a; --crema:#fdfaf5; --rosa:#e4c4b4; --verde:#4b5232; --borde:#e6e0d8; }
  * { box-sizing:border-box; margin:0; padding:0; }
  html { scroll-behavior:smooth; }
  body { font-family:"Poppins",Arial,sans-serif; background:var(--crema); color:#3d3d3d; }
  header { background:var(--oscuro); color:#fff; padding:44px 0 36px; }
  .in { max-width:1180px; margin:0 auto; padding:0 16px; }
  header h1 { font-size:clamp(26px,4.4vw,40px); font-weight:700; letter-spacing:.5px; }
  header p { color:var(--rosa); margin-top:8px; font-size:15px; max-width:640px; line-height:1.55; }
  header nav { margin-top:18px; display:flex; flex-wrap:wrap; gap:8px; }
  header nav a { color:#fff; text-decoration:none; font-size:13px; border:1px solid #6a6266; padding:5px 14px; border-radius:20px; }
  header nav a:hover { background:#4a4045; }
  main { padding-bottom:56px; }
  h2 { font-size:22px; color:var(--oscuro); border-bottom:3px solid var(--oscuro); padding-bottom:6px; margin:40px 0 22px; }
  .proyecto { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(0,1fr); gap:26px; background:#fff;
              border:1px solid var(--borde); border-radius:10px; padding:18px; margin-bottom:24px; scroll-margin-top:16px; }
  .marco { aspect-ratio:16/9; background:var(--oscuro2); border-radius:6px; overflow:hidden; cursor:zoom-in;
           display:flex; align-items:center; justify-content:center; }
  .marco .principal { width:100%; height:100%; object-fit:contain; display:block; }
  .miniaturas { display:flex; gap:8px; margin-top:10px; overflow-x:auto; padding-bottom:2px; }
  .mini { flex:0 0 auto; width:86px; aspect-ratio:16/9; border:2px solid transparent; border-radius:4px; overflow:hidden;
          background:var(--oscuro2); cursor:pointer; padding:0; opacity:.65; transition:opacity .15s, border-color .15s; }
  .mini img { width:100%; height:100%; object-fit:cover; display:block; }
  .mini:hover, .mini.activa { opacity:1; border-color:var(--oscuro); }
  .texto { display:flex; flex-direction:column; gap:10px; padding-top:2px; }
  .arriba { display:flex; align-items:baseline; justify-content:space-between; gap:12px; }
  .texto h3 { font-size:22px; color:var(--verde); line-height:1.25; }
  .anio { font-size:13px; color:var(--gris); font-weight:500; }
  .tipo { font-size:12.5px; color:var(--oscuro); background:#f3ece6; align-self:flex-start; padding:2px 10px; border-radius:12px; }
  .texto p { font-size:14.5px; line-height:1.65; }
  .tec { display:flex; flex-wrap:wrap; gap:5px; }
  .tec i { font-style:normal; font-size:12px; background:var(--oscuro); color:#fff; padding:2px 10px; border-radius:11px; }
  .boton { align-self:flex-start; margin-top:4px; background:#f6b93b; color:#2a2226; font-weight:600; font-size:14px;
           text-decoration:none; padding:8px 16px; border-radius:6px; }
  .boton:hover { background:#f3a91b; }
  footer { text-align:center; font-size:12.5px; color:var(--gris); padding:0 16px 36px; }
  footer a { color:inherit; }
  /* visor */
  .visor { position:fixed; inset:0; background:rgba(15,12,14,.94); display:none; align-items:center; justify-content:center; z-index:10; touch-action:pan-y; }
  .visor.abierto { display:flex; }
  .visor img { max-width:94vw; max-height:84vh; object-fit:contain; box-shadow:0 8px 40px rgba(0,0,0,.5); }
  .visor .pie { position:absolute; bottom:18px; left:0; right:0; text-align:center; color:#ddd; font-size:13.5px; }
  .visor button { position:absolute; background:rgba(255,255,255,.12); color:#fff; border:0; width:48px; height:48px;
                  border-radius:50%; font-size:22px; cursor:pointer; }
  .visor button:hover { background:rgba(255,255,255,.25); }
  .visor .cerrar { top:16px; right:16px; }
  .visor .ant { left:16px; top:50%; transform:translateY(-50%); }
  .visor .sig { right:16px; top:50%; transform:translateY(-50%); }
  @media (max-width:820px) {
    .proyecto { grid-template-columns:minmax(0,1fr); gap:16px; padding:14px; }
    .texto h3 { font-size:20px; }
    .visor .ant, .visor .sig { display:none; }
  }
'''

JS = '''
(function () {
  var visor = document.querySelector('.visor'), foto = visor.querySelector('img'), pie = visor.querySelector('.pie');
  var lista = [], pos = 0, nombre = '';
  function mostrar() {
    var f = lista[pos].split('|');
    foto.src = f[0]; foto.alt = nombre + ', ' + f[1];
    pie.textContent = nombre + '   ' + (pos + 1) + ' de ' + lista.length;
  }
  function abrir(art, i) {
    lista = art.dataset.fotos.split(' '); pos = i; nombre = art.querySelector('h3').textContent;
    mostrar(); visor.classList.add('abierto'); document.body.style.overflow = 'hidden';
  }
  function cerrar() { visor.classList.remove('abierto'); document.body.style.overflow = ''; }
  function mover(d) { pos = (pos + d + lista.length) % lista.length; mostrar(); }
  document.querySelectorAll('.proyecto').forEach(function (art) {
    var marco = art.querySelector('.marco'), actual = 0;
    var video = marco.querySelector('video') ? marco.innerHTML : '';
    art.querySelectorAll('.mini').forEach(function (b) {
      b.addEventListener('click', function () {
        actual = +b.dataset.i;
        art.querySelectorAll('.mini').forEach(function (x) { x.classList.toggle('activa', x === b); });
        if (actual === 0 && video) { marco.innerHTML = video; return; }
        var img = document.createElement('img');
        img.className = 'principal';
        img.src = b.querySelector('img').getAttribute('src');
        img.alt = '';
        marco.innerHTML = '';
        marco.appendChild(img);
      });
    });
    function ir() { abrir(art, actual); }
    marco.addEventListener('click', ir);
    marco.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); ir(); } });
  });
  visor.querySelector('.cerrar').addEventListener('click', cerrar);
  visor.querySelector('.ant').addEventListener('click', function () { mover(-1); });
  visor.querySelector('.sig').addEventListener('click', function () { mover(1); });
  visor.addEventListener('click', function (ev) { if (ev.target === visor) cerrar(); });
  document.addEventListener('keydown', function (ev) {
    if (!visor.classList.contains('abierto')) return;
    if (ev.key === 'Escape') cerrar();
    if (ev.key === 'ArrowLeft') mover(-1);
    if (ev.key === 'ArrowRight') mover(1);
  });
  var x0 = null;
  visor.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
  visor.addEventListener('touchend', function (ev) {
    if (x0 === null) return;
    var dx = ev.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) mover(dx < 0 ? 1 : -1);
  });
})();
'''

PAGINA = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proyectos de José Manuel González Corado</title>
<meta name="description" content="Portafolio de proyectos de José Manuel González Corado, estudiante de Ingeniería en Sistemas y profesor de robótica.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="in">
    <h1>José Manuel González Corado</h1>
    <p>Estudiante de tercer año de Ingeniería en Sistemas y profesor de robótica. Estos son mis proyectos, con capturas reales de cada uno.</p>
    <nav>
      <a href="#principales">Proyectos</a>
      <a href="#otros">Otros proyectos</a>
      <a href="https://ledkid.com" target="_blank" rel="noopener">ledkid.com</a>
      <a href="https://tunuba.github.io/certificaciones/">Certificaciones</a>
      <a href="https://github.com/Tunuba">GitHub</a>
    </nav>
  </div>
</header>
<main class="in">
  <h2 id="principales">Proyectos</h2>{principales}
  <h2 id="otros">Otros proyectos</h2>{otros}
</main>
<footer>José Manuel González Corado, <a href="mailto:memitoscorado@gmail.com">memitoscorado@gmail.com</a></footer>
<div class="visor" role="dialog" aria-modal="true" aria-label="Capturas en grande">
  <img alt="">
  <div class="pie"></div>
  <button class="cerrar" aria-label="Cerrar">&#x2715;</button>
  <button class="ant" aria-label="Anterior">&#x2039;</button>
  <button class="sig" aria-label="Siguiente">&#x203A;</button>
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
