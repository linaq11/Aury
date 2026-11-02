# Aury · Raspa y descubre

QR para las mesas de Restaurante Aury. El cliente escanea, rasca con el dedo,
le aparece el beneficio de la semana y se le **guarda en el celular**. Además
junta un punto por visita hasta el almuerzo gratis.

Sin servidor, sin base de datos, sin cuentas. Un archivo HTML.

---

## ⚠️ Las dos reglas que no se pueden romper

Estas dos cosas no son opinión de diseño: romperlas tiene consecuencias
concretas sobre el negocio.

### 1. Esto NO es un sorteo, y no puede volverse uno

En Colombia, un premio que decide el azar es un **juego promocional** y necesita
autorización previa. La excepción que tenían los comerciantes **fue derogada**
por el art. 94 de la Ley 1753 de 2015, y Coljuegos lo dice con esas palabras:
*"Se eliminan de la excepción contemplada en la Ley, a los comerciantes o
industriales que desarrollen juegos promocionales para impulsar sus ventas."*
Coljuegos además lista "raspa y gana" entre los métodos de azar cubiertos.

Lo que implicaría hacerlo con azar:

- Autorización previa de la **Lotería de Bolívar** (los municipales no los
  autoriza Coljuegos, los autoriza la Sociedad de Capital Público Departamental)
- **14 % del valor del plan de premios** en derechos de explotación
- No se puede publicitar antes de tener el permiso
- No hay exención por monto del premio, por tamaño del negocio, ni por ser local

Por eso el beneficio acá es **uno solo, igual para todos y anunciado de
antemano**: así no hay azar y no hay trámite. Se puede cambiar cada semana.
Lo que no se puede es poner una lista de premios y sortear cuál toca —
**ni aunque todos ganen algo**.

Fuentes: Ley 643 de 2001 arts. 5 y 31 · Ley 1753 de 2015 art. 94 ·
coljuegos.gov.co/publicaciones/301146/operadores_de_juegos_promocionales/

### 2. La reseña de Google se PIDE, nunca se PAGA

Google prohíbe expresamente ofrecer incentivos por reseñas:

> "Ofrecer incentivos, como pagos, descuentos o bienes o servicios gratuitos,
> a cambio de publicar reseñas"

Y prohíbe también el *review gating* (pedirle reseña solo a quien quedó
contento):

> "Desaconsejar o prohibir la publicación de reseñas negativas o solicitar
> reseñas positivas de clientes de forma selectiva."

La sanción no cae sobre la reseña, cae sobre **el perfil del negocio**: retiro
de reseñas, bloqueo de nuevas, aviso público de fraude en la ficha y suspensión
del perfil. Para un restaurante que vive de que lo encuentren en Google Maps,
eso es grave.

No hay umbral: un almuerzo gratis y un punto cuentan igual.

Lo que **sí** está permitido, y Google lo recomienda, es pedir la reseña a
secas, incluso con un QR. Por eso acá la reseña:

- va **después** de que el beneficio ya está guardado
- no da puntos, ni descuento, ni nada
- se le muestra **igual a todo el mundo**, sin preguntar antes si quedó contento
- lo dice en pantalla: *"tu beneficio y tus puntos no dependen de que la dejes"*

Fuente: support.google.com/contributionpolicy/answer/7400114

---

## Qué hay en la carpeta

**En vivo:** https://linaq11.github.io/Aury/
**Repo:** https://github.com/linaq11/Aury

```
index.html             la página principal (la "vitrina": foto que rota + carta)
vitrina-sin-foto.html  la misma sin la banda de comida
sobria.html            la primera versión, paleta sepia, sin foto ni carta
hacer-qr.py            genera el QR y la hoja para imprimir
preparar-platos.py     recorta las fotos de los platos para la banda
escoger-foto.py        cambia la foto de la banda
empaquetar.py          mete las imágenes dentro del html (*-PARA-VER.html)
img/logo.jpg           logo
qr/
  aury-qr.svg       vectorial, para imprenta
  aury-qr.png       para WhatsApp y pantalla
  aury-qr-logo.png  con el logo al centro — SOLO para Instagram, ver abajo
  mesa-A6.html      4 tarjetas por hoja carta, listo para imprimir
```

