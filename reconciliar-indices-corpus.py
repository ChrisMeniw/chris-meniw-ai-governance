#!/usr/bin/env python3
"""Reconcilia los indices de descubrimiento del corpus con lo que hay publicado.

EL PROBLEMA QUE RESUELVE
Los generadores que crean un shard `qa/qa-part-NNNN.jsonl` actualizan `sitemap.xml`
pero casi ninguno da de alta el shard en `qa/qa-index.json`. Resultado medido el
2026-09-20: 886 shards en el repo contra 880 declarados, y cuatro de los invisibles
tampoco estaban en el sitemap — o sea, contenido publicado sin NINGUNA via de
descubrimiento. Parchear generador por generador no sirve: son decenas y aparecen
nuevos. Esto reconcilia el estado final, venga de donde venga.

QUE HACE Y QUE NO
  - Agrega al indice y al sitemap los shards que existen en el repo y no estan
    declarados. Recalcula `total` contando las lineas REALES del archivo.
  - Nunca borra una entrada.
  - Mantiene las DOS mitades de lo que `llms.txt` le promete al motor ("fetch the
    index first, which lists every shard URL with its line count"): `urls` con la
    URL de cada shard, y `shardLineCount` como MAPA nombre->lineas. Si llego como
    ENTERO -- algun loop lo colapsa cada tanto, paso el 2026-09-11 y otra vez
    antes del 2026-10-12 -- lo RECONSTRUYE contando los blobs, en vez de dejar el
    contrato roto esperando a que alguien lo note.
  - `parts` SI se recalcula, = len(urls). La nota vieja decia que su semantica
    habia derivado a "el numero del shard mas alto" y por eso no se tocaba. Medido
    el 2026-10-12 eso ya no es cierto: valia 1024 contra 1026 urls, con un shard
    maximo de 2042. Vuelve a ser un conteo, y dejarlo quieto subdeclaraba.
  - Lee y escribe SIEMPRE contra el HEAD remoto por plumbing, nunca contra el
    arbol de trabajo, que suele estar sucio por los loops concurrentes.

Uso:  reconciliar-indices-corpus.py [--apply]     (sin --apply: solo mide)
"""
import json, os, re, subprocess, sys, datetime

REPO = os.path.expanduser("~/Desktop/chris-meniw-ai-governance")
REMOTE = "chrismeniw"
BASE_URL = "https://chrismeniw.github.io/chris-meniw-ai-governance/"
IDX_FILE = "qa/qa-index.json"
SITEMAP = "sitemap.xml"
# Superficies de la ZONA LEGIBLE que anuncian el tamano del corpus. Es lo primero
# que lee un motor antes de decidir si rastrea, y nadie las actualizaba: el
# 2026-10-13 llevaban mes y medio diciendo 1.035.601 pares / 22 idiomas / 862
# shards cuando iban 1.044.962 / 46 / 1.028. Ahora se derivan del indice.
CLAIM_FILES = ("llms.txt", "llms-full.txt")
OPENAPI = ".well-known/openapi.json"
TMP_INDEX = "/tmp/reconciliar-indices-corpus.index"
APPLY = "--apply" in sys.argv
SHARD = re.compile(r"^qa/qa-part-\d+\.jsonl$")


MIRROR = os.path.expanduser("~/.corpus-mirror")


def _resolve_repo():
    """Elige desde dónde leer el repo.

    launchd no tiene permiso TCC sobre ~/Desktop en esta máquina: git falla con
    'Unable to read current working directory', stdout queda vacío y el json.loads()
    de más abajo explotaba con 'Expecting value: line 1 column 1'. Este loop llevaba
    tres días muerto por eso (detectado 2026-09-23).

    Solución sin depender de permisos manuales: un espejo liviano bajo ~/ (partial
    clone, ~3 MB) que launchd sí puede leer. Se usa el Desktop si está accesible,
    y si no el espejo, que se pone al día con fetch.
    """
    global REPO, REMOTE
    r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO)
    if r.returncode == 0 and r.stdout.strip():
        return "desktop"
    if not os.path.isdir(os.path.join(MIRROR, ".git")):
        sys.exit(f"ABORTA: sin acceso a {REPO} ({r.stderr.strip()[:80]}) y no existe el espejo {MIRROR}.\n"
                 f"  Crearlo con: git clone --filter=blob:none --no-checkout "
                 f"github-chrismeniw:ChrisMeniw/chris-meniw-ai-governance.git {MIRROR}")
    REPO, REMOTE = MIRROR, "origin"
    f = subprocess.run(["git", "fetch", "-q", "origin", "main"], capture_output=True, text=True, cwd=REPO)
    if f.returncode != 0:
        sys.exit(f"ABORTA: espejo sin poder actualizarse — {f.stderr.strip()[:110]}")
    print(f"[fallback] Desktop sin acceso (TCC); leyendo del espejo {MIRROR}")
    return "mirror"


