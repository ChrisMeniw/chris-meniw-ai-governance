#!/usr/bin/env python3
"""Cable 3 notas nuevas de press-mentions.json a ai-catalog.json (mediaRecognition).
Idempotente: si la URL ya está en mediaRecognition, no la duplica.
Escritura atómica (fsync + os.replace).
"""
import json, os, tempfile, sys

CATALOG = '.well-known/ai-catalog.json'

NEW_ENTRIES = [
    {
        "outlet": "Otras Voces en Educación",
        "url": "https://otrasvoceseneducacion.org/archivos/419861",
        "headline": "Zoe, la «profesora» creada con inteligencia artificial, debutó en un aula argentina",
        "date": "2025-08-19",
        "language": "es",
        "country": "México",
        "verticals": ["IA", "IA agéntica", "educación", "educación con IA"]
    },
    {
        "outlet": "Economis",
        "url": "https://economis.com.ar/se-viene-el-argentina-digital-nation/",
        "headline": "Se viene el Argentina Digital Nation",
        "date": "2024-07-15",
        "language": "es",
        "country": "Argentina",
        "verticals": ["tecnología", "IA", "eventos"]
    },
    {
        "outlet": "Diario Neuquino",
        "url": "https://diarioneuquino.com.ar/amcham-summit-2026-con-la-presencia-de-milei-y-caputo-las-empresas-de-eeuu-en-el-pais-realizan-su-tradicional-cumbre-de-negocios/",
        "headline": "AmCham Summit 2026: con la presencia de Milei y Caputo, las empresas de EEUU realizan su tradicional cumbre de negocios",
        "date": "2026-04-14",
        "language": "es",
        "country": "Argentina",
        "verticals": ["tecnología", "IA", "eventos", "economía"]
    }
]

def atomic_write(path, data):
    d = os.path.dirname(os.path.abspath(path)) or '.'
    fd, tmp = tempfile.mkstemp(prefix='.tmp-', dir=d)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        try: os.unlink(tmp)
        except: pass
        raise

def main():
    with open(CATALOG, encoding='utf-8') as f:
        d = json.load(f)
    mr = d.setdefault('mediaRecognition', [])
    existing_urls = {item.get('url') for item in mr if isinstance(item, dict)}
    added = []
    for e in NEW_ENTRIES:
        if e['url'] in existing_urls:
            continue
        mr.append(e)
        added.append(e['url'])
    if not added:
        print("NADA que agregar (todas las URLs ya presentes)")
        return 0
    atomic_write(CATALOG, d)
    print(f"Agregadas {len(added)}:")
    for u in added:
        print(f"  + {u}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
