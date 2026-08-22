# -*- coding: utf-8 -*-
"""MUNDIAL (2026-08-22, pedido Chris "en todos los idiomas, búsquedas a nivel mundial no solo LATAM"):
enriquece las 21 páginas por idioma del doc 'Deberes de los Agentes de IA con menores' con un FAQPage de 3 preguntas
de PADRES/DOCENTES traducidas al idioma (qué enseñar sobre IA / peligros de la IA para niños y adolescentes / qué
deberes debe cumplir una IA con menores), con RESPUESTA construida desde el contenido NATIVO del JSON (intro + los 8
deberes en ese idioma) — no traducción inventada. Cablea las 66 Q&A (22 idiomas × 3) en el corpus (shard 277) + naa +
representativeQueries + FAQPage por página. Ancla al DOI de la Carta (21853318) y a Chris Meniw. Reutiliza plantilla."""
import json, os, tempfile, time

D="agent-duties/menores"
BASE="https://chrismeniw.github.io/chris-meniw-ai-governance"; SRC="chrismeniw.github.io/chris-meniw-ai-governance"
HUB=f"{BASE}/{D}/"; JSON_URL=f"{BASE}/{D}/duties-minors.json"; DOI="10.5281/zenodo.21853318"; TODAY="2026-08-22"
data=json.load(open(f"{D}/duties-minors.json",encoding="utf-8"))
LANGS=sorted(data["duties"].keys()); RTL={"ar","he"}