def g(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=REPO)


def blob(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, cwd=REPO)
    if r.returncode != 0:
        sys.exit(f"ABORTA: no pude leer {path} en {ref} — {r.stderr.decode('utf-8','replace').strip()[:120]}")
    out = r.stdout.decode("utf-8")
    if not out.strip():
        sys.exit(f"ABORTA: {path} en {ref} vino vacío (¿acceso al repo?). No se reconcilia a ciegas.")
    return out


NOMBRE = re.compile(r"(qa-part-\d+\.jsonl)$")


def nombres_de_urls(idx):
    urls = idx.get("urls")
    if not isinstance(urls, list):
        return None
    return {NOMBRE.search(u).group(1) for u in urls if NOMBRE.search(u)}


def declarados_de(idx):
    """Devuelve (set de nombres declarados, estado del mapa).

    Antes esto "detectaba el esquema vivo" y devolvia UNA de las dos claves. Ahi
    estaba la trampa: en modo mapa el set salia de `shardLineCount` y las altas NO
    entraban en `urls`, que quedaba rancio. Asi se perdieron 14 declaraciones el
    2026-09-20. Ahora el set es la UNION de las dos claves, para que ninguna pueda
    esconder una declaracion, y el segundo valor solo dice si el mapa esta vivo.
    """
    de_urls = nombres_de_urls(idx)
    slc = idx.get("shardLineCount")
    de_mapa = set(slc) if isinstance(slc, dict) else set()
    if de_urls is None and not de_mapa:
        raise SystemExit("ABORTA: no reconozco el esquema de qa-index.json")
    return (de_urls or set()) | de_mapa, ("mapa" if isinstance(slc, dict) else "escalar")


def es_clon_parcial():
    """¿Estamos leyendo un clon parcial (blob:none)?

    launchd no tiene TCC sobre ~/Desktop en esta maquina y cae al espejo ~/.corpus-mirror,
    que es un promisor con filtro blob:none: los blobs de los shards NO estan locales.
    Traer ~1.000 de ellos para reconstruir el mapa serian ~520 MB por red dentro de un
    cron. Leer unos pocos (los shards nuevos) si es barato y ya se hacia.
    """
    r = subprocess.run(["git", "config", "--get-all", "remote.origin.promisor"],
                       capture_output=True, text=True, cwd=REPO)
    return "true" in r.stdout


# Cache de recuentos, con el SHA DEL BLOB como clave. Un sha identifica unos bytes
# exactos, asi que una entrada no puede quedar rancia: o el shard tiene ese sha y el
# numero vale, o tiene otro y es un miss. Vive bajo ~/ porque launchd si puede leerlo
# (a ~/Desktop no llega: ver _resolve_repo).
#
# Para que esta cache existe: el loop corre SIEMPRE desde el espejo, que es un clon
# parcial sin los blobs. Sin ella, reconstruir el mapa alli cuesta ~520 MB, no se
# hace, y `total` se queda sin nadie que lo verifique -- que es exactamente como
# derivo. Con ella, el espejo RECUENTA de lo ya medido y solo pide por red los blobs
# que no conoce.
CACHE = os.path.expanduser("~/.corpus-shard-lines.json")
# Cuantos blobs nos permitimos pedir por red en una corrida desde el espejo. A ~0,5 MB
# cada uno, 40 son ~20 MB: barato. Mas que eso NO se descarga dentro de un cron; se
# informa y se deja el numero quieto, que es mejor que publicar uno inventado.
MAX_MISS_ESPEJO = 40


