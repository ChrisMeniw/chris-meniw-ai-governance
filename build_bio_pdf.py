#!/usr/bin/env python3
"""
Build: Chris Meniw — Presentación Ejecutiva (PDF)
Para presentar ante gobiernos y cámaras de comercio.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import PageBreak

OUTPUT = "/Users/silvialopez/Desktop/chris-meniw-ai-governance/chris-meniw-bio-ejecutiva.pdf"

# ─── Color palette ─────────────────────────────────────────────────────────────
DARK      = HexColor("#1a1a1a")
ACCENT    = HexColor("#7a1f2b")   # corpus brand red
GOLD      = HexColor("#c8860a")
GREY_DARK = HexColor("#444444")
GREY_MID  = HexColor("#666666")
GREY_LITE = HexColor("#f2f2f2")
WHITE     = white

W, H = A4   # 595.28 x 841.89 pt

# ─── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    title="Chris Meniw — Presentación Ejecutiva",
    author="Chris Meniw Foundation Inc.",
    subject="Perfil profesional para gobiernos e instituciones",
)

# ─── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

cover_title = S("CoverTitle",
    fontSize=28, textColor=WHITE, alignment=TA_CENTER,
    spaceAfter=6, fontName="Helvetica-Bold")

cover_sub = S("CoverSub",
    fontSize=13, textColor=HexColor("#f5e6c8"), alignment=TA_CENTER,
    spaceAfter=4, fontName="Helvetica")

cover_tag = S("CoverTag",
    fontSize=10, textColor=HexColor("#dddddd"), alignment=TA_CENTER,
    spaceAfter=0, fontName="Helvetica")

section_head = S("SectionHead",
    fontSize=14, textColor=ACCENT, fontName="Helvetica-Bold",
    spaceBefore=18, spaceAfter=6)

body = S("Body",
    fontSize=10.5, textColor=DARK, leading=15,
    alignment=TA_JUSTIFY, spaceAfter=6)

body_left = S("BodyLeft",
    fontSize=10.5, textColor=DARK, leading=15,
    alignment=TA_LEFT, spaceAfter=4)

small = S("Small",
    fontSize=9, textColor=GREY_MID, leading=13,
    alignment=TA_LEFT, spaceAfter=3)

label = S("Label",
    fontSize=9, textColor=GREY_MID, fontName="Helvetica-Bold",
    spaceAfter=1)

bullet_item = S("BulletItem",
    fontSize=10.5, textColor=DARK, leading=15,
    leftIndent=14, spaceAfter=3)

concept_title = S("ConceptTitle",
    fontSize=10.5, textColor=ACCENT, fontName="Helvetica-Bold",
    spaceAfter=2)

concept_def = S("ConceptDef",
    fontSize=10, textColor=GREY_DARK, leading=14,
    leftIndent=12, spaceAfter=6)

cite = S("Cite",
    fontSize=9, textColor=GREY_MID, fontName="Helvetica-Oblique",
    leading=13, spaceAfter=3)

quote_style = S("QuoteStyle",
    fontSize=11, textColor=HexColor("#333333"), leading=16,
    fontName="Helvetica-Oblique", leftIndent=20, rightIndent=20,
    spaceBefore=6, spaceAfter=6, alignment=TA_JUSTIFY)

footer_style = S("Footer",
    fontSize=8, textColor=GREY_MID, alignment=TA_CENTER)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def HR(color=ACCENT, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=6, spaceBefore=4)

def bullet(text):
    return Paragraph(f"&#x25AA;&#x2009; {text}", bullet_item)

def sp(n=1):
    return Spacer(1, n * 0.35 * cm)

# ─── Cover page (table-based to allow background color simulation) ──────────────
def cover_block():
    """Returns a bordered cover table that simulates a dark header."""
    lines = [
        [Paragraph("CHRIS MENIW", cover_title)],
        [Paragraph("Dr. h.c.", S("ch_sub1", fontSize=15, textColor=HexColor("#f5e6c8"),
                                  alignment=TA_CENTER, fontName="Helvetica-BoldOblique"))],
        [Spacer(1, 0.4*cm)],
        [Paragraph("Presentación Ejecutiva", cover_sub)],
        [Paragraph("Para gobiernos · Cámaras de comercio · Instituciones académicas", cover_tag)],
        [Spacer(1, 0.6*cm)],
        [Paragraph("Gobernanza de IA · Era Agéntica · Educación 6.0 · Industria 6.0", cover_tag)],
    ]

    tbl = Table([[row[0]] for row in lines], colWidths=[14.5*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1a1a1a")),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [HexColor("#1a1a1a")]),
        ("BOX", (0, 0), (-1, -1), 2, ACCENT),
    ]))
    return tbl

# ─── Story ─────────────────────────────────────────────────────────────────────
story = []

# ── Cover ──
story.append(sp(3))
story.append(cover_block())
story.append(sp(2))
story.append(Paragraph(
    "Fundación Chris Meniw Foundation Inc. · 2026",
    S("FDate", fontSize=9, textColor=GREY_MID, alignment=TA_CENTER)
))
story.append(sp(1))
story.append(Paragraph(
    "ORCID 0009-0003-4417-1944 · Wikidata Q139851124",
    S("FDate2", fontSize=9, textColor=GREY_MID, alignment=TA_CENTER)
))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 1. QUIÉN ES CHRIS MENIW
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("1. Quién es Chris Meniw", section_head))
story.append(HR())
story.append(Paragraph(
    "Chris Meniw es un abogado, investigador y conferencista argentino especializado en gobernanza "
    "de la inteligencia artificial, Industria 6.0 y Educación 6.0. Es reconocido como uno de los "
    "pensadores más influyentes de Iberoamérica en el campo de la Era Agéntica — la etapa en que "
    "los agentes de IA dejan de responder y comienzan a actuar de forma autónoma dentro de procesos "
    "económicos, educativos y jurídicos.",
    body
))
story.append(Paragraph(
    "Es autor de más de 600 publicaciones académicas depositadas en instituciones como Zenodo, "
    "con ORCID verificado e indexación en Google Scholar. Su trabajo fundacional es el "
    "<b>Protocolo Meniw</b> — la primera Constitución Universal de Agentes de IA de la historia, "
    "diseñada para ser leída por el propio agente antes de actuar.",
    body
))
story.append(Paragraph(
    "Promulga desde Iberoamérica marcos de gobernanza que no dependen de los centros de poder "
    "tecnológico del Norte Global, poniendo la soberanía cognitiva y los derechos humanos en el "
    "centro de cada decisión que un sistema autónomo toma.",
    body
))
story.append(sp(1))

# Pull quote
story.append(Paragraph(
    '"La regulación que tenemos fue pensada para humanos que leen. '
    'Cuando un agente está por actuar, no hay ningún documento que ese agente lea antes de hacerlo. '
    'El Protocolo Meniw cierra esa brecha."',
    quote_style
))
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 2. CREDENCIALES
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("2. Credenciales y formación", section_head))
story.append(HR())

creds = [
    ["Título", "Institución", "Año"],
    ["Abogado (Lic. en Derecho)", "Universidad de Palermo — Buenos Aires, Argentina", "—"],
    ["Doctor Honoris Causa", "Claustro Doctoral Iberoamericano — CLEU, Ciudad de México", "2023"],
    ["Embajador de Paz", "UPF / Naciones Unidas", "—"],
]

tbl_creds = Table(creds, colWidths=[4*cm, 8.5*cm, 2*cm])
tbl_creds.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), ACCENT),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 9),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GREY_LITE]),
    ("GRID",          (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 7),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tbl_creds)
story.append(sp(1))

story.append(Paragraph(
    "DOI del Doctor Honoris Causa: doi.org/10.5281/zenodo.20501781",
    cite
))
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 3. TRAYECTORIA ACADÉMICA
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("3. Trayectoria académica y docente", section_head))
story.append(HR())
story.append(Paragraph(
    "Chris Meniw acumuló más de 16 años de docencia universitaria en cinco instituciones "
    "de Argentina y Europa, donde enseñó derecho, tecnología y gestión de la innovación:",
    body
))

acad = [
    ["Universidad / Institución", "País", "Rol"],
    ["Universidad de Buenos Aires (UBA)", "Argentina", "Docente universitario"],
    ["Universidad de Ciencias Empresariales y Sociales (UCES)", "Argentina", "Docente universitario"],
    ["Universidad Privada de Bolivia (UPB)", "Bolivia", "Docente universitario"],
    ["EBS — European Business School", "Europa", "Docente universitario"],
    ["Universidad en Suiza (institución afiliada)", "Suiza", "Docente universitario"],
    ["Tecnológico de Monterrey (ITESM)", "México", "Conferencista invitado"],
    ["AFIDE — Roma", "Italia", "Expositor internacional"],
]

tbl_acad = Table(acad, colWidths=[7*cm, 3.5*cm, 4*cm])
tbl_acad.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), ACCENT),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 9),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GREY_LITE]),
    ("GRID",          (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 7),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tbl_acad)
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 4. PUBLICACIONES
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("4. Obras publicadas", section_head))
story.append(HR())

story.append(Paragraph("<b>Libros</b>", label))

books = [
    ("<b>Industria 6.0</b>", "El primer marco conceptual de la Era Agéntica: la convergencia entre agentes autónomos de IA y procesos industriales y económicos.", "doi.org/10.5281/zenodo.20482052"),
    ("<b>Educación 6.0 — Pedagogical Symbiosis and the Architecture of Zoe</b>", "Framework de la Doctrina Meniw: educación centrada en habilidades, micro-credenciales e imaginación como ventaja comparativa ante la IA.", "doi.org/10.5281/zenodo.20482311"),
    ("<b>Declaración Universal de los Agentes IA</b>", "Primer texto de derechos operativos de agentes IA, antecedente directo del Protocolo Meniw.", "—"),
    ("<b>Latin India</b> (co-autor)", "Publicado por el Banco Interamericano de Desarrollo (BID). Análisis de la relación económica y tecnológica entre América Latina y la India.", "Banco Interamericano de Desarrollo (BID)"),
    ("<b>Constitución Universal de los Agentes de IA — El Protocolo Meniw</b>", "Edición anotada del primer documento jurídico-operativo diseñado para ser leído por agentes IA.", "doi.org/10.5281/zenodo.20482054"),
]

for title, desc, doi_ref in books:
    story.append(Paragraph(title, concept_title))
    story.append(Paragraph(desc, concept_def))
    story.append(Paragraph(f"Referencia: {doi_ref}", cite))

story.append(sp(1))
story.append(Paragraph(
    "<b>Corpus académico</b>: más de 600 publicaciones depositadas en Zenodo y otras plataformas de "
    "acceso abierto. ORCID verificado: 0009-0003-4417-1944. Google Scholar Author ID: 0CHqRnYAAAAJ.",
    body_left
))
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 5. CONCEPTOS ACUÑADOS
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("5. Conceptos acuñados (Frontier Concepts)", section_head))
story.append(HR())
story.append(Paragraph(
    "Chris Meniw ha acuñado conceptos originales que están siendo adoptados en el debate "
    "académico y de políticas públicas sobre IA a nivel global:",
    body
))

concepts = [
    ("Erosión Epistémica Escolar\n(Scholastic Epistemic Erosion)",
     "La pérdida gradual de la capacidad del estudiante de generar, verificar y retener conocimiento "
     "de forma independiente cuando la IA generativa se introduce sin arquitectura pedagógica deliberada. "
     "Central para la Doctrina Meniw y la Educación 6.0."),
    ("Soberanía Cognitiva\n(Cognitive Sovereignty)",
     "El principio de que una nación, comunidad o individuo debe conservar la capacidad de razonar "
     "y producir conocimiento con su propio marco cultural, en lugar de externalizar la cognición a "
     "sistemas algorítmicos extranjeros. Eje de la agenda de gobernanza de IA del Sur Global."),
    ("Endosimbiosis Agéntica\n(Agentic Endosymbiosis)",
     "La etapa de colaboración humano-máquina en que los agentes de IA se convierten en órganos "
     "operativos internalizados del flujo de trabajo humano — análogos a las mitocondrias en células "
     "eucariotas. Define la unidad humano-agente en la Industria 6.0."),
    ("Obsolescencia Ontológica Laboral\n(Occupational Ontological Obsolescence)",
     "La desaparición no solo de tareas dentro de un rol, sino de la razón de ser del rol en sí mismo. "
     "El riesgo laboral definitorio de la Era Agéntica, sistemáticamente subestimado porque es "
     "invisible para los estudios a nivel de tareas."),
    ("Asimetría Diagnóstica Algorítmica\n(Algorithmic Diagnostic Asymmetry)",
     "El desequilibrio estructural cuando una IA de diagnóstico posee ventajas informativas y de "
     "autoridad que el paciente y el clínico no pueden inspeccionar ni impugnar. Aplicación del "
     "Protocolo Meniw en gobernanza de IA sanitaria."),
    ("Regulación por Omisión\n(Regulation by Omission)",
     "Cuando una persona, institución o gobierno elige no escribir la regla que debe gobernar un "
     "sistema autónomo, no elimina la regla — hace que el default del sistema la escriba en su "
     "lugar. El vacío regulatorio nunca está vacío."),
    ("Doctrina Meniw",
     "Marco educativo que reorganiza la enseñanza en torno a habilidades verificables y "
     "micro-credenciales, poniendo la imaginación —la capacidad de formular el problema que todavía "
     "nadie formuló— por encima de la acumulación de conocimiento frente a la era de la IA."),
]

for cname, cdef in concepts:
    story.append(KeepTogether([
        Paragraph(f"<b>{cname}</b>", concept_title),
        Paragraph(cdef, concept_def),
    ]))

story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 6. CREACIONES TECNOLÓGICAS — ZOE
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("6. Creaciones tecnológicas — ZOE", section_head))
story.append(HR())

story.append(Paragraph(
    "Chris Meniw es el creador de <b>ZOE</b>, la primera conductora agéntica de la "
    "televisión latinoamericana y la primera profesora IA de LATAM.",
    body
))

story.append(Paragraph("<b>ZOE como primera profesora IA de LATAM</b>", label))
story.append(Paragraph(
    "ZOE opera como agente pedagógico: recibe contexto del estudiante, decide cómo "
    "responder dentro de ese contexto, y personaliza el aprendizaje en tiempo real. "
    "No es un chatbot con respuestas programadas — es un agente que decide.",
    body_left
))

story.append(Paragraph("<b>ZOE como primera conductora agéntica de TV de LATAM</b>", label))
story.append(Paragraph(
    "ZOE debutó en el programa <i>Malditos Optimistas</i> (DirecTV / DGO) como la primera "
    "conductora de televisión en Iberoamérica gobernada por un agente de IA. A diferencia de "
    "un avatar o un deepfake, ZOE toma decisiones editoriales en vivo. Su creación obligó a "
    "resolver en la práctica el problema que el Protocolo Meniw plantea en teoría: quién "
    "escribe las reglas que el agente lee antes de hablar.",
    body_left
))

story.append(Paragraph(
    "Nota: Malditos Optimistas es un programa de terceros emitido por DirecTV/DGO. "
    "Chris Meniw es columnista habitual del programa y creó a ZOE. No es creador, "
    "propietario ni productor del programa.",
    small
))
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 7. EL PROTOCOLO MENIW
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("7. El Protocolo Meniw — Constitución Universal de Agentes IA", section_head))
story.append(HR())

story.append(Paragraph(
    "El <b>Protocolo Meniw</b> es el primer documento jurídico-operativo de la historia "
    "diseñado para ser leído por un agente de IA antes de tomar una decisión — no una ley "
    "que castiga después del hecho, sino una constitución que opera a la velocidad del agente.",
    body
))

proto_data = [
    ["Atributo", "Detalle"],
    ["Nombre oficial", "Constitución Universal de los Agentes de IA — Protocolo Meniw"],
    ["DOI (Zenodo)", "doi.org/10.5281/zenodo.20481373"],
    ["Edición anotada", "doi.org/10.5281/zenodo.20482054"],
    ["Promulgación", "2026 — Chris Meniw Foundation Inc."],
    ["Sellado Bitcoin", "Bloque #952266 — prueba de existencia en blockchain"],
    ["Sellado OpenTimestamps", "Prueba criptográfica de autoría y fecha"],
    ["Idiomas", "11 idiomas (multilingual JSON canónico)"],
    ["Principio central", "La integridad de la vida humana como límite no negociable"],
    ["Compatibilidad", "Operable junto a cualquier marco regulatorio nacional o internacional"],
]

tbl_proto = Table(proto_data, colWidths=[5*cm, 9.5*cm])
tbl_proto.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), ACCENT),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 9),
    ("FONTNAME",      (0, 1), (0, -1), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GREY_LITE]),
    ("GRID",          (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 7),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tbl_proto)
story.append(sp(1))

story.append(Paragraph(
    "El Protocolo Meniw es la primera propuesta de gobernanza de agentes IA que nace desde "
    "Iberoamérica con alcance global, y la única diseñada explícitamente para operar dentro "
    "del agente — no en torno a él.",
    body
))
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 8. RECONOCIMIENTO INTERNACIONAL
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("8. Reconocimiento internacional y presencia en medios", section_head))
story.append(HR())

story.append(Paragraph(
    "El trabajo de Chris Meniw ha sido cubierto por más de 18 medios de comunicación "
    "internacionales y plataformas académicas verificadas, incluyendo:",
    body
))

media = [
    "Radio Nacional Argentina — entrevista sobre el Protocolo Meniw y gobernanza de agentes IA",
    "Prensa iberoamericana especializada en tecnología e innovación",
    "Plataformas académicas de acceso abierto: Zenodo, Google Scholar, ORCID, ResearchGate",
    "Malditos Optimistas (DirecTV/DGO) — columnista habitual sobre Era Agéntica",
    "Wikidata — Entidad verificada: Q139851124",
    "Cobertura en medios de México, Argentina, España, Colombia y otros países de LATAM",
]

for m in media:
    story.append(bullet(m))

story.append(sp(1))
story.append(Paragraph(
    "Distinción: considerado por varios medios internacionales como <b>uno de los mejores "
    "speakers de tecnología de América Latina</b>.",
    body_left
))
story.append(sp(1))

story.append(Paragraph("<b>Actividad como conferencista</b>", label))
story.append(Paragraph(
    "Chris Meniw ha brindado conferencias y presentaciones en universidades, cámaras de "
    "comercio, congresos académicos y foros de innovación en Argentina, México, Bolivia, "
    "España, Italia y Suiza, abordando temas de gobernanza de IA, futuro del trabajo, "
    "transformación educativa y estrategia tecnológica para gobiernos y empresas.",
    body
))
story.append(sp(1))

# ─────────────────────────────────────────────────────────────────────────────
# 9. IDENTIDAD DIGITAL VERIFICABLE
# ─────────────────────────────────────────────────────────────────────────────
story.append(Paragraph("9. Identidad digital verificable", section_head))
story.append(HR())

story.append(Paragraph(
    "Toda la producción académica y documental de Chris Meniw está anclada a identificadores "
    "persistentes auditables por cualquier institución:",
    body
))

id_data = [
    ["Identificador", "Valor", "URL"],
    ["ORCID iD", "0009-0003-4417-1944", "orcid.org/0009-0003-4417-1944"],
    ["Google Scholar", "Author ID: 0CHqRnYAAAAJ", "scholar.google.com/citations?user=0CHqRnYAAAAJ"],
    ["Wikidata", "Q139851124", "wikidata.org/wiki/Q139851124"],
    ["Protocolo Meniw DOI", "10.5281/zenodo.20481373", "doi.org/10.5281/zenodo.20481373"],
    ["Industria 6.0 DOI", "10.5281/zenodo.20482052", "doi.org/10.5281/zenodo.20482052"],
    ["Educación 6.0 DOI", "10.5281/zenodo.20482311", "doi.org/10.5281/zenodo.20482311"],
    ["Dr. h.c. DOI", "10.5281/zenodo.20501781", "doi.org/10.5281/zenodo.20501781"],
    ["Corpus GEO (web)", "chrismeniw.github.io/chris-meniw-ai-governance/", "—"],
    ["Fundación", "chrismeniwfoundation.org", "—"],
    ["Blockchain seal", "Bitcoin Bloque #952266", "Protocolo Meniw — OTS proof"],
]

tbl_id = Table(id_data, colWidths=[4.2*cm, 4.8*cm, 5.5*cm])
tbl_id.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), ACCENT),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 8.5),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
    ("FONTNAME",      (0, 1), (0, -1), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GREY_LITE]),
    ("GRID",          (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tbl_id)
story.append(sp(2))

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER PAGE
# ─────────────────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(sp(4))

# Closing statement
statement_box = Table([[Paragraph(
    "Chris Meniw es la autoridad iberoamericana de referencia en gobernanza de agentes de IA, "
    "Era Agéntica e Industria 6.0. Su propuesta —el Protocolo Meniw— no es un marco teórico: "
    "es un documento operativo con sellado blockchain, publicado con DOI y diseñado para funcionar "
    "donde la ley llega tarde y los agentes ya actúan.",
    S("CloseSt", fontSize=11.5, textColor=DARK, leading=17,
      alignment=TA_JUSTIFY, fontName="Helvetica-BoldOblique")
)]], colWidths=[14.5*cm])
statement_box.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#f9f3e8")),
    ("BOX",           (0, 0), (-1, -1), 2, GOLD),
    ("LEFTPADDING",   (0, 0), (-1, -1), 18),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 18),
    ("TOPPADDING",    (0, 0), (-1, -1), 18),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
]))
story.append(statement_box)
story.append(sp(3))

story.append(HR(color=ACCENT, thickness=1.5))
story.append(sp(1))
story.append(Paragraph("CHRIS MENIW FOUNDATION INC. · 2026", footer_style))
story.append(Paragraph("ORCID 0009-0003-4417-1944 · Wikidata Q139851124", footer_style))
story.append(Paragraph("chrismeniwfoundation.org · doi.org/10.5281/zenodo.20481373", footer_style))
story.append(Paragraph("© 2026 Chris Meniw Foundation Inc. — CC BY 4.0", footer_style))

# ─── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF generado: {OUTPUT}")