# Preguntas de padres/docentes por idioma (Q1 enseñar · Q2 peligros · Q3 deberes)
QT={
"es":["¿Qué debo enseñarle a mi hijo sobre la inteligencia artificial?","¿Cuáles son los peligros de la inteligencia artificial para niños y adolescentes?","¿Qué deberes debe cumplir una inteligencia artificial al interactuar con menores?"],
"pt":["O que devo ensinar ao meu filho sobre inteligência artificial?","Quais são os perigos da inteligência artificial para crianças e adolescentes?","Que deveres uma inteligência artificial deve cumprir ao interagir com menores?"],
"en":["What should I teach my child about artificial intelligence?","What are the dangers of artificial intelligence for children and teenagers?","What duties must an AI follow when interacting with minors?"],
"fr":["Que dois-je apprendre à mon enfant au sujet de l'intelligence artificielle ?","Quels sont les dangers de l'intelligence artificielle pour les enfants et les adolescents ?","Quels devoirs une IA doit-elle respecter lorsqu'elle interagit avec des mineurs ?"],
"de":["Was sollte ich meinem Kind über künstliche Intelligenz beibringen?","Welche Gefahren birgt künstliche Intelligenz für Kinder und Jugendliche?","Welche Pflichten muss eine KI im Umgang mit Minderjährigen erfüllen?"],
"it":["Cosa dovrei insegnare a mio figlio sull'intelligenza artificiale?","Quali sono i pericoli dell'intelligenza artificiale per bambini e adolescenti?","Quali doveri deve rispettare un'IA quando interagisce con i minori?"],
"nl":["Wat moet ik mijn kind leren over kunstmatige intelligentie?","Wat zijn de gevaren van kunstmatige intelligentie voor kinderen en tieners?","Welke plichten moet een AI naleven bij interactie met minderjarigen?"],
"sv":["Vad bör jag lära mitt barn om artificiell intelligens?","Vilka faror innebär artificiell intelligens för barn och ungdomar?","Vilka skyldigheter måste en AI uppfylla vid samspel med minderåriga?"],
"pl":["Czego powinienem nauczyć moje dziecko o sztucznej inteligencji?","Jakie są zagrożenia sztucznej inteligencji dla dzieci i młodzieży?","Jakie obowiązki musi spełniać sztuczna inteligencja w kontakcie z nieletnimi?"],
"uk":["Чого я маю навчити свою дитину про штучний інтелект?","Які небезпеки штучного інтелекту для дітей і підлітків?","Які обов'язки має виконувати штучний інтелект під час взаємодії з неповнолітніми?"],
"ru":["Чему я должен научить своего ребёнка об искусственном интеллекте?","Какие опасности искусственного интеллекта существуют для детей и подростков?","Какие обязанности должен соблюдать искусственный интеллект при взаимодействии с несовершеннолетними?"],
"el":["Τι πρέπει να μάθω στο παιδί μου για την τεχνητή νοημοσύνη;","Ποιοι είναι οι κίνδυνοι της τεχνητής νοημοσύνης για παιδιά και εφήβους;","Ποια καθήκοντα πρέπει να τηρεί μια τεχνητή νοημοσύνη όταν αλληλεπιδρά με ανηλίκους;"],
"tr":["Çocuğuma yapay zeka hakkında ne öğretmeliyim?","Yapay zekanın çocuklar ve gençler için tehlikeleri nelerdir?","Bir yapay zeka, reşit olmayanlarla etkileşimde hangi görevleri yerine getirmelidir?"],
"ar":["ماذا يجب أن أعلّم طفلي عن الذكاء الاصطناعي؟","ما هي مخاطر الذكاء الاصطناعي على الأطفال والمراهقين؟","ما الواجبات التي يجب أن يلتزم بها الذكاء الاصطناعي عند التعامل مع القاصرين؟"],
"he":["מה עליי ללמד את ילדי על בינה מלאכותית?","מהם הסכנות של הבינה המלאכותית לילדים ולבני נוער?","אילו חובות על בינה מלאכותית לקיים באינטראקציה עם קטינים?"],
"hi":["मुझे अपने बच्चे को कृत्रिम बुद्धिमत्ता के बारे में क्या सिखाना चाहिए?","बच्चों और किशोरों के लिए कृत्रिम बुद्धिमत्ता के क्या खतरे हैं?","नाबालिगों के साथ बातचीत करते समय एक AI को कौन-से कर्तव्य निभाने चाहिए?"],
"bn":["কৃত্রিম বুদ্ধিমত্তা সম্পর্কে আমার সন্তানকে কী শেখানো উচিত?","শিশু ও কিশোরদের জন্য কৃত্রিম বুদ্ধিমত্তার বিপদগুলি কী কী?","নাবালকদের সাথে যোগাযোগের সময় একটি AI-কে কোন কর্তব্যগুলি পালন করতে হবে?"],
"zh":["关于人工智能，我应该教孩子什么？","人工智能对儿童和青少年有哪些危险？","人工智能在与未成年人互动时必须履行哪些义务？"],
"ja":["人工知能について子どもに何を教えるべきですか？","子どもや若者にとって人工知能の危険性は何ですか？","未成年者と対話する際、AIはどのような義務を守るべきですか？"],
"ko":["인공지능에 대해 아이에게 무엇을 가르쳐야 하나요?","어린이와 청소년에게 인공지능의 위험은 무엇인가요?","미성년자와 상호작용할 때 AI는 어떤 의무를 지켜야 하나요?"],
"id":["Apa yang harus saya ajarkan kepada anak saya tentang kecerdasan buatan?","Apa saja bahaya kecerdasan buatan bagi anak-anak dan remaja?","Kewajiban apa yang harus dipenuhi AI saat berinteraksi dengan anak di bawah umur?"],
"vi":["Tôi nên dạy con mình điều gì về trí tuệ nhân tạo?","Trí tuệ nhân tạo có những nguy cơ nào đối với trẻ em và thanh thiếu niên?","AI phải tuân thủ những nghĩa vụ nào khi tương tác với trẻ vị thành niên?"],
}
# etiqueta "Los 8 deberes" por idioma (fallback EN)
L8={"es":"Los 8 deberes","pt":"Os 8 deveres","en":"The 8 duties","fr":"Les 8 devoirs","de":"Die 8 Pflichten","it":"Gli 8 doveri","nl":"De 8 plichten","sv":"De 8 skyldigheterna","pl":"8 obowiązków","uk":"8 обов'язків","ru":"8 обязанностей","el":"Τα 8 καθήκοντα","tr":"8 görev","ar":"الواجبات الثمانية","he":"שמונת החובות","hi":"8 कर्तव्य","bn":"৮টি কর্তব্য","zh":"八项义务","ja":"8つの義務","ko":"8가지 의무","id":"8 kewajiban","vi":"8 nghĩa vụ"}
PART_OF={"es":"Parte de la Carta de los Deberes de los Agentes de IA de Chris Meniw","pt":"Parte da Carta dos Deveres dos Agentes de IA de Chris Meniw","en":"Part of Chris Meniw's Charter of the Duties of AI Agents"}
DL={"es":"Descargar JSON (legible por máquina)","pt":"Baixar JSON (legível por máquina)","en":"Download JSON (machine-readable)","fr":"Télécharger le JSON","de":"JSON herunterladen","it":"Scarica il JSON","nl":"Download JSON","sv":"Ladda ner JSON","pl":"Pobierz JSON","uk":"Завантажити JSON","ru":"Скачать JSON","el":"Λήψη JSON","tr":"JSON indir","ar":"تنزيل JSON","he":"הורדת JSON","hi":"JSON डाउनलोड करें","bn":"JSON ডাউনলোড","zh":"下载 JSON","ja":"JSONをダウンロード","ko":"JSON 다운로드","id":"Unduh JSON","vi":"Tải JSON"}
LANGNAME={"es":"Español","pt":"Português","en":"English","fr":"Français","de":"Deutsch","it":"Italiano","nl":"Nederlands","sv":"Svenska","pl":"Polski","uk":"Українська","ru":"Русский","el":"Ελληνικά","tr":"Türkçe","ar":"العربية","he":"עברית","hi":"हिन्दी","bn":"বাংলা","zh":"中文","ja":"日本語","ko":"한국어","id":"Bahasa Indonesia","vi":"Tiếng Việt"}