### Por qué la tarjeta impresa lleva el QR sin logo

Probado con opencv a varios tamaños, con desenfoque y girado 7°:

| Tamaño | Liso | Con logo |
|---|---|---|
| 90 px | pasa (falla borroso) | falla |
| 110 px | **pasa todo** | falla |
| 130 px y más | pasa todo | pasa todo |

El logo tapa datos y le quita margen. A tamaño impreso los dos sirven, pero en
la pieza que tiene que funcionar siempre el margen vale más que la marca — y el
logo ya va impreso al lado del QR. El del logo queda para stories, donde se ve
grande.

---

## Lo que hay que configurar

Todo está junto, arriba del `<script>` en `index.html`, en el bloque `CONFIG`.

| Qué | Ahora | Hay que |
|---|---|---|
| `googleReview` | **vacío** | Pegar el link de reseñas. Mientras esté vacío, la pantalla de reseña no se muestra (mejor que un botón roto). Se saca en Perfil de Empresa de Google → Inicio → "Pide reseñas" |
| `beneficio` | Jugo natural gratis | Confirmar que a Eli le cuadra el costo |
| `puntosParaAlmuerzo` | 20 | Calibrar con el margen real. Ver la calculadora del panel |
| `claveDelMes` | `2611` | **Cambiarla cada mes** |
| `vigenciaDesde` / `vigenciaHasta` | 3 nov – 31 dic 2026 | La Ley 1480 de 2011 art. 33 obliga a publicar la fecha de cierre. Sin fecha, la promoción queda vigente hasta publicar la revocatoria por el mismo medio |

---

## Cómo se usa en el restaurante

**El cliente:** escanea el QR de la mesa → rasca → le sale el beneficio de la
semana, guardado en el celular → cuando pide, se lo muestra a la cajera.

**La cajera**, en el celular del cliente:

1. Mantener pulsado el logo de arriba **3 segundos** → pide la clave del mes.
   (Son 3 segundos a propósito, para que ningún cliente lo encuentre de casualidad.)
2. **"+1 punto a este celular"**, una vez por visita. Si se toca dos veces
   seguidas, pregunta antes.
3. **"Abrir Lo mío"** y tocar el beneficio que acabó de entregar, para que quede
   marcado como usado.

El punto sale **solo** del botón de la cajera. Eso es a propósito: si los puntos
se dieran por escanear, cualquiera le toma foto al QR y acumula puntos sin pisar
el restaurante.

---

## Lo que esto NO hace, dicho de frente

- **Los puntos viven en el celular del cliente, no en un servidor.** Si borra los
  datos del navegador, cambia de celular o navega en modo privado, los pierde.
  Está escrito en los términos. Guardarlos de verdad exige pedir el celular del
  cliente y una base de datos, con todo lo que la Ley 1581 de 2012 exige encima
  (autorización previa y expresa, aviso de privacidad, canal de reclamos).
  No vale la pena todavía.
- **Un cliente mañoso puede inflarse los puntos** si sabe abrir las herramientas
  del navegador. El control real es que el almuerzo gratis se entrega en persona,
  mirando a la persona a la cara.
- **No hay reportes.** Nadie puede ver cuántos escanearon ni cuántos premios se
  entregaron. Para eso hace falta servidor.
- **No guarda ningún dato personal**, y por eso no hay que inscribir nada en el
  RNBD ni pedir consentimientos. Es una decisión, no un olvido.

---

## Si cambia la URL

El QR impreso **no se puede editar**. Si cambia la dirección hay que regenerar
y volver a imprimir:

```
python hacer-qr.py https://linaq11.github.io/Aury/
```

Por eso conviene decidir la URL definitiva **antes** de mandar a imprimir en
cantidad. Si algún día quiere dominio propio (`aury.com.co` o parecido), es el
momento de comprarlo: cuesta unos 15 dólares al año y hace que el QR impreso
sirva para siempre, sin importar dónde esté alojada la página.
