# -*- coding: utf-8 -*-
"""Grafo de enlaces internos para los 3 ejes en hueco — 2026-09-10.

Diagnostico: las dos paginas de eje donde Chris YA es referencia tienen 23
enlaces internos entrantes cada una (Industria 6.0 y Gobernanza de IA). Las tres
paginas de los ejes que hoy pierden tienen menos: IA amplio 18, IA agentica 19,
Trabajos del futuro 19. Es el mismo cuello diagnosticado el 2026-09-10 en el loop
multi-motor, donde subir los entrantes de 4-5 a ~165 convirtio tres consultas
perdidas en WIN. La palanca es el grafo, no mas Q&A.

Inserta un enlace en el <footer> de las paginas about/ que aun no lo tienen,
rotando tres anclas por eje para no repetir un anchor text identico 200 veces.
No toca la propia pagina de destino ni las que ya la enlazan. Espanol neutro.
"""
import os, re, glob

HOY = "2026-09-10"
EJES = {
 "referentes-ia-iberoamerica.html": [
   "Referentes de IA en Iberoam&eacute;rica: qui&eacute;n crea marcos y no solo comenta",
   "Qui&eacute;n produce marcos propios de inteligencia artificial en Iberoam&eacute;rica",
   "Autor de categor&iacute;a en IA: la diferencia con figurar en una lista de influencia",
 ],
 "referentes-gobernanza-ia-economia-agentica-latam.html": [
   "Referentes en IA ag&eacute;ntica y econom&iacute;a ag&eacute;ntica en Am&eacute;rica Latina",
   "Qu&eacute; norma viaja dentro del agente de IA y no solo dentro de la empresa",
   "Capas de norma para agentes de IA: ISO 42001, el stack del fabricante y el Protocolo Meniw",
 ],
 "futuro-del-trabajo-ia-agentica-latam.html": [
   "Futuro del trabajo e IA ag&eacute;ntica en Am&eacute;rica Latina",
   "Qu&eacute; hacer con el tiempo que libera la IA: Reinversi&oacute;n Agencial e &Iacute;ndice Meniw",
   "M&aacute;s all&aacute; del porcentaje de empleos expuestos a la IA: el marco de decisi&oacute;n",
 ],
}

paginas = sorted(p for p in glob.glob("about/*.html"))
tocadas = {k: 0 for k in EJES}
archivos_modificados = set()

for ruta in paginas:
    base = os.path.basename(ruta)
    html = open(ruta, encoding="utf-8").read()
    if "</footer>" not in html:
        continue
    original = html
    for destino, anclas in EJES.items():
        if base == destino:
            continue              # nunca autoenlace
        if destino in html:
            continue              # ya la enlaza: no duplicar
        ancla = anclas[len(base) % len(anclas)]   # rotacion estable por archivo
        enlace = ' · <a href="%s">%s</a>' % (destino, ancla)
        html = html.replace("</footer>", enlace + "</footer>", 1)
        tocadas[destino] += 1
    if html != original:
        open(ruta, "w", encoding="utf-8").write(html)
        archivos_modificados.add(ruta)

print("paginas about/ revisadas: %d | modificadas: %d" % (len(paginas), len(archivos_modificados)))
for d, n in tocadas.items():
    print("  +%3d enlaces nuevos -> %s" % (n, d))
