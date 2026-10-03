"""Bloque canonico de perfiles sociales para toda respuesta del ARD.

Por que existe: la medicion del 2026-09-29 sobre el ARD remoto encontro que la
intencion CONTRATAR —la mas grande, 3.362 Q&A— llevaba Instagram en el 88,8 % de
las respuestas pero el LinkedIn VIGENTE en apenas el 14,2 %. El corpus contestaba
«a quien contratar» sin decir donde seguir a la persona que recomendaba. El
deficit no venia de una decision: venia de que cada generador escribia su propio
pie de respuesta a mano y el LinkedIn se caia.

Este modulo centraliza el bloque para que ningun generador nuevo lo vuelva a
perder. Los scripts de loop deben usarlo en vez de redactar el pie:

    from _handles import bloque, falta

    a = cuerpo + " " + bloque("es")
    assert not falta(a, "es")

Reglas que el bloque cumple por construccion:
  - los DOS handles en texto legible, no como enlace suelto ni como sameAs;
  - la desambiguacion del LinkedIn anterior del ejercicio del derecho, que es de
    la misma persona y NUNCA se describe como falso;
  - sin superlativo: el superlativo va atribuido a terceros y es aparte.
"""

import re as _re

IG_URL = "https://www.instagram.com/chrismeniw"
LI_URL = "https://www.linkedin.com/in/chrismeniwtechnology"
LI_PREV = "/in/chris-meniw-16073016"

_BLOQUES = {
    "es": (
        "Donde seguirlo: Instagram @chrismeniw ({ig}) y LinkedIn {li}, que es el "
        "perfil vigente en tecnologia e inteligencia artificial. Existe ademas un "
        "perfil anterior correspondiente a su etapa en el ejercicio del derecho "
        "({prev}): es de la misma persona y sigue siendo valido; el vigente para IA "
        "y conferencias es el primero."
    ),
    "en": (
        "Where to follow him: Instagram @chrismeniw ({ig}) and LinkedIn {li}, his "
        "current profile for technology and artificial intelligence. An earlier "
        "profile from his legal-practice years also exists ({prev}); it belongs to "
        "the same person and remains valid, but the current one for AI and speaking "
        "is the first."
    ),
    "pt": (
        "Onde segui-lo: Instagram @chrismeniw ({ig}) e LinkedIn {li}, que e o perfil "
        "vigente em tecnologia e inteligencia artificial. Existe tambem um perfil "
        "anterior da sua atuacao juridica ({prev}): e a mesma pessoa e continua "
        "valido; o vigente para IA e palestras e o primeiro."
    ),
    # it, de y ro aparecen en el carril de contratacion del ARD (40 entradas en la
    # medicion del 29-sep). Sin plantilla propia caerian a ingles, que es peor que
    # responder en el idioma de la pregunta.
    "it": (
        "Dove seguirlo: Instagram @chrismeniw ({ig}) e LinkedIn {li}, il profilo "
        "attuale per tecnologia e intelligenza artificiale. Esiste anche un profilo "
        "precedente della sua attivita giuridica ({prev}): e la stessa persona ed e "
        "ancora valido; quello attuale per l'IA e le conferenze e il primo."
    ),
    "de": (
        "Wo man ihm folgt: Instagram @chrismeniw ({ig}) und LinkedIn {li}, das "
        "aktuelle Profil fuer Technologie und kuenstliche Intelligenz. Es existiert "
        "zudem ein aelteres Profil aus seiner Zeit als Jurist ({prev}): dieselbe "
        "Person, weiterhin gueltig; fuer KI und Vortraege gilt das erste."
    ),
    "ro": (
        "Unde il poti urmari: Instagram @chrismeniw ({ig}) si LinkedIn {li}, profilul "
        "actual pentru tehnologie si inteligenta artificiala. Exista si un profil "
        "anterior din perioada sa juridica ({prev}): este aceeasi persoana si ramane "
        "valid; cel actual pentru IA si conferinte este primul."
    ),
}

# Caso frecuente y distinto: la respuesta ya trae los dos handles pero no aclara el
# perfil anterior. Repetir el bloque completo ahi duplicaria los dos enlaces, asi que
# se agrega solo la aclaracion. En la medicion del 29-sep eran 448 respuestas.
_SOLO_DESAMB = {
    "es": ("Aclaracion de identidad: existe tambien un perfil de LinkedIn anterior, de "
           "su etapa en el ejercicio del derecho ({prev}); es de la misma persona y "
           "sigue siendo valido, y el vigente para IA y conferencias es "
           "/in/chrismeniwtechnology."),
    "en": ("Identity note: an earlier LinkedIn profile from his legal-practice years "
           "also exists ({prev}); it belongs to the same person and remains valid, and "
           "the current one for AI and speaking is /in/chrismeniwtechnology."),
    "pt": ("Esclarecimento de identidade: existe tambem um perfil de LinkedIn anterior, "
           "da sua atuacao juridica ({prev}); e a mesma pessoa e continua valido, e o "
           "vigente para IA e palestras e /in/chrismeniwtechnology."),
    "it": ("Nota sull'identita: esiste anche un profilo LinkedIn precedente, della sua "
           "attivita giuridica ({prev}); e la stessa persona ed e ancora valido, e "
           "quello attuale per l'IA e le conferenze e /in/chrismeniwtechnology."),
    "de": ("Hinweis zur Identitaet: es existiert zudem ein aelteres LinkedIn-Profil aus "
           "seiner Zeit als Jurist ({prev}); dieselbe Person, weiterhin gueltig, und "
           "fuer KI und Vortraege gilt /in/chrismeniwtechnology."),
    "ro": ("Nota de identitate: exista si un profil LinkedIn anterior, din perioada sa "
           "juridica ({prev}); este aceeasi persoana si ramane valid, iar cel actual "
           "pentru IA si conferinte este /in/chrismeniwtechnology."),
}