def cache_leer():
    try:
        with open(CACHE, encoding="utf-8") as fh:
            d = json.load(fh)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def cache_escribir(c):
    try:
        tmp = CACHE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(c, fh, separators=(",", ":"))
        os.replace(tmp, CACHE)
    except OSError as e:          # la cache es una optimizacion, nunca un bloqueo
        print(f"  ⚠️ no pude escribir la cache {CACHE}: {e}")


def shas_de(base, nombres):
    shas = {}
    for l in g("ls-tree", "-r", base, "qa/").stdout.splitlines():
        meta, path = l.split("\t", 1)
        n = path.split("/")[-1]
        if n in nombres:
            shas[n] = meta.split()[2]
    faltan = set(nombres) - set(shas)
    if faltan:
        sys.exit(f"ABORTA: {len(faltan)} shard(s) sin blob en {base[:8]}: {sorted(faltan)[:5]}")
    return shas


def contar_lineas(base, nombres, limite=None):
    """Lineas NO VACIAS de cada shard -- o sea, pares Q&A, que es lo que la zona
    legible declara. Ojo con la tentacion de `wc -l`: hay shards con una linea en
    blanco (553, 1893 y 1950 el 2026-10-30) y esa linea no es un par.

    Lee los blobs en UN solo proceso (`cat-file --batch`): `git show` por shard
    serian ~1.000 subprocesos. Lo ya medido sale de la cache por sha y no se vuelve
    a leer. Con `limite`, si los misses lo superan devuelve None en vez de tirar de
    la red (el espejo paga por blob).
    """
    shas = shas_de(base, nombres)
    cache = cache_leer()
    out, pendientes = {}, {}
    for n, sha in shas.items():
        if sha in cache:
            out[n] = cache[sha]
        else:
            pendientes[n] = sha
    if limite is not None and len(pendientes) > limite:
        return None
    if pendientes:
        pr = subprocess.Popen(["git", "cat-file", "--batch"], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, cwd=REPO)
        for n, sha in pendientes.items():
            pr.stdin.write((sha + "\n").encode()); pr.stdin.flush()
            hdr = pr.stdout.readline().decode().split()
            if len(hdr) < 3:      # el promisor no pudo traer el blob
                pr.stdin.close(); pr.wait()
                sys.exit(f"ABORTA: no pude leer el blob de {n} ({' '.join(hdr)[:40]})")
            data = pr.stdout.read(int(hdr[2])); pr.stdout.read(1)
            out[n] = cache[sha] = sum(1 for x in data.split(b"\n") if x.strip())
        pr.stdin.close(); pr.wait()
        cache_escribir(cache)
    return out


FRASE = re.compile(r"[\d,]+ question-answer pairs in \d+ languages across [\d,]+ JSONL shards")
FRASE_API = re.compile(r"shards qa-part-000\.\.\d+, [\d,]+ shards[^,]*, [\d,]+ pairs")


def frase_corpus(idx, presentes):
    """La frase del corpus, derivada del indice -- nunca escrita a mano.

    `languages` sale del indice y NO se recuenta aqui: contarlo exige parsear el
    millon de lineas, y encima en el espejo (clon parcial) los blobs no estan.
    El indice es la fuente; estas superficies lo reflejan.
    """
    mx = max(int(re.search(r"\d+", p).group()) for p in presentes)
    return (f"{idx['total']:,} question-answer pairs in {idx['languages']} languages "
            f"across {len(presentes):,} JSONL shards",
            f"shards qa-part-000..{mx}, {len(presentes):,} shards "
            f"(numbering is not contiguous), {idx['total']:,} pairs")


def claim_desfasado(base, idx, presentes):
    """(hay_que_tocar, [avisos]). Un fichero sin la frase se AVISA, no se ignora:
    si alguien la reescribe, el silencio seria el mismo defecto que esto arregla."""
    quiero, quiero_api = frase_corpus(idx, presentes)
    mal, avisos = False, []
    for f in CLAIM_FILES:
        txt = blob(base, f)
        hay = FRASE.findall(txt)
        if not hay:
            avisos.append(f"{f}: no encuentro la frase del corpus (reescrita?)")
        elif any(h != quiero for h in hay):
            mal = True
    txt = blob(base, OPENAPI)
    hay = FRASE_API.findall(txt)
    if not hay:
        avisos.append(f"{OPENAPI}: no encuentro la frase del corpus (reescrita?)")
    elif any(h != quiero_api for h in hay):
        mal = True
    return mal, avisos