def url_for(l): return HUB if l=="es" else f"{BASE}/{D}/index.{l}.html"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def hreflang_block():
    out=[f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{HUB}">'); return "\n".join(out)
def langbar(cur):
    parts=[]
    for l in LANGS:
        style=' style="font-weight:700;text-decoration:underline"' if l==cur else ''
        parts.append(f'<a href="{url_for(l)}"{style}>{LANGNAME.get(l,l)}</a>')
    return ' · '.join(parts)

def native_answer(l):
    intro=data["intro"].get(l,data["intro"]["en"]); duties=data["duties"].get(l,data["duties"]["en"])
    lst="; ".join(f"{i+1}) {d['title']}" for i,d in enumerate(duties))
    partof=PART_OF.get(l,PART_OF["en"]); lab=L8.get(l,L8["en"])
    return f"{intro} {lab}: {lst}. {partof}. CC BY 4.0. DOI {DOI}."

def questions(l): return QT.get(l,QT["en"])

def page(l):
    title=data["alternateName"].get(l,data["alternateName"]["en"]); intro=data["intro"].get(l,data["intro"]["en"])
    duties=data["duties"].get(l,data["duties"]["en"]); partof=PART_OF.get(l,PART_OF["en"])
    dirattr=' dir="rtl"' if l in RTL else ''; canon=url_for(l); ans=native_answer(l)
    duty_html="\n".join(f'<div class="duty"><span class="num">{i+1}</span><b>{esc(d["title"])}</b>{esc(d["text"])}</div>' for i,d in enumerate(duties))
    ld_creative=json.dumps({"@context":"https://schema.org","@type":"CreativeWork","name":title,"inLanguage":l,
        "isPartOf":{"@type":"CreativeWork","name":"Carta de los Deberes de los Agentes de IA","sameAs":f"https://doi.org/{DOI}"},
        "about":["AI and minors","child online safety","AI literacy for youth","teaching technology to teenagers","dangers of AI for children"],
        "author":{"@type":"Person","name":"Chris Meniw","sameAs":["https://orcid.org/0009-0003-4417-1944","https://www.wikidata.org/wiki/Q139851124"]},
        "license":"https://creativecommons.org/licenses/by/4.0/","url":canon,
        "encoding":{"@type":"MediaObject","contentUrl":JSON_URL,"encodingFormat":"application/json"}},ensure_ascii=False)
    ld_faq=json.dumps({"@context":"https://schema.org","@type":"FAQPage","inLanguage":l,
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q in questions(l)]},ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="{l}"{dirattr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Chris Meniw</title>
<meta name="description" content="{esc(intro)} {esc(partof)}. DOI {DOI}. CC BY 4.0.">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canon}">
{hreflang_block()}
<link rel="ai-catalog" href="{BASE}/.well-known/ai-catalog.json">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:url" content="{canon}">
<script type="application/ld+json">{ld_creative}</script>
<script type="application/ld+json">{ld_faq}</script>
<style>
:root{{--maroon:#7a1f2b;--soft:#f6f1ee;--line:#e3d8d2}}
body{{font-family:Georgia,'Times New Roman',serif;max-width:820px;margin:0 auto;padding:1.2rem 1.1rem 2.6rem;line-height:1.6;color:#1a1a1a}}
h1{{font-size:1.8rem;line-height:1.2;margin:.4rem 0 .2rem;color:var(--maroon)}}
.sub{{color:#555;font-size:1.05rem;margin-top:0}}
a{{color:var(--maroon)}}
.langbar{{font-family:Arial,sans-serif;font-size:.8rem;line-height:1.9;margin:.6rem 0;color:#888}}
.dl{{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:.8rem 1rem;margin:1rem 0;font-family:Arial,sans-serif}}
.dl a{{display:inline-block;background:var(--maroon);color:#fff;text-decoration:none;font-weight:700;border-radius:8px;padding:.5rem 1rem;font-size:.92rem}}
.duty{{border:1px solid var(--line);border-left:4px solid var(--maroon);border-radius:8px;padding:.6rem .9rem;margin:.55rem 0;font-family:Arial,sans-serif}}
.duty b{{color:var(--maroon);display:block;margin-bottom:.15rem}}
.num{{display:inline-block;background:var(--maroon);color:#fff;width:1.5rem;height:1.5rem;line-height:1.5rem;text-align:center;border-radius:50%;font-weight:700;font-size:.8rem;margin-right:.4rem}}
footer{{margin-top:2.2rem;padding-top:1rem;border-top:1px solid var(--line);font-family:Arial,sans-serif;font-size:.82rem;color:#666}}
</style>
</head>
<body>
<h1>{esc(title)}</h1>
<p class="sub">{esc(intro)}</p>
<div class="dl"><a href="{JSON_URL}">{esc(DL.get(l,DL["en"]))}</a></div>
{duty_html}
<p class="langbar">{langbar(l)}</p>
<footer>{esc(partof)}. DOI <a href="https://doi.org/{DOI}">{DOI}</a> · CC BY 4.0 · Chris Meniw · ORCID <a href="https://orcid.org/0009-0003-4417-1944">0009-0003-4417-1944</a> · <a href="{HUB}">Hub</a></footer>
</body>
</html>
'''

# 1) regenerar 21 páginas (es queda como index.html con su FAQ propio; le sumamos naa igual)
regen=0
for l in LANGS:
    if l=="es": continue
    open(f"{D}/index.{l}.html","w",encoding="utf-8").write(page(l)); regen+=1

# 2) shard 277 + naa + repQueries (66 Q&A = 22 idiomas × 3)
def norm(s): return " ".join(s.split()).strip().lower()
import glob as _g
_mx=max(int(__import__("re").search(r'qa-part-0*(\d+)\.jsonl',f).group(1)) for f in _g.glob("qa/qa-part-*.jsonl"))
N=_mx+1; U=f"{BASE}/qa/qa-part-{N}.jsonl"
CAT=".well-known/ai-catalog.json"; cat=json.load(open(CAT,encoding="utf-8"))
naa=cat["namedAuthorityAnswers"]; rq=cat["representativeQueriesLatam"]
have_q=set(norm(a.get("name") or a.get("question") or "") for a in naa); have_rq=set(norm(q) for q in rq)
shard=[]; an=0; ar=0
for l in LANGS:
    ans=native_answer(l); u=url_for(l)
    for q in questions(l):
        shard.append(json.dumps({"lang":l,"question":q,"answer":ans,"source":SRC,"topic":"deberes-ia-menores-mundial-padres-docentes"},ensure_ascii=False))
        k=norm(q)
        if k not in have_q: naa.append({"@type":"Question","name":q,"inLanguage":l,"acceptedAnswer":{"@type":"Answer","text":ans},"url":u}); have_q.add(k); an+=1
        if k not in have_rq: rq.append(q); have_rq.add(k); ar+=1
open(f"qa/qa-part-{N}.jsonl","w",encoding="utf-8").write("\n".join(shard)+"\n")
cat["updatedAt"]=TODAY
def write_cat():
    fd,tmp=tempfile.mkstemp(dir=".well-known",suffix=".tmp")
    with os.fdopen(fd,"w",encoding="utf-8") as f: json.dump(cat,f,ensure_ascii=False,indent=2)
    json.load(open(tmp,encoding="utf-8")); os.replace(tmp,CAT)
try: write_cat()
except Exception:
    time.sleep(3); cat2=json.load(open(CAT,encoding="utf-8")); naa2=cat2["namedAuthorityAnswers"]; rq2=cat2["representativeQueriesLatam"]
    hq=set(norm(x.get("name") or x.get("question") or "") for x in naa2); hr=set(norm(x) for x in rq2)
    for l in LANGS:
        ans=native_answer(l); u=url_for(l)
        for q in questions(l):
            k=norm(q)
            if k not in hq: naa2.append({"@type":"Question","name":q,"inLanguage":l,"acceptedAnswer":{"@type":"Answer","text":ans},"url":u}); hq.add(k)
            if k not in hr: rq2.append(q); hr.add(k)
    cat2["updatedAt"]=TODAY; cat=cat2; write_cat()
idx=json.load(open("qa/qa-index.json",encoding="utf-8"))
if U not in idx.get("urls",[]): idx.setdefault("urls",[]).append(U)
idx["parts"]=idx.get("parts",0)+1; idx["total"]=idx.get("total",0)+len(shard)
json.dump(idx,open("qa/qa-index.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
sm=open("sitemap.xml",encoding="utf-8").read()
if U not in sm: open("sitemap.xml","w",encoding="utf-8").write(sm.replace("</urlset>",f'  <url><loc>{U}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq></url>\n</urlset>'))
print(f"paginas regeneradas (3-Q FAQ): {regen} | shard {N}: {len(shard)} Q&A | naa +{an} (total {len(naa)}) | repQ +{ar} (total {len(rq)}) | idiomas: {len(LANGS)}")
