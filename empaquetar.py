#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mete las imagenes DENTRO del HTML para poder mandar un solo archivo.

    python empaquetar.py vitrina.html

Saca vitrina-PARA-VER.html, que se abre con doble clic desde cualquier
carpeta y desde el celular, sin necesitar la carpeta img/ al lado.

Es solo para mirar y compartir. La version que se publica es la normal,
con las imagenes aparte: asi el navegador las cachea y la pagina pesa
menos en la segunda visita.
"""
import sys, os, re, base64, mimetypes

if len(sys.argv) < 2:
    print("Uso: python empaquetar.py vitrina.html")
    sys.exit(1)

AQUI = os.path.dirname(os.path.abspath(__file__))
src  = os.path.join(AQUI, sys.argv[1])
if not os.path.exists(src):
    print("No existe", src)
    sys.exit(1)

html = open(src, encoding="utf-8").read()

usadas, faltantes = [], []

def incrustar(ruta):
    p = os.path.join(AQUI, ruta.replace("/", os.sep))
    if not os.path.exists(p):
        faltantes.append(ruta)
        return None
    tipo = mimetypes.guess_type(p)[0] or "image/jpeg"
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    usadas.append((ruta, os.path.getsize(p)))
    return "data:%s;base64,%s" % (tipo, b64)

# cualquier img/....jpg|png que aparezca, este en CSS, en HTML o en el JS
def cambiar(m):
    ruta = m.group(0)
    d = incrustar(ruta)
    return d if d else ruta

html = re.sub(r'img/[A-Za-z0-9_.-]+\.(?:jpg|jpeg|png|webp)', cambiar, html)

base = os.path.splitext(sys.argv[1])[0]
dest = os.path.join(AQUI, base + "-PARA-VER.html")
open(dest, "w", encoding="utf-8").write(html)

print("Incrustadas %d imagenes:" % len(set(r for r, _ in usadas)))
for r, n in sorted(set(usadas)):
    print("   %-24s %6.0f KB" % (r, n / 1024))
if faltantes:
    print("\nNO ENCONTRADAS (quedan rotas):")
    for f in sorted(set(faltantes)):
        print("   ", f)
print("\n%s  (%.0f KB)" % (dest, os.path.getsize(dest) / 1024))
print("Se abre con doble clic desde cualquier carpeta.")
