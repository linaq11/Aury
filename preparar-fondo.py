#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prepara la foto de fondo para la version "Vitrina".

El original es un PNG de 2048x2048 y 5,5 MB. Eso es inservible en el celular
de un cliente con mala senal en una mesa, que es exactamente donde se abre
esta pagina. Aca se recorta a vertical, se oscurece para que el texto blanco
tenga contraste encima, y se saca:

    img/fondo.jpg        ~1080x1440, el que se usa
    img/fondo-mini.jpg   24px, se incrusta en el HTML como placeholder
                         para que haya algo caliente en pantalla al instante

    python preparar-fondo.py
"""
import os, base64, io
from PIL import Image, ImageEnhance

ORIGEN = (r"C:\Users\linaq\Downloads\restaurante-instagram\Fotos\equipo"
          r"\EDITADAS\7-Plato-primer-plano.png")
AQUI = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(AQUI, "img")
os.makedirs(IMG, exist_ok=True)

im = Image.open(ORIGEN).convert("RGB")
print("original:", im.size)

# Recorte vertical 3:4 centrado un poco arriba: el plato queda en el tercio alto,
# que es donde no lo tapan los paneles de vidrio.
W, H = im.size
objetivo = 3 / 4
if W / H > objetivo:
    nw = int(H * objetivo)
    izq = (W - nw) // 2
    im = im.crop((izq, 0, izq + nw, H))
else:
    nh = int(W / objetivo)
    arriba = int((H - nh) * 0.30)
    im = im.crop((0, arriba, W, arriba + nh))

im = im.resize((1080, 1440), Image.LANCZOS)

# Oscurecer y bajar saturacion: el fondo es fondo. Sin esto, el texto claro
# encima no llega al minimo de contraste y la comida compite con la boleta.
im = ImageEnhance.Brightness(im).enhance(0.46)
im = ImageEnhance.Color(im).enhance(0.86)

im.save(os.path.join(IMG, "fondo.jpg"), quality=72, optimize=True, progressive=True)
print("fondo.jpg     ", im.size, "{:,} bytes".format(os.path.getsize(os.path.join(IMG,"fondo.jpg"))))

mini = im.resize((18, 24), Image.LANCZOS)
mini.save(os.path.join(IMG, "fondo-mini.jpg"), quality=40)
buf = io.BytesIO(); mini.save(buf, format="JPEG", quality=40)
b64 = base64.b64encode(buf.getvalue()).decode()
print("fondo-mini     18x24  {:,} bytes".format(len(b64)))
print()
print("Pegar en el CSS de vitrina.html como placeholder:")
print("data:image/jpeg;base64," + b64)
