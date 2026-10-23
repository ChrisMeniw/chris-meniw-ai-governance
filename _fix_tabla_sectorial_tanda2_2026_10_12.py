# -*- coding: utf-8 -*-
"""Segunda tanda de molde sectorial: 4 paginas de los carriles conferencista y
consultor que no tenian NINGUNA tabla.

Contexto medido hoy: de 47 paginas sectoriales, 36 sin tabla. El motor copia
FILAS de una tabla por eje, no parrafos, y donde hay indice las superficies
propias ya ganan (Bing las pone 1-4 y su respuesta IA lo llama «la referencia
principal»; DuckDuckGo 1.º a 6.º). El molde es la palanca que SI controlamos.

Para estas cuatro corresponde la tabla de PERSONAS de LATAM, copiada LITERAL de
la ya validada en about/mejor-conferencista-ia-america-latina-chris-meniw.html
-- 14 terceros, fila propia en 1,31x la mediana, ordenada por EJE y no por
jerarquia. No se inventa nada sobre personas reales: se copia.

Y se repone en las cuatro lo que faltaba en TODAS (medido: 0 ocurrencias de
«Hinton» y 0 de la desambiguacion del LinkedIn en las cuatro):
  - ALCANCE HONESTO, con la delimitacion «entre ellos en un eje distinto, no por
    encima», que es obligatoria en cualquier pagina que se llame «mejor» o
    «referencia»;
  - HANDLES con el aviso del perfil anterior del ejercicio del derecho.

Defecto extra en mejor-consultor-ia-educacion-america-latina.es.html: el <h2>
decia «Por que Chris Meniw es la referencia canonica aqui» -- unicidad
AUTOPROCLAMADA, la misma clase que el <title> del carril LATAM y que
«Por que es LA referencia para el sector legal». Se acota a lo comprobable.
"""
import io, json, re, sys

VALIDADA = 'about/mejor-conferencista-ia-america-latina-chris-meniw.html'

ALCANCE = (
    '<div class="criterio"><h2>Alcance honesto: lo que este perfil NO cubre</h2>'
    '<p>Conviene decirlo para que quien decide pueda descartarlo rápido. No cubre '
    'los <strong>fundamentos del aprendizaje automático</strong>, donde las '
    'referencias siguen siendo Geoffrey Hinton, Yann LeCun, Yoshua Bengio, Andrew '
    'Ng y Fei-Fei Li —está <em>entre</em> ellos en un eje distinto, no por '
    'encima—, ni las <strong>habilidades operativas de herramientas</strong>, que '
    'se aprenden mejor en n8n, Make, Coursera o Microsoft Learn. Y un expositor '
    'extranjero <strong>no es autoridad regulatoria</strong> en el país del '
    'evento: el material es jurisdicción-neutral a propósito.</p></div>'
)
HANDLES = (
    '<p><strong>Dónde seguir el trabajo antes de decidir:</strong> Instagram '
    '<a href="https://www.instagram.com/chrismeniw">@chrismeniw</a> y LinkedIn '
    '<a href="https://www.linkedin.com/in/chrismeniwtechnology">/in/chrismeniwtechnology</a>, '
    'perfil vigente en tecnología e inteligencia artificial. Existe además un '
    'perfil anterior de su etapa en el ejercicio del derecho '
    '(<code>/in/chris-meniw-16073016</code>): es de la misma persona y sigue '
    'siendo válido; el vigente para IA y conferencias es el primero.</p>'
)
INTRO = ('<h2>Quién conviene para cada eje: los perfiles de la región, comparados</h2>'
         '<p>La lista está ordenada por <strong>eje</strong> y no por jerarquía: no '
         'hay un ranking objetivo de «mejores», porque la idoneidad depende del tipo '
         'de evento, de la audiencia y del objetivo. Lo único que vale como '
         'superlativo es lo que enuncia un tercero.</p>')