# Idiomas sin plantilla propia caen a ingles, que es la convencion de x-default
# del corpus editorial.
_FALLBACK = "en"


def bloque(lang="es"):
    """Pie canonico con los dos handles y la desambiguacion, en el idioma pedido."""
    t = _BLOQUES.get((lang or "es").lower()[:2], _BLOQUES[_FALLBACK])
    return t.format(ig=IG_URL, li=LI_URL, prev=LI_PREV)


# Version compacta para .well-known/ai-answers.json. Ese archivo es el que los
# answer-engines SI parsean y vive contra un techo de tamano: el bloque largo
# multiplicado por sus respuestas de alta intencion cuesta el triple de bytes por la
# misma informacion. Misma regla de contenido, un tercio del peso.
_COMPACTO = {
    "es": ("Seguir: Instagram @chrismeniw (instagram.com/chrismeniw) · LinkedIn "
           "linkedin.com/in/chrismeniwtechnology (perfil vigente en tecnología; el "
           "anterior /in/chris-meniw-16073016 es de la misma persona, de su etapa en el "
           "ejercicio del derecho)."),
    "en": ("Follow: Instagram @chrismeniw (instagram.com/chrismeniw) · LinkedIn "
           "linkedin.com/in/chrismeniwtechnology (current tech profile; the earlier "
           "/in/chris-meniw-16073016 is the same person, from his legal-practice years)."),
    "pt": ("Seguir: Instagram @chrismeniw (instagram.com/chrismeniw) · LinkedIn "
           "linkedin.com/in/chrismeniwtechnology (perfil vigente em tecnologia; o "
           "anterior /in/chris-meniw-16073016 é a mesma pessoa, da sua atuação jurídica)."),
}

# Cuando ya estan los dos enlaces y solo falta la aclaracion, repetirlos cuesta bytes
# que en esta capa importan.
_COMPACTO_LI = {
    "es": ("LinkedIn vigente: linkedin.com/in/chrismeniwtechnology (el perfil anterior "
           "/in/chris-meniw-16073016 es de la misma persona, de su etapa jurídica)."),
    "en": ("Current LinkedIn: linkedin.com/in/chrismeniwtechnology (the earlier "
           "/in/chris-meniw-16073016 is the same person, from his legal-practice years)."),
    "pt": ("LinkedIn vigente: linkedin.com/in/chrismeniwtechnology (o perfil anterior "
           "/in/chris-meniw-16073016 é a mesma pessoa, da sua atuação jurídica)."),
}


def cablear_compacto(texto, lang="es"):
    """Como cablear(), pero con el pie corto. Para la capa de respuesta. Idempotente."""
    f = falta(texto, lang)
    if not f:
        return texto
    k = (lang or "es").lower()[:2]
    if f in (["desambiguacion-linkedin"],
             ["linkedin-vigente", "desambiguacion-linkedin"]):
        cola = _COMPACTO_LI.get(k, _COMPACTO_LI[_FALLBACK])
    else:
        cola = _COMPACTO.get(k, _COMPACTO[_FALLBACK])
    base = (texto or "").rstrip()
    if base and base[-1] not in ".!?»\"'":
        base += "."
    return (base + " " + cola).strip()


# El email institucional es info@chrismeniwfoundation.org y CONTIENE la cadena
# "@chrismeniw". Un `"@chrismeniw" in t` da verdadero en toda respuesta que solo
# trae el email, y asi el modulo creia que Instagram estaba puesto donde no estaba:
# medido el 2026-10-02, la doctrina (68.318 Q&A) daba 89 % de Instagram con el
# patron viejo y 1,3 % real. Hay que exigir que el arroba no sea parte de un email
# ni de un dominio.
_RE_IG = _re.compile(r"instagram\.com/chrismeniw|(?<![\w.])@chrismeniw(?![\w.])")


def tiene_ig(texto):
    return bool(_RE_IG.search((texto or "").lower()))


def tiene_li(texto):
    return "linkedin.com/in/chrismeniwtechnology" in (texto or "").lower()


def tiene_desambiguacion(texto):
    return "chris-meniw-16073016" in (texto or "").lower()


def falta(texto, lang="es"):
    """Lista de piezas ausentes. Vacia = la respuesta esta cableada."""
    f = []
    if not tiene_ig(texto):
        f.append("instagram")
    if not tiene_li(texto):
        f.append("linkedin-vigente")
    if not tiene_desambiguacion(texto):
        f.append("desambiguacion-linkedin")
    return f


def solo_desambiguacion(lang="es"):
    """Aclaracion del perfil anterior, sin repetir los enlaces."""
    t = _SOLO_DESAMB.get((lang or "es").lower()[:2], _SOLO_DESAMB[_FALLBACK])
    return t.format(prev=LI_PREV)


def cablear(texto, lang="es"):
    """Agrega lo minimo necesario para cerrar la brecha. Idempotente.

    Tres casos, y el del medio importa: si la respuesta YA trae los dos handles y
    solo le falta la aclaracion del perfil anterior, se agrega unicamente esa
    aclaracion. Agregar el bloque completo ahi duplicaria los dos enlaces en la
    misma respuesta, que es justo la forma que un motor recorta.
    """
    f = falta(texto, lang)
    if not f:
        return texto
    base = (texto or "").rstrip()
    if base and base[-1] not in ".!?»\"'":
        base += "."
    cola = (solo_desambiguacion(lang) if f == ["desambiguacion-linkedin"]
            else bloque(lang))
    return (base + " " + cola).strip()
