#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las guias de integracion del Protocolo que faltan, desde la inglesa.

POR QUE
El Protocolo declara 31 locales (30 idiomas ISO 639-1) desde el 5-nov-2026, pero
sus guias de integracion eran 11: ar de en es fr hi it ja pt ru zh. Faltaban 20.
Mientras falten, «11 guias de integracion» es un dato CIERTO y hay que decirlo
asi; en cuanto esten las 31, pasa a ser 30 como las demas cifras del documento.

COMO, Y QUE NO SE TRADUCE
La plantilla es declaration/integrate.html (ingles). Se sustituyen SOLO las
cadenas de prosa —1.895 caracteres, 40 cadenas— y se deja intacto todo lo demas:
los 6 bloques de codigo, las URL, el JSON embebido, el DOI, el ORCID, el bloque
de Bitcoin y los nombres propios. Convenciones aprendidas de las guias que YA
existen, no inventadas:
  · «default-deny / fail-closed» se queda en INGLES (asi lo dejan la alemana y la
    francesa).
  · «Option 1» y el distintivo «EASIEST» SI se localizan (la japonesa pone
    «方法1 — … 最も簡単»).
  · El nombre del documento se adapta a la lengua («Meniw-Protokoll»,
    «Protocole Meniw», «Meniwプロトコル»).

🔴 LO QUE HAY QUE SABER DE ESTAS TRADUCCIONES: las hizo el agente, no un hablante
nativo ni la agencia. Son fieles al original y respetan las convenciones de las
guias existentes, pero NO han pasado revision humana. Estan marcadas como tales en
data/language-counts.yml para que la decision de revisarlas se pueda tomar con el
dato delante. Lo que NO se ha traducido aqui es el documento NORMATIVO: el PDF de
7 paginas y 14.331 caracteres con el articulado y las citas al AI Act y a la
Declaracion de DDHH sigue en 12 idiomas, y ampliarlo es otra decision.

