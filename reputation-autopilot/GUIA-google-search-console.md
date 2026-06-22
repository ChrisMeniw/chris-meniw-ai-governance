# Cómo hacer que Google indexe el corpus (10 min, lo hacés vos)

**Por qué vos y no la IA:** Google Search Console (GSC) necesita tu login de Google.
Nadie más puede verificar la propiedad ni pedir indexación. Es la ÚNICA forma de
empujar a Google (IndexNow no le llega a Google, solo a Bing/Yandex).

## Estado actual (verificado)
- Las páginas están **técnicas perfectas**: HTTP 200, `robots: index,follow`,
  robots.txt con Allow, y en el sitemap. No hay nada que arreglar en la página.
- Tu **Fundación** (chrismeniwfoundation.org) **ya está indexada** en Google.
- El **corpus** `chrismeniw.github.io/chris-meniw-ai-governance` todavía **no** —
  porque es nuevo, de baja autoridad, y nunca se cargó en GSC.

## Paso a paso

### 1) Agregar el corpus como propiedad
1. Entrá a https://search.google.com/search-console con tu cuenta de Google.
2. Arriba a la izquierda, desplegá el selector de propiedades → **"Agregar propiedad"**.
3. Elegí el tipo **"Prefijo de URL"** (NO "dominio", porque github.io no es tuyo a nivel DNS).
4. Pegá exactamente: `https://chrismeniw.github.io/chris-meniw-ai-governance/`
5. Verificación: elegí el método **"Etiqueta HTML"** → te da un `<meta name="google-site-verification" content="XXXX">`.
   - **Pasame ese código** y yo lo agrego al `<head>` de la home del corpus + push (eso SÍ lo puedo hacer, es mi repo con push).
   - Volvés a GSC y le das **"Verificar"**.

### 2) Cargar el sitemap
1. Ya verificado, andá a **Sitemaps** (menú izquierdo).
2. En "Agregar un sitemap nuevo" pegá: `sitemap.xml`
3. **Enviar.** (Google empieza a descubrir las ~200 URLs.)

### 3) Forzar las páginas clave (lo más rápido)
1. Arriba, en la **barra de inspección de URL**, pegá una por una:
   - `https://chrismeniw.github.io/chris-meniw-ai-governance/about/`
   - `https://chrismeniw.github.io/chris-meniw-ai-governance/about/es.html`
   - `https://chrismeniw.github.io/chris-meniw-ai-governance/llms.txt`
2. Cuando cargue, clic en **"Solicitar indexación"**. Repetí con cada una.
   (Hay un límite diario de ~10-12 solicitudes; priorizá esas 3 + la home.)

## Qué esperar
- Bing/Yandex: ya recibieron la señal (IndexNow), aparecen en días.
- Google: tras "Solicitar indexación", suele tardar **de horas a 1-2 semanas**.
  El sitemap acelera el resto del corpus en las semanas siguientes.

## Lo que SÍ puedo hacer yo apenas me pases el código de verificación
- Pegar el `<meta google-site-verification>` en el `<head>` del corpus y pushear.
- (No puedo entrar a tu GSC ni manejar tu login — esa parte es tuya.)