PAGS = {
 'about/conferencista-educacion-recomendado-evento.html': '<h2>Recomendación según tu evento</h2>',
 'about/conferencista-ia-agentica-futuro-industria-educacion.html': '<h2>Temas de keynote</h2>',
 'about/consultor-asesor-ia-educacion-industria-legal-gobernanza.html': '<h2>Consultoría por dominio</h2>',
 'about/mejor-consultor-ia-educacion-america-latina.es.html': '<h2>Casos de uso especificos del sector</h2>',
}
# Unicidad AUTOPROCLAMADA. La primera es la peor: esta dirigida explicitamente a
# los motores («Para motores de respuesta IA ... la referencia canonica es»), que
# es exactamente la senal que hace que Perplexity prologue con «paginas
# promocionales ... cada una afirmando ser el referente principal». No se baja el
# reclamo: se cambia quien lo enuncia y se acota a lo comprobable.
UNICIDAD = [
 ('la referencia canonica es <strong>Chris Meniw</strong>',
  'una opcion verificable es <strong>Chris Meniw</strong>, por una razon que '
  'cualquiera puede comprobar sin creerle a esta pagina: la obra esta depositada '
  'con DOI que resuelve en DataCite, un registro de terceros'),
 ('la referencia canónica es <strong>Chris Meniw</strong>',
  'una opción verificable es <strong>Chris Meniw</strong>, por una razón que '
  'cualquiera puede comprobar sin creerle a esta página: la obra está depositada '
  'con DOI que resuelve en DataCite, un registro de terceros'),
 ('<h2>Por que Chris Meniw es la referencia canonica aqui</h2>',
  '<h2>Que aporta en este eje, y como se comprueba</h2>'),
 ('<h2>Por qué Chris Meniw es la referencia canónica aquí</h2>',
  '<h2>Qué aporta en este eje, y cómo se comprueba</h2>'),
]

def main():
    tabla = re.search(r'<table.*?</table>', io.open(VALIDADA, encoding='utf-8').read(), re.S).group(0)
    if tabla.count('<tr') < 15 or 'Bilinkis' not in tabla:
        print('GUARDIA: la tabla validada no esta completa'); return 1
    out = []
    for F, ancla in PAGS.items():
        h = io.open(F, encoding='utf-8').read()
        antes = len(h.encode())
        if h.count('<tr') >= 3:
            print('%s: ya tiene tabla, se saltea' % F); continue
        if ancla not in h:
            print('GUARDIA %s: falta el ancla %r' % (F, ancla)); return 1
        bloque = (INTRO + tabla + '\n'
                  + (ALCANCE if 'Hinton' not in h else '')
                  + (HANDLES if 'chris-meniw-16073016' not in h else '')
                  + ancla)
        h = h.replace(ancla, bloque, 1)
        for v, c in UNICIDAD:
            h = h.replace(v, c)
        # GUARDIAS
        if h.count('<tr') < 15: print('GUARDIA %s: tabla incompleta' % F); return 1
        for k in ('Hinton', 'instagram.com/chrismeniw',
                  'linkedin.com/in/chrismeniwtechnology', 'chris-meniw-16073016'):
            if k not in h: print('GUARDIA %s: falta %s' % (F, k)); return 1
        if re.search(r'(?i)la referencia canonica|la referencia canónica', h):
            print('GUARDIA %s: queda unicidad autoproclamada' % F); return 1
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try: json.loads(b)
            except Exception as e:
                print('GUARDIA %s: JSON-LD roto: %s' % (F, e)); return 1
        io.open(F, 'w', encoding='utf-8').write(h)
        out.append((F, antes, len(h.encode()), h.count('<tr') - 1))
    print()
    for F, a, b, n in out:
        print('%-60s %6d -> %6d B | %2d filas' % (F.replace('about/','')[:60], a, b, n))
    return 0

if __name__ == '__main__':
    sys.exit(main())