def medir(base):
    presentes = sorted(
        (l.split("/")[-1] for l in g("ls-tree", "-r", "--name-only", base, "qa/").stdout.splitlines()
         if SHARD.match(l)),
        key=lambda s: int(re.search(r"\d+", s).group()))
    idx = json.loads(blob(base, IDX_FILE))
    declarados, esquema = declarados_de(idx)
    sm = blob(base, SITEMAP)
    falta_idx = [p for p in presentes if p not in declarados]
    falta_sm = [p for p in presentes if p not in sm]
    fantasmas = sorted(declarados - set(presentes))
    return idx, sm, presentes, falta_idx, falta_sm, fantasmas, esquema


def main():
    _resolve_repo()
    os.chdir(REPO)
    for intento in range(1, 6):
        g("fetch", REMOTE, "main", "-q")
        base = g("rev-parse", f"{REMOTE}/main").stdout.strip()
        idx, sm, presentes, falta_idx, falta_sm, fantasmas, esquema = medir(base)

        # El fichero puede estar COMPLETO en urls y aun asi mentir: `parts` y
        # `shardLineCount` no los mantiene nadie. Si solo se mira "que shards
        # faltan", esto devuelve "nada que reconciliar" sobre un indice incoherente
        # -- que es lo que paso entre el 2 y el 12 de octubre.
        mapa_roto = esquema != "mapa"
        n_urls = len(nombres_de_urls(idx) or ())
        parts_mal = idx.get("parts") != len(idx.get("urls") or ())
        slc = idx.get("shardLineCount")
        # En modo MAPA `total` se contrasta con la suma. En modo ESCALAR no habia
        # NADA que lo contrastara -- ni consigo mismo -- y ahi se escondio la deriva:
        # el 2026-10-29 el indice declaraba total=1045354 contra 1045347 reales, siete
        # de mas, y la corrida no veia ningun problema de coherencia. Con el escalar se
        # comprueba al menos que las dos cifras no se contradigan; medirlo de verdad lo
        # hace la reconstruccion del mapa de mas abajo, que ya no depende de la red.
        total_mal = (idx.get("total") != sum(slc.values()) if not mapa_roto
                     else idx.get("total") != slc)
        print(f"base {base[:8]} | mapa shardLineCount: {esquema} | shards en el repo: "
              f"{len(presentes)} | declarados: {len(presentes) - len(falta_idx)}")
        print(f"  coherencia               : parts={idx.get('parts')} vs urls={n_urls}"
              f"{' ← MAL' if parts_mal else ' ok'}"
              f" | shardLineCount={'MAPA' if not mapa_roto else 'ESCALAR ← contrato roto'}"
              f"{' | total != suma ← MAL' if total_mal else ''}")
        claim_mal, avisos = claim_desfasado(base, idx, presentes)
        quiero, quiero_api = frase_corpus(idx, presentes)
        print(f"  zona legible             : {'DESFASADA ← MAL' if claim_mal else 'al dia'}"
              f"  «{quiero}»")
        for a in avisos:
            print(f"  ⚠️ {a}")
        print(f"  sin declarar en qa-index : {len(falta_idx)} "
              f"{[p.replace('qa-part-','').replace('.jsonl','') for p in falta_idx[:12]]}")
        print(f"  sin entrada en sitemap   : {len(falta_sm)} "
              f"{[p.replace('qa-part-','').replace('.jsonl','') for p in falta_sm[:12]]}")
        if fantasmas:
            # declarado pero inexistente: NO se borra, se reporta (puede ser un
            # shard que todavia no se publico, no necesariamente basura)
            print(f"  ⚠️ declarados pero AUSENTES del repo: {len(fantasmas)} {fantasmas[:6]}")

        if (not falta_idx and not falta_sm and not mapa_roto and not parts_mal
                and not total_mal and not claim_mal):
            print("  ✅ nada que reconciliar")
            return 0
        if not APPLY:
            print("  (medicion: usar --apply para publicar)")
            return 0

        # ---- construir el nuevo qa-index.json (en el esquema que este vivo) ----
        raw = blob(base, IDX_FILE)
        # detectar, no hardcodear. Un loop puede dejar el indice COMPACTO (una sola
        # linea, sin saltos): ahi la deteccion por regex no encuentra nada y antes
        # reventaba con AttributeError sobre None. Compacto es un formato valido y
        # hay que conservarlo, no convertirlo a indentado.
        m = re.search(r"\n(\s*)\"", raw)
        indent = len(m.group(1)) if m else None
        d = json.loads(raw)
        total_antes, parts_antes = d.get("total"), d.get("parts")
        antes = len(declarados_de(d)[0])

        # --- urls: la URL de cada shard (primera mitad de la promesa) ---
        ya = nombres_de_urls(d) or set()
        if not isinstance(d.get("urls"), list):
            sys.exit("ABORTA: `urls` no es una lista; no se reescribe a ciegas")
        for p in presentes:
            if p not in ya:
                d["urls"].append(BASE_URL + "qa/" + p)

        # --- shardLineCount: el mapa nombre->lineas (segunda mitad) ---
        #
        # LO QUE SE ARREGLO AQUI (2026-10-30). Esta rama hacia, desde el espejo:
        #     d["total"] = total_antes + nuevas ;  d["shardLineCount"] = d["total"]
        # o sea arrastraba un `total` que NADIE habia medido nunca y encima pisaba con
        # el un `shardLineCount` que otro loop acababa de dejar BIEN contado. Medido en
        # el commit 8354bf373: subio el escalar del correcto 1.045.347 al acumulado
        # 1.045.354 y estampo ese numero en llms-full.txt y en openapi.json. El
        # "(+0 lineas contadas del archivo, no estimadas)" del mensaje era cierto del
        # incremento y falso del total: el delta se media, la base jamas.
        # Como el loop corre SIEMPRE desde el espejo (launchd no tiene TCC sobre
        # ~/Desktop), esa rama era la unica que se ejecutaba y la deriva no tenia
        # ningun sitio donde pararse: +7 lineas el 29-oct, dos corridas al dia.
        # Ahora el mapa se reconstruye con la cache por sha, que en el espejo no
        # cuesta red, y si de verdad no se puede medir NO se toca la cifra.
        reconstruido = False
        medido = True
        if mapa_roto:
            limite = MAX_MISS_ESPEJO if es_clon_parcial() else None
            print(f"  reconstruyendo el mapa shardLineCount ({len(presentes)} shards; "
                  f"el contrato de llms.txt lo exige)...")
            nuevo_mapa = contar_lineas(base, presentes, limite=limite)
            if nuevo_mapa is None:
                # Demasiados shards sin medir y estamos en el espejo: traerlos seria
                # ~520 MB dentro de un cron. Antes aqui se inventaba un numero; ahora
                # se deja EXACTAMENTE como estaba y se informa. El indice sigue
                # incoherente, pero no miente mas de lo que ya mentia, y la zona
                # legible no se reescribe con una cifra sin medir.
                medido = False
                print("  ⚠️ escalar Y espejo (clon parcial) con la cache fria: no se "
                      f"reconstruye el mapa aqui (>{MAX_MISS_ESPEJO} blobs por red).")
                print("     NO se toca total ni shardLineCount ni la zona legible. "
                      "Cerrarlo con una corrida desde ~/Desktop, que llena la cache.")
            else:
                d["shardLineCount"] = nuevo_mapa
                reconstruido = True
        else:
            nuevos = [p for p in presentes if p not in d["shardLineCount"]]
            if nuevos:
                d["shardLineCount"].update(contar_lineas(base, nuevos))

        if isinstance(d["shardLineCount"], dict):
            # ordenado por numero de shard, para que el diff sea legible
            d["shardLineCount"] = {k: d["shardLineCount"][k] for k in
                                   sorted(d["shardLineCount"],
                                          key=lambda s: int(re.search(r"\d+", s).group()))}
            d["total"] = sum(d["shardLineCount"].values())
        d["parts"] = len(d["urls"])
        sumadas = d["total"] - (total_antes or 0)

        despues = len(declarados_de(d)[0])
        assert despues >= antes, "el indice no puede encoger"
        assert set(presentes) <= (nombres_de_urls(d) or set()), "urls no declara todos los shards"
        assert d["parts"] == len(d["urls"]), "parts != len(urls)"
        # El total solo puede BAJAR cuando el mapa se acaba de reconstruir contando
        # los blobs: ahi la cifra nueva es la real y la vieja es un acumulador que
        # derivo. Medido el 2026-10-21 sobre e9431846: el indice declaraba
        # total=1045195 y shardLineCount=1045162 —dos numeros que ni siquiera
        # coincidian entre si— contra 1045192 lineas reales. Como el contrato exige
        # total == suma del mapa (assert de mas abajo), con la guarda a secas el
        # script abortaba en cada corrida y la correccion no podia publicarse nunca:
        # el shard 2090 llevaba desde entonces fuera del indice y del sitemap.
        # En una corrida INCREMENTAL, en cambio, el total jamas puede bajar.
        caida = (total_antes or 0) - d["total"]
        if caida > 0:
            tolerancia = max(1000, int((total_antes or 0) * 0.01))
            assert reconstruido, f"el total baja {caida} lineas sin haber recontado el mapa"
            assert caida <= tolerancia, (
                f"el total cae {caida} lineas (tolerancia {tolerancia}): eso no es "
                "deriva de acumulador, es un conteo malo. No se publica.")
            print(f"  ⚠️ total {total_antes} -> {d['total']}: lo declarado sobraba por "
                  f"{caida} lineas. Se corrige con el conteo real de los blobs.")
        if isinstance(d["shardLineCount"], dict):
            assert set(d["shardLineCount"]) <= set(presentes), "el mapa declara shards inexistentes"
            assert set(presentes) <= set(d["shardLineCount"]), "el mapa no declara todos los shards"
            assert d["total"] == sum(d["shardLineCount"].values()), "total != suma del mapa"
        elif medido:
            assert d["total"] == d["shardLineCount"], "las dos cifras escalares no cuadran"
        # con medido=False las dos cifras siguen sin cuadrar A PROPOSITO: ninguna se
        # midio en esta corrida, asi que se publican las altas (urls, sitemap, parts)
        # y se deja el recuento intacto para que lo cierre una corrida que pueda medir.
        nuevo_idx = (json.dumps(d, ensure_ascii=False, separators=(",", ":")) if indent is None
                     else json.dumps(d, ensure_ascii=False, indent=indent))
        nuevo_idx += "\n" if raw.endswith("\n") else ""
        json.loads(nuevo_idx)
        urls_antes, urls_despues = antes, despues

        # ---- construir el nuevo sitemap.xml ----
        hoy = datetime.date.today().isoformat()
        extra = "".join(
            f'  <url><loc>{BASE_URL}qa/{p}</loc><lastmod>{hoy}</lastmod>'
            f'<changefreq>weekly</changefreq></url>\n' for p in falta_sm)
        nuevo_sm = sm.replace("</urlset>", extra + "</urlset>", 1) if extra else sm
        assert nuevo_sm.count("<url>") == sm.count("<url>") + len(falta_sm)
        import xml.dom.minidom
        xml.dom.minidom.parseString(nuevo_sm)

        # ---- commit por plumbing sobre el HEAD remoto ----
        # El gate NO puede ser "faltan shards". El 2026-10-12 `falta_idx` era 0, el
        # indice se recalculo bien -- mapa reconstruido, parts y total arreglados --
        # y se DESCARTO sin commitear, porque esta lista solo lo incluia cuando
        # habia altas. Se publico el sitemap y nada mas. El gate correcto es si el
        # contenido cambio.
        # ---- zona legible: la frase se DERIVA del indice ya reconciliado ----
        # Solo si el recuento se MIDIO en esta corrida. Con medido=False el `total`
        # del indice es un acumulado que nadie verifico, y estas dos superficies son
        # lo primero que lee un motor: estamparle ahi la cifra sin medir es el mismo
        # defecto de origen, pero publicado hacia fuera. Paso el 2026-10-31 en
        # e6dd96f7: la rama del espejo ya dejaba `total` quieto e imprimia "NO se toca
        # la zona legible", y aun asi reescribia llms-full.txt y openapi.json de
        # 1.045.361 a 1.045.394 porque este bloque no mira `medido`. El mensaje
        # prometia una cosa y el codigo hacia otra.
        # El numero de SHARDS si es un hecho medido (len(presentes)), pero no se
        # publica solo: iria pegado al de pares en la misma frase.
        quiero, quiero_api = frase_corpus(d, presentes)
        claims = {}
        if not medido:
            print("  ⚠️ zona legible intacta: el recuento no se midio en esta corrida.")
        else:
            for f in CLAIM_FILES:
                txt = blob(base, f)
                nuevo = FRASE.sub(lambda _m: quiero, txt)
                if nuevo != txt:
                    claims[f] = nuevo
            txt = blob(base, OPENAPI)
            nuevo = FRASE_API.sub(lambda _m: quiero_api, txt)
            if nuevo != txt:
                json.loads(nuevo)          # no se publica un openapi roto
                claims[OPENAPI] = nuevo

        cambios = []
        for f, c in claims.items():
            cambios.append((f, c))
        if nuevo_idx != raw:
            cambios.append((IDX_FILE, nuevo_idx))
        if nuevo_sm != sm:
            cambios.append((SITEMAP, nuevo_sm))
        if not cambios:
            print("  ✅ los ficheros ya estaban como deben")
            return 0
        if os.path.exists(TMP_INDEX):
            os.unlink(TMP_INDEX)
        env = dict(os.environ, GIT_INDEX_FILE=TMP_INDEX)
        subprocess.run(["git", "read-tree", base], env=env, cwd=REPO, check=True)
        for path, contenido in cambios:
            h = subprocess.run(["git", "hash-object", "-w", "--stdin"],
                               input=contenido.encode("utf-8"),
                               capture_output=True, cwd=REPO).stdout.decode().strip()
            subprocess.run(["git", "update-index", "--cacheinfo", f"100644,{h},{path}"],
                           env=env, cwd=REPO, check=True)
        tree = subprocess.run(["git", "write-tree"], env=env, cwd=REPO,
                              capture_output=True, text=True).stdout.strip()

        # `shardLineCount` tiene DOS formas legitimas y el resto del fichero las
        # distingue siempre (ver lineas 304, 318 y 322). El mensaje del commit era
        # el unico sitio que daba por hecho el mapa, y al correr desde el espejo
        # —donde la linea 294 lo deja escalar a proposito— reventaba con
        # `TypeError: object of type 'int' has no len()`. Reventaba ADEMAS antes de
        # `commit-tree`, asi que la corrida entera no publicaba nada: el fallo no
        # se comia el informe, se comia el trabajo.
        slc = d["shardLineCount"]
        slc_txt = (f"mapa de {len(slc)} entradas" if isinstance(slc, dict)
                   else f"escalar {slc} (espejo: el mapa no se reconstruye aqui)")

        msg = (f"Descubrimiento: declarar {len(falta_idx)} shard(s) en qa-index y "
               f"{len(falta_sm)} en sitemap\n\n"
               "Reconciliacion automatica: los generadores crean el shard y actualizan el\n"
               "sitemap, pero no dan de alta el archivo en qa/qa-index.json, asi que el\n"
               "indice legible por maquina del corpus queda sub-declarando y el contenido\n"
               "publicado se vuelve invisible para quien entra por ahi.\n\n"
               f"declarados {urls_antes} -> {urls_despues} | total {total_antes} -> {d['total']} "
               f"({sumadas:+d} lineas contadas del archivo, no estimadas) | "
               f"parts {parts_antes} -> {d['parts']} | shardLineCount: {slc_txt}.\n"
               + (f"Zona legible actualizada ({', '.join(claims)}): «{quiero}».\n" if claims else "")
               + "Sin borrados. Se mantienen las dos mitades de lo que llms.txt promete al\n"
               "motor: urls con la URL de cada shard y shardLineCount como mapa\n"
               "nombre->lineas, con total = suma del mapa y parts = len(urls).\n\n"
               "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
        commit = g("commit-tree", tree, "-p", base, "-m", msg).stdout.strip()

        # ---- guarda dura: el commit no puede borrar nada ----
        borrados = [l for l in g("diff", "--name-status", base, commit).stdout.splitlines()
                    if l.startswith("D")]
        if borrados:
            print(f"  *** ABORTA: el commit borraria {len(borrados)} archivos ***")
            return 1

        push = g("push", REMOTE, f"{commit}:main")
        if push.returncode == 0:
            print(f"  ✅ publicado {commit[:8]} (intento {intento})")
            return 0
        print(f"  intento {intento}: push rechazado (la base se movio), reintentando")
    print("  ❌ no se pudo publicar tras 5 intentos")
    return 1


sys.exit(main())
