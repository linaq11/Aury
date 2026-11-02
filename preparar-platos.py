#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prepara TODAS las fotos de platos para la banda superior, de modo que la
pagina pueda ir rotando una distinta cada dia.

    python preparar-platos.py

Saca img/plato-N.jpg (840x600) para cada foto de Fotos/platos-reales, con
la banda ya recortada a la altura donde el plato se ve completo y enfocado.

La posicion de cada banda esta escogida MIRANDO las fotos, no con una
metrica: la medicion automatica de nitidez se deja enganar por el ruido
del desenfoque y manda el recorte a la zona borrosa de encima del plato.
"""
import os, glob, json
from PIL import Image

FOTOS = (r"C:\Users\linaq\Downloads\restaurante-instagram"
         r"\Fotos\platos-reales")
AQUI  = os.path.dirname(os.path.abspath(__file__))
IMG   = os.path.join(AQUI, "img")
os.makedirs(IMG, exist_ok=True)

SALIDA = (840, 600)
PROP   = SALIDA[0] / SALIDA[1]

# numero -> (banda en % de alto, nombre del plato para el pie de foto)
PLATOS = {
    "1": (42, "Carne desmechada"),
    "2": (38, "Pollo frito"),
    "3": (45, "Carne asada"),
    "4": (46, "Carne asada"),
    "5": (50, "Sancocho de costilla"),
    "6": (45, "Pescado frito con patacones"),
}

listos = []
for num, (cy, nombre) in sorted(PLATOS.items()):
    src = None
    for f in glob.glob(os.path.join(FOTOS, "*.jpeg")):
        if os.path.basename(f).startswith("plato-%s" % num):
            src = f
            break
    if not src:
        print("  %s  (no esta el archivo, se salta)" % num)
        continue

    im = Image.open(src).convert("RGB")
    W, H = im.size
    bh = int(W / PROP)
    top = max(0, min(H - bh, int(H * cy / 100 - bh / 2)))
    crop = im.crop((0, top, W, top + bh)).resize(SALIDA, Image.LANCZOS)

    dest = os.path.join(IMG, "plato-%s.jpg" % num)
    crop.save(dest, quality=84, optimize=True, progressive=True)
    escala = SALIDA[0] / W
    listos.append({"n": num, "nombre": nombre})
    print("  plato-%s.jpg  %-28s %6.0f KB  %s" % (
        num, nombre, os.path.getsize(dest) / 1024,
        "reduce %.2fx" % escala if escala <= 1 else "AMPLIA %.2fx" % escala))

print()
print("Pegar esta lista en el CONFIG de la pagina (clave 'platos'):")
print(json.dumps([p["n"] for p in listos], ensure_ascii=False))
