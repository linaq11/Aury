#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Arma la imagen para mandar por WhatsApp a los clientes cuando pagan.

    python hacer-pieza-whatsapp.py

Saca qr/whatsapp.jpg (1080x1350, formato 4:5).

OJO CON ALGO IMPORTANTE: si la clienta recibe esto EN SU CELULAR, no
puede escanear el QR con ese mismo celular. Por eso la pieza lleva el
link escrito, y el mensaje de WhatsApp debe llevarlo tambien como texto
para que sea tocable. El QR de la imagen sirve para cuando se la
reenvian a otra persona o la ven en otra pantalla.
"""
import os
import segno
from PIL import Image, ImageDraw, ImageFont

URL      = "https://linaq11.github.io/Aury/"
URL_VIS  = "linaq11.github.io/Aury"
AQUI     = os.path.dirname(os.path.abspath(__file__))
SALIDA   = os.path.join(AQUI, "qr", "whatsapp.jpg")
LOGO     = os.path.join(AQUI, "img", "logo.jpg")
os.makedirs(os.path.join(AQUI, "qr"), exist_ok=True)

W, H    = 1080, 1350
NOCHE   = (0x15, 0x15, 0x1a)
CREMA   = (0xf8, 0xe9, 0xcf)
NARANJA = (0xf4, 0x94, 0x0a)
TINTA   = (0xf7, 0xf6, 0xf1)
MARRON  = (0x2a, 0x12, 0x06)

F = "C:/Windows/Fonts/"
def fuente(nombre, tam):
    return ImageFont.truetype(F + nombre, tam)

negra  = lambda t: fuente("ariblk.ttf", t)      # titulares
semi   = lambda t: fuente("seguisb.ttf", t)     # apoyos
normal = lambda t: fuente("segoeui.ttf", t)     # texto
emoji  = lambda t: fuente("seguiemj.ttf", t)    # emojis a color

im = Image.new("RGB", (W, H), NOCHE)
d  = ImageDraw.Draw(im)

def centrado(y, txt, f, color, espaciado=0):
    if espaciado:
        ancho = sum(d.textlength(c, font=f) + espaciado for c in txt) - espaciado
        x = (W - ancho) / 2
        for c in txt:
            d.text((x, y), c, font=f, fill=color)
            x += d.textlength(c, font=f) + espaciado
    else:
        d.text((W/2, y), txt, font=f, fill=color, anchor="ma")

# ---- logo ----
if os.path.exists(LOGO):
    lado = 150
    logo = Image.open(LOGO).convert("RGB").resize((lado, lado), Image.LANCZOS)
    mask = Image.new("L", (lado*4, lado*4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, lado*4, lado*4), fill=255)
    mask = mask.resize((lado, lado), Image.LANCZOS)
    aro = Image.new("RGB", (lado+10, lado+10), NARANJA)
    m2 = Image.new("L", ((lado+10)*4, (lado+10)*4), 0)
    ImageDraw.Draw(m2).ellipse((0, 0, (lado+10)*4, (lado+10)*4), fill=255)
    im.paste(aro, ((W-lado-10)//2, 70), m2.resize((lado+10, lado+10), Image.LANCZOS))
    im.paste(logo, ((W-lado)//2, 75), mask)

# ---- titulares ----
# Redaccion de Lina. Los emojis van con Segoe UI Emoji y embedded_color,
# porque con la fuente de texto salen en blanco y negro.
# "premios" en plural: confirmado por Lina el 2 nov 2026, porque la
# bebida ya trae varias opciones (seis jugos y varias gaseosas).
def emo_texto(y, emo, txt, f, color, tam_emo, al_final=False):
    """Dibuja emoji + texto (o texto + emoji) centrado como un bloque."""
    fe = emoji(tam_emo)
    ae = d.textlength(emo, font=fe)
    at = d.textlength(txt, font=f)
    x = (W - (ae + 14 + at)) / 2
    dy = y + (f.size - tam_emo)//2
    if al_final:
        d.text((x, y), txt, font=f, fill=color)
        d.text((x + at + 14, dy), emo, font=fe, embedded_color=True)
    else:
        d.text((x, dy), emo, font=fe, embedded_color=True)
        d.text((x + ae + 14, y), txt, font=f, fill=color)

centrado(248, "RESTAURANTE AURY", semi(26), NARANJA, espaciado=5)
emo_texto(300, "🎉", "¡Raspa, gana", negra(60), TINTA, 52)
centrado(372, "y acumula!", negra(60), TINTA)
centrado(458, "¡Tienes un raspado cada día! Descubre", normal(27), (190, 188, 182))
centrado(494, "cuántos puntos te llevas y sorpréndete", normal(27), (190, 188, 182))
emo_texto(530, "🎁", "con los premios que pueden aparecer.", normal(27), (190, 188, 182), 26, al_final=True)

# ---- tarjeta del QR ----
TX, TY, TW_, TH_ = 232, 582, 616, 616
tarjeta = Image.new("RGB", (TW_, TH_), CREMA)
mr = Image.new("L", (TW_*4, TH_*4), 0)
ImageDraw.Draw(mr).rounded_rectangle((0, 0, TW_*4, TH_*4), radius=130, fill=255)
im.paste(tarjeta, (TX, TY), mr.resize((TW_, TH_), Image.LANCZOS))

qr = segno.make(URL, error="h")
qr.save(os.path.join(AQUI, "qr", "_tmp.png"), scale=20, border=0,
        dark="#2a1206", light="#f8e9cf")
# 500 y no 520, y subido: el rotulo de abajo quedaba a 12px del QR y le
# comia la zona de silencio. En pantalla limpia leia igual, pero un
# escaner apuntando a la pantalla de otro celular es menos indulgente.
q = Image.open(os.path.join(AQUI, "qr", "_tmp.png")).convert("RGB").resize((474, 474), Image.LANCZOS)
im.paste(q, (TX + (TW_-474)//2, TY + 54))
os.remove(os.path.join(AQUI, "qr", "_tmp.png"))

d.text((W/2, TY + 566), "Apunta la cámara", font=semi(27), fill=MARRON, anchor="ma")

# ---- el link, que es lo que de verdad sirve en WhatsApp ----
emo_texto(1222, "⭐", "¡Acumula 20 puntos y el almuerzo", semi(27), NARANJA, 26)
centrado(1258, "va por cuenta de la casa!", semi(27), NARANJA)
centrado(1300, URL_VIS, normal(25), (150, 148, 143))

im.save(SALIDA, quality=90, optimize=True, progressive=True)
print("whatsapp.jpg  %dx%d  %.0f KB" % (W, H, os.path.getsize(SALIDA)/1024))
print(SALIDA)
