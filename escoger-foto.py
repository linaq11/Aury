#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cambia la foto de la banda superior de vitrina.html.

    python escoger-foto.py 3          # usa plato-3
    python escoger-foto.py 3 --cerca  # el mismo plato, mas de cerca
    python escoger-foto.py            # muestra las opciones

Por defecto el recorte es el MAS LEJOS que cabe en la banda: toma todo el
ancho de la foto. Con --cerca se acerca un 25%.

Busca sola la franja mas nitida de cada foto, porque son fotos con poca
profundidad de campo y el centro geometrico no siempre es el enfocado.
"""
import sys, os, glob
from PIL import Image, ImageFilter

AQUI   = os.path.dirname(os.path.abspath(__file__))
FOTOS  = (r"C:\Users\linaq\Downloads\restaurante-instagram"
          r"\Fotos\platos-reales")
DESTINO = os.path.join(AQUI, "img", "hero.jpg")

# la banda es 1.4 de proporcion (840x600)
PROP = 840 / 600
SALIDA = (840, 600)

NOMBRES = {
    "1": "carne desmechada, plato blanco",
    "2": "pollo frito, plato blanco",
    "3": "carne, plato negro (vista amplia)",
    "4": "carne, plato negro (mas cerca)",
    "5": "sancocho de costilla",
    "6": "pescado frito con patacones",
}

def nitidez(im):
    g = im.convert("L").resize((400, int(400 * im.height / im.width)), Image.LANCZOS)
    px = list(g.filter(ImageFilter.FIND_EDGES).getdata())
    m = sum(px) / len(px)
    return sum((v - m) ** 2 for v in px) / len(px)

def archivo(num):
    for f in glob.glob(os.path.join(FOTOS, "*.jpeg")):
        base = os.path.basename(f)
        if base.startswith("plato-%s" % num):
            return f
    return None

if len(sys.argv) < 2:
    print("Fotos disponibles:\n")
    for k, v in NOMBRES.items():
        f = archivo(k)
        marca = " " if f else "  (no esta)"
        print("  %s  %s%s" % (k, v, marca))
    print("\n  python escoger-foto.py 3          (vista amplia)")
    print("  python escoger-foto.py 3 --cerca  (mas cerca)")
    sys.exit(0)

num = sys.argv[1]
cerca = "--cerca" in sys.argv
src = archivo(num)
if not src:
    print("No encuentro la foto %s. Corre el script sin argumentos para ver cuales hay." % num)
    sys.exit(1)

im = Image.open(src).convert("RGB")
W, H = im.size
ancho = int(W * 0.75) if cerca else W
bh = int(ancho / PROP)

# buscar la franja mas nitida
mejor = (-1, 0, 0)
for cy in range(25, 80, 3):
    top = int(H * cy / 100 - bh / 2)
    izq = (W - ancho) // 2
    if top < 0 or top + bh > H:
        continue
    v = nitidez(im.crop((izq, top, izq + ancho, top + bh)))
    if v > mejor[0]:
        mejor = (v, top, izq)

_, top, izq = mejor
crop = im.crop((izq, top, izq + ancho, top + bh)).resize(SALIDA, Image.LANCZOS)
crop.save(DESTINO, quality=84, optimize=True, progressive=True)

escala = SALIDA[0] / ancho
print("Foto %s: %s" % (num, NOMBRES.get(num, "")))
print("  recorte      %s  %s" % ("mas cerca" if cerca else "vista amplia",
                                 "(amplia %.2fx, pierde nitidez)" % escala if escala > 1
                                 else "(reduce %.2fx, se ve bien)" % escala))
print("  nitidez      %.0f" % mejor[0])
print("  guardada en  %s  (%.0f KB)" % (DESTINO, os.path.getsize(DESTINO) / 1024))
print("\nRecarga vitrina.html para verla.")
