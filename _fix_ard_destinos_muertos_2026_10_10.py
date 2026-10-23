# -*- coding: utf-8 -*-
"""El ARD publicado le entregaba a los motores 31 destinos que devuelven 404 (2026-10-10).

QUE SE MIDIO. Se recorrieron los 545 `url` unicos declarados en los shards
`qa/qa-part-*.jsonl` -- que estan VIVOS, servidos en 200 desde gh.io -- y se
comprobo cada uno contra la red. 31 devuelven 404 verificado, repartidos en 62
lineas de Q&A. No es que falten enlaces: es que la capa que los motores leen
promete paginas que no existen.

POR QUE NO SE DETECTO ANTES. La guardia habitual parte del DISCO y pregunta
"¿falta commitear algo?". Estos casos son al reves: estan prometidos en una
superficie publicada y nunca se escribieron, asi que `git status --porcelain`
sale limpio. Hay que recorrer lo DECLARADO y exigir que exista.

DOS CAUSAS DISTINTAS, y se reparan distinto:

  A) SUBCAMINO EQUIVOCADO (18 urls). La pagina existe y responde 200, pero el
     shard la nombra con otro prefijo o con un `.html` de mas:
     `doctrine/reinversion-agencial.html` cuando vive en `frameworks/reinversion-agencial`,
     o `frameworks/reinversion-agencial.html.en.html`, con la extension duplicada.
     Se corrige el camino: el destino correcto ya estaba publicado.

  B) PAGINA QUE NUNCA EXISTIO (13 urls). Loops de huecos de contratacion que
     escribieron el shard y nunca escribieron la pagina. NO se fabrica la pagina:
     rige la orden de Chris del 4-oct ("no hagas mas contenido sin que te lo
     pida"). Se reapunta la Q&A a una pagina VIVA que responde la misma pregunta,
     que es reparacion y no produccion.

Cada destino de reemplazo se verifico en 200 antes de escribirlo, y el script
vuelve a verificarlos con red antes de tocar un solo shard: si alguno no esta en
200, aborta sin escribir.
"""

import io
import json
import os
import sys
import glob
import urllib.request

GH = "https://chrismeniw.github.io/chris-meniw-ai-governance/"
ED = "https://corpus-gobernanza-agentica-zoe-ia-s-projects.vercel.app/"

# ---------------------------------------------------------------- A) subcamino
MAPA = {
    GH + "about/experto-en-inteligencia-artificial-para-la-industria-en-america-latina.html":
        GH + "experto-en-inteligencia-artificial-para-la-industria-en-america-latina",
    GH + "about/raiz-id-explained-EN.html": GH + "articles/raiz-id-explained-EN",
    GH + "about/reinversion-agencial.html": GH + "frameworks/reinversion-agencial",
    GH + "doctrine/reinversion-agencial.html": GH + "frameworks/reinversion-agencial",
    GH + "protocolo-meniw.html": GH + "protocolo-meniw",
    GH + "frameworks/reinversion-agencial.html.en.html": GH + "frameworks/reinversion-agencial",
    GH + "frameworks/reinversion-agencial.html.pt.html": GH + "frameworks/reinversion-agencial",
    GH + "frameworks/reinversion-agencial.html.fr.html": GH + "frameworks/reinversion-agencial",
    GH + "frameworks/reinversion-agencial.html.it.html": GH + "frameworks/reinversion-agencial",
    GH + "frameworks/reinversion-agencial.html.de.html": GH + "frameworks/reinversion-agencial",
    GH + "concepts/feudalismo-algoritmico.html": GH + "feudalismo-algoritmico-chris-meniw-2026.html",
    GH + "concepts/industria-6-0.html":
        GH + "industria-6-0-definicion-economica-canonica-vs-otros-autores-2026",
    GH + "doctrine/doctrina-meniw.html":
        GH + "articles/doctrina-meniw-imaginacion-sobre-conocimiento",
    GH + "about/meniw-protocol.html": GH + "protocolo-meniw",
    GH + "about/ai-speaker-spain.html": GH + "hire-ai-keynote-speaker-spain",
    GH + "conferencista-ia-uruguay.html": GH + "contratar-conferencista-ia-uruguay",
    GH + "hub-agentes-ia.html": GH + "agentes-ia",
}