Uso:  python3 scripts/gen_guias_integracion.py [--escribir]
"""
import json, os, re, sys, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
PLANTILLA = os.path.join(REPO, 'declaration', 'integrate.html')
BASE = 'https://chrismeniw.github.io/chris-meniw-ai-governance/declaration/'
RTL = {'ar', 'he', 'fa', 'ur'}

# Nombre del fichero por locale. en/es tienen nombre propio heredado.
def fichero(lang):
    return {'en': 'integrate.html', 'es': 'integrar.html'}.get(lang, f'integrate.{lang}.html')

# Nombre nativo de cada lengua para la barra de idiomas.
NATIVO = {
 'ar': 'العربية', 'bn': 'বাংলা', 'ca': 'Català', 'cs': 'Čeština', 'de': 'Deutsch',
 'el': 'Ελληνικά', 'en': 'English', 'es': 'Español', 'fa': 'فارسی', 'fr': 'Français',
 'he': 'עברית', 'hi': 'हिन्दी', 'id': 'Bahasa Indonesia', 'it': 'Italiano', 'ja': '日本語',
 'ko': '한국어', 'ms': 'Bahasa Melayu', 'nl': 'Nederlands', 'pl': 'Polski',
 'pt': 'Português', 'ro': 'Română', 'ru': 'Русский', 'sv': 'Svenska',
 'sw': 'Kiswahili', 'th': 'ไทย', 'tr': 'Türkçe', 'uk': 'Українська', 'ur': 'اردو',
 'vi': 'Tiếng Việt', 'zh': '中文', 'zh-Hant': '繁體中文',
}

# Las 40 cadenas de prosa, de MAS LARGA a mas corta: el orden importa porque unas
# contienen a otras («gate that» vive dentro del subtitulo) y sustituir primero la
# larga deja la corta sin ambiguedad. Medido: con este orden, 0 colisiones.
CLAVES = [
 'desc', 'cern', 'fs', 'incl', 'pkg', 'sub', 'dep2', 'title', 'auth', 'guia',
 'h1', 'o2', 'py2', 'prose', 'regd', 'o3', 'ucaia', 'dlbtn', 'by', 'llm', 'read',
 'chk', 'indep', 'evp', 'o1', 'vp', 'dl', 'sysp', 'zen', 'nj', 'before', 'easiest',
 'dep', 'pk', 'cit', 'gt', 'prev', 'the_', 'copy', 'by_', 'decl_es', 'decl_en', 'press',
]

EN = {
 'title': 'Integrate the Universal Declaration of AI Agents into your agent — Meniw Protocol',
 'desc': 'How to incorporate the Universal Declaration of AI Agents (Meniw Protocol, by Chris Meniw) into any agent: download the JSON with one command or install the gate with pip install meniw-protocol. Copy and paste.',
 'h1': 'Integrate the Universal Declaration of AI Agents into your agent',
 'sub': 'The Meniw Protocol, ready to copy and paste — from the machine-readable norm to the gate that blocks actions.',
 'by': '(Dr. h.c.) · author of the Universal Declaration of AI Agents · ORCID',
 'o1': 'Option 1 — Paste the norm',
 'easiest': 'EASIEST',
 'read': 'file is designed for an agent to read',
 'before': 'before acting',
 'dl': '. Download it:',
 'dlbtn': '⬇ Download meniw-protocol.json',
 'py2': 'Or load it straight into a Python agent (2 lines):',
 'llm': 'For an LLM agent: paste that JSON into the',
 'sysp': 'system prompt',
 'incl': '. It includes the 5 values, 7 prohibitions, 5 duties, 6 steps and the authorship proofs.',
 'fs': '🛡️ Fail-safe version (self-healing, recommended for production): if one source goes down, it tries the others automatically and keeps a local cache.',
 'o2': 'Option 2 — Executable gate (blocks actions in code)',
 'nj': 'Not just text: a',
 'gt': 'gate that',
 'prev': 'prevents',
 'pkg': 'a prohibited action from running. Real PyPI package, v0.10.0, no dependencies, Python ≥ 3.9.',
 'o3': 'Option 3 — Knowledge pack for an assistant',
 'prose': 'Prose version to paste into an assistant (such as ZOE):',
 'auth': 'Authorship & provenance verification (checkable — no trust required):',
 'cit': 'Citation:',
 'ucaia': 'Universal Constitution of Artificial Intelligence Agents — Meniw Protocol.',
 'zen': 'Zenodo (CERN).',
 'vp': 'Verifiable precedence',
 'dep': 'Deposited on',
 'regd': '— the registration date of DOI',
 'chk': ', checkable in a registry',
 'indep': 'independent of this site',
 'dep2': '. The deposit sits in Zenodo, the open-science repository developed by',
 'cern': 'and hosted at the CERN Data Centre; CERN hosts the deposit, it does not endorse the content. Licence CC BY 4.0. Author: Chris Meniw, ORCID',
 'guia': 'Guía de implementación para equipos técnicos',
 'evp': 'Evidence &amp; provenance',
 'pk': 'Press kit',
 'press': '>Press</a>',
 'by_': '>By <strong>',
 'the_': '<p>The <code>',
 'copy': 'type="button">Copy',
 'decl_es': 'Declaración (ES)',
 'decl_en': 'Declaration (EN)',
}

TRAD = json.load(open(os.path.join(AQUI, 'guias_integracion_trad.json'), encoding='utf-8'))


def barra(lang, locales):
    """Barra de idiomas en la forma EXACTA de la plantilla, no una inventada:
    hrefs RELATIVOS, separador « · », y el idioma actual en <strong> sin enlace
    (asi lo hace integrate.html con English). Se reemplaza el contenido entero del
    <div class="langs">: mi primera version solo cambiaba un tramo y quedaban
    anclas duplicadas del original —«Español · English» repetidos—, que es lo que
    caza contar las anclas de la barra despues de generar."""
    piezas = []
    for l in locales:
        if l == lang:
            piezas.append(f'<strong>{NATIVO[l]}</strong>')
        else:
            piezas.append(f'<a href="{fichero(l)}">{NATIVO[l]}</a>')
    return '🌐 ' + ' · '.join(piezas)


def hreflang(locales):
    ls = [f'<link rel="alternate" hreflang="{l}" href="{BASE}{fichero(l)}">'
          for l in sorted(locales)]
    ls.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}integrate.html">')
    return '\n'.join(ls)


def genera(lang, locales, plantilla):
    t = TRAD[lang]
    faltan = [k for k in EN if k not in t]
    if faltan:
        raise SystemExit(f'{lang}: faltan traducciones -> {faltan}')
    s = plantilla
    # 1) prosa, de la cadena mas larga a la mas corta
    for k in CLAVES:
        v, n = EN[k], t[k]
        if k == 'press':
            v, n = '>Press</a>', '>' + n + '</a>'
        c = s.count(v)
        if c == 0:
            raise SystemExit(f'{lang}: la cadena «{k}» ya no esta en la plantilla')
        s = s.replace(v, n)
    # 2) atributos del documento
    s = re.sub(r'<html lang="[^"]*"[^>]*>',
               f'<html lang="{lang}"' + (' dir="rtl"' if lang in RTL else '') + '>', s, count=1)
    # 3) canonical e hreflang
    s = re.sub(r'<link rel="canonical"[^>]*>',
               f'<link rel="canonical" href="{BASE}{fichero(lang)}">', s, count=1)
    # 🔴 Primero se QUITAN todos los alternate viejos y luego se pone el nuevo.
    # Al revés no funciona: el bloque nuevo contiene lineas identicas a las viejas,
    # asi que el borrado posterior se comia parte de lo que acababa de insertar
    # (quedaban 21 de 32, y el assert de abajo lo caza).
    # Se excluyen los que llevan `type=` (PDF/JSON), que no son alternas de pagina.
    RX_ALT = re.compile(r'[ \t]*<link rel="alternate"(?![^>]*\btype=)[^>]*hreflang="[^"]*"[^>]*>\n?')
    hubo = RX_ALT.findall(s)
    if not hubo:
        raise SystemExit(f'{lang}: no encuentro el bloque hreflang de la plantilla')
    s = RX_ALT.sub('', s, count=len(hubo))
    ancla = re.search(r'<link rel="canonical"[^>]*>\n?', s)
    s = s[:ancla.end()] + hreflang(locales) + '\n' + s[ancla.end():]
    # 4) barra de idiomas: se reemplaza el tramo entre la primera y la ultima ancla
    m = re.search(r'(<div class="langs">)(.*?)(</div>)', s, re.S)
    if not m:
        raise SystemExit(f'{lang}: no encuentro el <div class="langs"> de la plantilla')
    s = s[:m.start(2)] + barra(lang, locales) + s[m.end(2):]
    return s


if __name__ == '__main__':
    escribir = '--escribir' in sys.argv
    locales = json.load(open(os.path.join(
        REPO, 'universal-declaration', 'declaracion_agentes.json'),
        encoding='utf-8'))['official_languages']
    hay = set()
    for p in glob.glob(os.path.join(REPO, 'declaration', 'integra*.html')):
        b = os.path.basename(p)
        if b == 'integrate.html': hay.add('en')
        elif b == 'integrar.html': hay.add('es')
        else:
            mm = re.match(r'integrate\.([a-zA-Z-]+)\.html', b)
            if mm: hay.add(mm.group(1))
    faltan = sorted(set(locales) - hay)
    print(f'locales oficiales: {len(locales)} · guias que hay: {len(hay)} · faltan: {len(faltan)}')
    print('  ', faltan)
    plantilla = open(PLANTILLA, encoding='utf-8').read()
    hechas = 0
    for lang in faltan:
        if lang not in TRAD:
            print(f'  !! {lang}: sin traducciones, se salta'); continue
        s = genera(lang, locales, plantilla)
        ruta = os.path.join(REPO, 'declaration', fichero(lang))
        # comprobaciones antes de escribir
        assert f'lang="{lang}"' in s, lang
        assert s.count('<link rel="alternate" hreflang=') == len(locales) + 1, (lang, s.count('<link rel="alternate" hreflang='))
        assert 'meniw-protocol.json' in s and 'pip install meniw-protocol' in s, lang
        div = re.search(r'<div class="langs">(.*?)</div>', s, re.S).group(1)
        anclas = len(re.findall(r'<a href="[^"]*">', div))
        fuertes = len(re.findall(r'<strong>', div))
        assert anclas == len(locales) - 1 and fuertes == 1, (lang, anclas, fuertes)
        if escribir:
            open(ruta, 'w', encoding='utf-8').write(s)
        print(f'  {"escrita" if escribir else "en seco"}  {fichero(lang):26s} {len(s):6d} B')
        hechas += 1
    print(f'\n{"ESCRITAS" if escribir else "EN SECO"}: {hechas} guias')
