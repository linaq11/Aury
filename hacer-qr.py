#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera el QR de Restaurante Aury y la pieza imprimible para la mesa.

    python hacer-qr.py                        # usa la URL de abajo
    python hacer-qr.py https://otra.url/      # usa otra URL

Si cambia la URL hay que volver a correr esto Y volver a imprimir:
el QR impreso no se puede editar.

Salidas (carpeta qr/):
    aury-qr.svg          vectorial, para imprenta
    aury-qr.png          1200 px, para WhatsApp y pantalla
    aury-qr-logo.png     con el logo en el centro
    mesa-A6.html         pieza para la mesa, 4 por hoja carta
"""
import sys, os, base64
import segno
from PIL import Image

URL = sys.argv[1] if len(sys.argv) > 1 else "https://linaq11.github.io/aury-raspa/"

AQUI   = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "qr")
LOGO   = os.path.join(AQUI, "img", "logo.jpg")
os.makedirs(SALIDA, exist_ok=True)

MARRON = "#2a1206"
CREMA  = "#f8e9cf"

# error="h" recupera el 30%: es lo que permite tapar el centro con el logo
qr = segno.make(URL, error="h")

qr.save(os.path.join(SALIDA, "aury-qr.svg"), scale=10, border=4,
        dark=MARRON, light=CREMA)
qr.save(os.path.join(SALIDA, "aury-qr.png"), scale=40, border=4,
        dark=MARRON, light=CREMA)

# --- QR con el logo al centro ---
base = Image.open(os.path.join(SALIDA, "aury-qr.png")).convert("RGB")
W, H = base.size
if os.path.exists(LOGO):
    # 18% del ancho: con ECC "h" se lee sin problema
    lado = int(W * 0.18)
    logo = Image.open(LOGO).convert("RGB").resize((lado, lado), Image.LANCZOS)
    marco = int(lado * 0.10)
    placa = Image.new("RGB", (lado + marco*2, lado + marco*2), CREMA)
    placa.paste(logo, (marco, marco))
    base.paste(placa, ((W - placa.size[0])//2, (H - placa.size[1])//2))
base.save(os.path.join(SALIDA, "aury-qr-logo.png"), quality=95)
print("QR listo para:", URL)

# --- Pieza para la mesa ---
# Va el QR LISO, no el del logo. Verificado con opencv: el liso decodifica
# desde 110 px incluso borroso y girado 7 grados; el del logo se cae por
# debajo de 130 px porque el logo tapa datos. En la pieza que tiene que
# funcionar siempre, el margen vale más que la marca: el logo ya va al lado.
with open(os.path.join(SALIDA, "aury-qr.png"), "rb") as f:
    qr_b64 = base64.b64encode(f.read()).decode()

# Misma redaccion que la pieza de WhatsApp, para que el cliente lea lo
# mismo en la mesa y en el celular.
TARJETA = """
  <div class="t">
    <div class="marca">Restaurante Aury</div>
    <div class="tit">🎉 ¡Raspa, gana<br>y acumula!</div>
    <div class="cuerpo">¡Tienes un raspado cada d&iacute;a! Descubre cu&aacute;ntos puntos
      te llevas y sorpr&eacute;ndete con los premios que pueden aparecer. 🎁</div>
    <img class="qr" src="data:image/png;base64,{qr}" alt="Codigo QR">
    <div class="pie">Apunta la c&aacute;mara del celular</div>
    <div class="min">⭐ &iexcl;Acumula 20 puntos y el almuerzo va por cuenta de la casa!</div>
  </div>
"""

HTML = """<!DOCTYPE html>
<html lang="es-CO"><head><meta charset="utf-8">
<title>Aury - pieza para la mesa</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Public+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  @page {{ size: letter; margin: 8mm; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:"Public Sans",sans-serif; background:#fff; }}
  .hoja {{ display:grid; grid-template-columns:1fr 1fr; gap:4mm; }}
  .t {{
    border:1.4px dashed #c8b89c; border-radius:5mm;
    padding:8mm 6mm; text-align:center;
    background:#f8e9cf; color:#2a1206;
    display:flex; flex-direction:column; align-items:center;
    height:134mm; justify-content:center;
    page-break-inside:avoid;
  }}
  .marca {{ font-family:"Bricolage Grotesque",sans-serif; font-weight:800;
    font-size:10pt; letter-spacing:.16em; text-transform:uppercase; color:#d8362a; }}
  .tit {{ font-family:"Bricolage Grotesque",sans-serif; font-weight:800;
    font-size:18pt; line-height:1.1; letter-spacing:-.02em; margin:3mm 0 2.5mm; }}
  .cuerpo {{ font-size:8.4pt; line-height:1.4; color:#4a2812; margin:0 2mm 4mm;
    max-width:62mm; }}
  .qr {{ width:48mm; height:48mm; display:block; }}
  .pie {{ font-size:9.5pt; font-weight:600; margin-top:4mm; color:#4a2812; }}
  .min {{ font-size:8.4pt; line-height:1.45; margin-top:3mm; color:#6b4a2e;
    max-width:58mm; }}
  .nota {{ margin-top:6mm; font-size:8pt; color:#999; text-align:center; }}
  @media print {{ .nota {{ display:none; }} }}
</style></head><body>
<div class="hoja">{tarjetas}</div>
<div class="nota">Imprime en papel grueso, recorta por la linea y pon una en cada mesa.
URL del QR: {url}</div>
</body></html>
"""

with open(os.path.join(SALIDA, "mesa-A6.html"), "w", encoding="utf-8") as f:
    f.write(HTML.format(
        tarjetas="".join(TARJETA.format(qr=qr_b64) for _ in range(4)),
        url=URL))

print("Archivos en:", SALIDA)
for n in sorted(os.listdir(SALIDA)):
    print("  ", n, "{:,} bytes".format(os.path.getsize(os.path.join(SALIDA, n))))