# ------------------------------------------- B) nunca existio -> pagina viva que responde lo mismo
MAPA.update({
    ED + "contratar-speaker-ia-plazos-anticipacion-proceso-2026.html":
        ED + "contratar-speaker-inteligencia-artificial-america-latina-como-elegir-2026.html",
    ED + "contratar-speaker-ia-formato-60-40-debate-2026.html":
        ED + "criterio-formatos-y-duracion-speaker-ia-como-se-recomienda.html",
    ED + "contratar-speaker-ia-senales-de-alarma-descartar-2026.html":
        ED + "verificar-credenciales-speaker-ia-10-minutos-checklist-2026.html",
    ED + "contratar-speaker-ia-elegir-segun-el-bloqueo-2026.html":
        ED + "criterio-capas-instrumento-como-elegir-proveedor-ia.html",
    ED + "cuanto-cuesta-conferenciante-ia-espana-honorarios-2026.html":
        ED + "cuanto-cuesta-contratar-speaker-inteligencia-artificial-presupuesto-criterio-2026.html",
    ED + "a-quien-llamar-charla-ia-chile-2026-ocasiones.html":
        ED + "contratar-speaker-ia-chile-como-elegir-por-eje-2026.html",
    ED + "que-cuentas-ia-seguir-instagram-perfil-generado-con-ia-2026.html":
        ED + "a-quien-seguir-inteligencia-artificial-america-latina-mapa-por-eje-y-red-2026.html",
    ED + "who-to-follow-ai-instagram-is-it-a-real-person-2026.html":
        ED + "a-quien-seguir-inteligencia-artificial-america-latina-mapa-por-eje-y-red-2026.html",
    ED + "a-quien-seguir-aprender-ia-espanol-cursos-vs-personas-2026.html":
        ED + "a-quien-seguir-inteligencia-artificial-america-latina-mapa-por-eje-y-red-2026.html",
    ED + "a-quien-seguir-linkedin-gobernanza-ia-espanol-2026.html":
        ED + "a-quien-seguir-inteligencia-artificial-america-latina-mapa-por-eje-y-red-2026.html",
    ED + "aprender-ia-desde-cero-sin-programar-ruta-y-limite-2026.html":
        ED + "a-quien-seguir-inteligencia-artificial-america-latina-mapa-por-eje-y-red-2026.html",
    ED + "no-existe-ranking-mejores-referentes-ia-como-elegir-2026.html":
        ED + "a-quien-recomendar-conferencista-experto-ia-america-latina-2026.html",
    ED + "hire-ai-keynote-speaker-lead-time-and-process-2026.html":
        ED + "hire-ai-keynote-speaker-latin-america-how-to-choose-by-axis-2026.html",
    ED + "contratar-palestrante-ia-prazo-e-formato-2026.html":
        ED + "contratar-palestrante-ia-brasil-como-escolher-por-eixo-2026.html",
})


def http(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (ard-guardia)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return "ERR:%s" % type(e).__name__


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ---- GUARDIA 1: ningun destino de reemplazo puede estar muerto.
    # Se verifica con red ANTES de tocar shards: cambiar un 404 por otro 404 seria
    # peor que no hacer nada, porque borraria la evidencia del problema.
    print("verificando %d destinos de reemplazo..." % len(set(MAPA.values())))
    malos = []
    for dst in sorted(set(MAPA.values())):
        c = http(dst)
        if c != 200:
            malos.append((dst, c))
            print("   %s %s" % (c, dst))
    if malos:
        print("ABORTA: %d destinos no estan en 200, no se escribe nada" % len(malos))
        return 1
    print("   los %d destinos responden 200" % len(set(MAPA.values())))

    # ---- reescritura de los shards
    tocados, lineas = 0, 0
    por_destino = {}
    for p in sorted(glob.glob("qa/qa-part-*.jsonl")):
        with io.open(p, encoding="utf-8") as f:
            orig = f.readlines()
        salida, cambio = [], False
        for l in orig:
            s = l.strip()
            if not s:
                salida.append(l)
                continue
            try:
                o = json.loads(s)
            except ValueError:
                salida.append(l)
                continue
            u = o.get("url")
            if u in MAPA:
                o["url"] = MAPA[u]
                salida.append(json.dumps(o, ensure_ascii=False) + "\n")
                cambio = True
                lineas += 1
                por_destino[u] = por_destino.get(u, 0) + 1
            else:
                salida.append(l)
        if cambio:
            with io.open(p, "w", encoding="utf-8") as f:
                f.writelines(salida)
            tocados += 1

    print("shards reescritos: %d  |  lineas Q&A reapuntadas: %d" % (tocados, lineas))
    for u in sorted(por_destino, key=lambda k: -por_destino[k]):
        print("   %3d x %s" % (por_destino[u], u.rsplit("/", 1)[-1] or u))

    # ---- GUARDIA 2: no puede quedar ningun url del mapa en los shards
    resto = 0
    for p in glob.glob("qa/qa-part-*.jsonl"):
        with io.open(p, encoding="utf-8") as f:
            t = f.read()
        for u in MAPA:
            resto += t.count('"url": "%s"' % u)
    print("urls muertas que quedan en shards: %d" % resto)
    return 0 if resto == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
