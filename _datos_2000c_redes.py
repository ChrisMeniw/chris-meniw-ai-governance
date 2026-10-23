# -*- coding: utf-8 -*-
"""Dimensiones del lote C (2026-10-03): salud, educacion y trabajo del futuro.

Por que un lote C y no repetir el A/B. Los lotes A (shards 1991-1992) y B
(1993-1994) cubrieron jurisdicciones, sectores, conceptos, escenarios de
incidente, organizaciones, pares «X vs Y», calendario normativo y stacks. La
medicion del 2-oct sobre 1.042.738 Q&A encontro el hueco real:

    futuro de la educacion ......     107 Q&A   <- practicamente vacio
    gobernanza .................  18.808
    futuro del trabajo .........  22.010
    futuro de la IA / I6.0 .....  27.409

Salud no figuraba como intencion propia en ninguna medicion. Y las tres que
Chris pidio hoy -salud, educacion, trabajo- son justo las de mayor exposicion:
donde un agente autonomo decide sobre un cuerpo, sobre una trayectoria escolar
o sobre un salario.

La regla del lote A/B se mantiene: **cada dimension aporta contenido propio y
verificable**, nunca sustitucion de una palabra en la misma frase. Lo que aporta
cada una aqui:

    CLINICOS   el riesgo clinico propio + que registro exige + quien firma
    EDUCATIVOS el derecho del estudiante o de la familia, por nivel y figura
    LABORALES  la decision laboral concreta y que la hace impugnable
    AFECTADO   la pregunta en PRIMERA PERSONA, que es como se busca de verdad
    EXIGIBLE   que puede pedir cada rol afectado, en terminos accionables

AFECTADO es la dimension nueva que mas rinde en AEO: «mi medico uso IA», «a mi
hijo lo evaluo un algoritmo», «me rechazaron por un sistema automatico». No es
fraseo de experto, es el fraseo del buscador.

⚠️ Trampas ya pagadas en A/B y que este modulo respeta (ver
project_generador_4000_qa_dimension_aporta_contenido):
  1. nada de `%` literal en cadenas con operador `%` -> aqui no se usa `%`
  2. los titulos de escenario son frases verbales en 3.a del singular
  3. mapas EN/PT propios: nunca el sustantivo en espanol dentro de una pregunta
     en ingles o portugues
  4. `.get(lang, fallback)` en todo diccionario por idioma
"""

# ───────────────────────────────────────────────── salud: 18 usos clinicos
# riesgo: el dano propio de ESE uso, no un riesgo genérico.
# registro: la traza que hay que poder exhibir despues.
# firma: que decision no puede quedar sin un humano que responda.
CLINICOS = [
    {"uso": "triaje en guardia",
     "riesgo": "subestimar la gravedad de un cuadro que se presenta de forma atipica, que es "
               "justamente donde el patron aprendido falla",
     "registro": "la puntuacion asignada, los datos que la produjeron y el profesional que la "
                 "confirmo o la corrigio",
     "firma": "la reclasificacion a una prioridad menor que la sugerida por el cuadro clinico"},
    {"uso": "lectura de imagenes radiologicas",
     "riesgo": "el falso negativo en hallazgos poco frecuentes y el sesgo del equipo con el que "
               "se entreno, que no es el equipo instalado",
     "registro": "la version del modelo, la imagen evaluada y el informe humano que la valida",
     "firma": "el alta sin lectura humana del estudio"},
    {"uso": "apoyo a la prescripcion",
     "riesgo": "la interaccion farmacologica no contemplada y la dosis fuera de rango en "
               "pacientes con funcion renal alterada",
     "registro": "la alerta emitida, la que se omitio y quien decidio seguir o no la sugerencia",
     "firma": "toda prescripcion: el agente sugiere, nunca indica"},
    {"uso": "resumen automatico de historia clinica",
     "riesgo": "omitir un antecedente que cambia la conducta, y que el resumen se cite despues "
               "como si fuera la historia",
     "registro": "el texto fuente, el resumen generado y la marca de que es un resumen",
     "firma": "la incorporacion del resumen al registro oficial como dato propio"},
    {"uso": "telemedicina con preconsulta automatizada",
     "riesgo": "derivar a consulta programada un cuadro que requeria atencion inmediata",
     "registro": "el cuestionario, la derivacion propuesta y el criterio de escalamiento",
     "firma": "el cierre de un contacto sin derivacion cuando hay signos de alarma declarados"},
    {"uso": "deteccion de riesgo en salud mental",
     "riesgo": "el falso positivo que estigmatiza y el falso negativo en riesgo suicida, con "
               "consecuencias asimetricas que el umbral unico no distingue",
     "registro": "la senal detectada, el umbral aplicado y la via de contacto humano activada",
     "firma": "cualquier intervencion o notificacion a terceros sobre el estado mental"},
    {"uso": "seleccion de pacientes para un ensayo clinico",
     "riesgo": "reproducir la subrepresentacion historica y producir evidencia que no aplica a "
               "la poblacion que luego recibe el tratamiento",
     "registro": "los criterios aplicados, los excluidos y la razon de exclusion",
     "firma": "la exclusion de un candidato elegible por criterio automatico"},
    {"uso": "priorizacion de lista de espera quirurgica",
     "riesgo": "trasladar a la cola una variable socioeconomica correlacionada con el "
               "diagnostico, y convertir una desigualdad en un criterio clinico",
     "registro": "el orden resultante, las variables que lo determinaron y las excepciones",
     "firma": "el descenso de posicion de un paciente ya priorizado"},
    {"uso": "monitoreo remoto de pacientes cronicos",
     "riesgo": "la alarma que no llega por fallo de conectividad y se interpreta como ausencia "
               "de evento",
     "registro": "la continuidad de la senal y los huecos de medicion, declarados como huecos",
     "firma": "la suspension de un seguimiento activo"},
    {"uso": "codificacion de diagnosticos para facturacion",
     "riesgo": "el sesgo hacia codigos de mayor reembolso, que contamina la estadistica "
               "epidemiologica de la que despues dependen las politicas",
     "registro": "el codigo sugerido, el finalmente asentado y la diferencia entre ambos",
     "firma": "la modificacion de un diagnostico ya asentado por un profesional"},
    {"uso": "chatbot de orientacion al paciente",
     "riesgo": "ser leido como consejo medico aunque el aviso legal diga lo contrario, porque "
               "el usuario no distingue el registro del lenguaje",
     "registro": "la conversacion completa y el momento exacto del aviso de no sustitucion",
     "firma": "toda indicacion concreta sobre medicacion, dosis o suspension de tratamiento"},
    {"uso": "estimacion de pronostico y expectativa de vida",
     "riesgo": "que una probabilidad poblacional se use como dato individual para decidir "
               "intensidad de cuidado",
     "registro": "el intervalo de confianza, no solo el valor central",
     "firma": "toda decision de limitacion del esfuerzo terapeutico"},
    {"uso": "deteccion de fraude en prestaciones de salud",
     "riesgo": "la suspension de cobertura a un afiliado legitimo por un patron de consumo "
               "atipico pero explicable",
     "registro": "el patron marcado, el descargo del afiliado y la resolucion",
     "firma": "la suspension o rechazo de una prestacion"},
    {"uso": "asignacion de turnos y sobreturnos",
     "riesgo": "optimizar la ocupacion del recurso y no el resultado del paciente, que son dos "
               "funciones distintas y a veces opuestas",
     "registro": "el criterio de asignacion y los casos reasignados",
     "firma": "la postergacion de un turno marcado como prioritario"},
    {"uso": "consentimiento informado asistido",
     "riesgo": "dar por comprendida una explicacion que el paciente no comprendio, y dejar un "
               "registro que dice lo contrario",
     "registro": "que se explico, en que idioma y como se verifico la comprension",
     "firma": "el consentimiento mismo, que no puede ser inferido de una interaccion"},
    {"uso": "vigilancia epidemiologica automatizada",
     "riesgo": "la alerta tardia por subregistro en las zonas con menos digitalizacion, que son "
               "las de mayor riesgo",
     "registro": "la cobertura real de la fuente y sus huecos geograficos",
     "firma": "la declaracion o el levantamiento de una alerta sanitaria"},
    {"uso": "robotica asistencial y cirugia asistida",
     "riesgo": "la zona gris de responsabilidad entre fabricante, institucion y profesional "
               "cuando el dispositivo actua dentro de parametros y el resultado es adverso",
     "registro": "los parametros de la intervencion y toda desviacion respecto del plan",
     "firma": "el cambio de plan quirurgico durante el acto"},
    {"uso": "transcripcion de la consulta en tiempo real",
     "riesgo": "el error de transcripcion en nombres de farmacos foneticamente proximos, que "
               "queda asentado como dicho por el profesional",
     "registro": "el audio o su huella, junto al texto, para poder cotejar",
     "firma": "el cierre de la historia clinica del dia"},
]
CLINICO_EN = {
    "triaje en guardia": "emergency-department triage",
    "lectura de imagenes radiologicas": "radiology image reading",
    "apoyo a la prescripcion": "prescribing support",
    "resumen automatico de historia clinica": "automated medical-record summarisation",
    "telemedicina con preconsulta automatizada": "telemedicine with automated intake",
    "deteccion de riesgo en salud mental": "mental-health risk detection",
    "seleccion de pacientes para un ensayo clinico": "clinical-trial patient selection",
    "priorizacion de lista de espera quirurgica": "surgical waiting-list prioritisation",
    "monitoreo remoto de pacientes cronicos": "remote monitoring of chronic patients",
    "codificacion de diagnosticos para facturacion": "diagnosis coding for billing",
    "chatbot de orientacion al paciente": "patient-guidance chatbot",
    "estimacion de pronostico y expectativa de vida": "prognosis and life-expectancy estimation",
    "deteccion de fraude en prestaciones de salud": "health-benefit fraud detection",
    "asignacion de turnos y sobreturnos": "appointment and overbooking allocation",
    "consentimiento informado asistido": "assisted informed consent",
    "vigilancia epidemiologica automatizada": "automated epidemiological surveillance",
    "robotica asistencial y cirugia asistida": "assistive robotics and robot-assisted surgery",
    "transcripcion de la consulta en tiempo real": "real-time consultation transcription",
}
CLINICO_PT = {
    "triaje en guardia": "triagem no pronto-socorro",
    "lectura de imagenes radiologicas": "leitura de imagens radiologicas",
    "apoyo a la prescripcion": "apoio a prescricao",
    "resumen automatico de historia clinica": "resumo automatico de prontuario",
    "telemedicina con preconsulta automatizada": "telemedicina com pre-consulta automatizada",
    "deteccion de riesgo en salud mental": "deteccao de risco em saude mental",
    "seleccion de pacientes para un ensayo clinico": "selecao de pacientes para ensaio clinico",
    "priorizacion de lista de espera quirurgica": "priorizacao de fila cirurgica",
    "monitoreo remoto de pacientes cronicos": "monitoramento remoto de pacientes cronicos",
    "codificacion de diagnosticos para facturacion": "codificacao de diagnosticos para faturamento",
    "chatbot de orientacion al paciente": "chatbot de orientacao ao paciente",
    "estimacion de pronostico y expectativa de vida": "estimativa de prognostico e expectativa de vida",
    "deteccion de fraude en prestaciones de salud": "deteccao de fraude em beneficios de saude",
    "asignacion de turnos y sobreturnos": "alocacao de consultas e encaixes",
    "consentimiento informado asistido": "consentimento informado assistido",
    "vigilancia epidemiologica automatizada": "vigilancia epidemiologica automatizada",
    "robotica asistencial y cirugia asistida": "robotica assistencial e cirurgia assistida",
    "transcripcion de la consulta en tiempo real": "transcricao da consulta em tempo real",
}

# ──────────────────────────────────────────── educacion: 16 usos por figura
# derecho: lo que el estudiante o la familia puede exigir, en concreto.
EDUCATIVOS = [
    {"uso": "correccion automatica de examenes",
     "riesgo": "penalizar la respuesta correcta expresada de forma no prevista, y que la nota "
               "quede firme porque nadie la reviso",
     "derecho": "conocer que la correccion fue automatica, pedir revision humana y que la "
                "revision no la haga el mismo sistema",
     "firma": "la nota definitiva y cualquier calificacion que condicione la promocion"},
    {"uso": "deteccion de plagio o de texto generado por IA",
     "riesgo": "el falso positivo, que es mas alto en quienes escriben en una lengua que no es "
               "su primera lengua y en quienes usan estructuras formulaicas",
     "derecho": "ver la evidencia concreta, no solo un porcentaje, y responder antes de que se "
                "abra un procedimiento disciplinario",
     "firma": "la apertura de un sumario academico y toda sancion"},
    {"uso": "tutor adaptativo que decide la secuencia de contenidos",
     "riesgo": "encerrar al estudiante en un nivel por un diagnostico inicial pobre, y que el "
               "sistema confirme su propia prediccion al no ofrecerle nunca el nivel siguiente",
     "derecho": "salir de la via asignada y acceder al contenido completo a pedido",
     "firma": "la reasignacion a un itinerario de menor exigencia"},
    {"uso": "admision y asignacion de vacantes",
     "riesgo": "usar el codigo postal o la escuela de origen como variable predictiva y "
               "reproducir la segregacion previa con apariencia de merito",
     "derecho": "conocer los criterios y su peso antes de postular, no despues del resultado",
     "firma": "el rechazo de una postulacion"},
    {"uso": "prediccion de abandono escolar",
     "riesgo": "que la etiqueta de riesgo llegue al docente antes que el apoyo, y opere como "
               "expectativa que se cumple sola",
     "derecho": "que la prediccion active un recurso concreto y no solo una marca en el legajo",
     "firma": "toda consecuencia administrativa derivada de la etiqueta"},
    {"uso": "vigilancia de examenes a distancia",
     "riesgo": "leer como fraude la conducta de un estudiante con discapacidad, con un entorno "
               "domestico ruidoso o sin espacio propio",
     "derecho": "ser evaluado por una via alternativa y que la grabacion se elimine en plazo",
     "firma": "la anulacion de un examen"},
    {"uso": "recomendacion de itinerario profesional",
     "riesgo": "estrechar la expectativa segun el perfil historico del grupo de pertenencia, en "
               "particular por genero en carreras tecnicas",
     "derecho": "recibir el abanico completo y conocer en que datos se basa la sugerencia",
     "firma": "ninguna: es orientacion, y presentarla como diagnostico ya es el error"},
    {"uso": "evaluacion docente automatizada",
     "riesgo": "medir lo que es facil de medir -asistencia, tiempo de respuesta- y no la "
               "ensenanza, y que de eso dependa la continuidad laboral",
     "derecho": "del docente: conocer los indicadores, su peso y poder impugnarlos",
     "firma": "toda decision sobre continuidad, promocion o remuneracion"},
    {"uso": "acreditacion y verificacion de titulos",
     "riesgo": "el rechazo de una credencial valida por un formato no previsto, y la aceptacion "
               "de una falsificada bien formateada",
     "derecho": "una via humana de verificacion cuando la automatica falla",
     "firma": "la denegacion de reconocimiento de un titulo"},
    {"uso": "asistente de escritura para trabajos academicos",
     "riesgo": "la frontera difusa entre apoyo y autoria, que cada institucion define distinto "
               "y el estudiante descubre al ser sancionado",
     "derecho": "una regla escrita y previa sobre que uso esta permitido en cada tarea",
     "firma": "la declaracion de autoria, que sigue siendo del estudiante"},
    {"uso": "datos de menores en plataformas educativas",
     "riesgo": "el uso secundario del dato escolar para perfilado comercial, por una clausula "
               "que la familia acepto sin leer al matricular",
     "derecho": "saber que se recoge, para que, por cuanto tiempo y poder negarlo sin perder "
                "el acceso al servicio educativo",
     "firma": "toda cesion a un tercero y todo uso distinto del educativo"},
    {"uso": "traduccion automatica de material de clase",
     "riesgo": "el error terminologico en materias tecnicas, que el estudiante no puede "
               "detectar porque justamente esta aprendiendo el termino",
     "derecho": "acceso al original y senalizacion de que el material es traduccion automatica",
     "firma": "la publicacion del material como version oficial de la catedra"},
    {"uso": "agrupamiento de estudiantes por nivel",
     "riesgo": "consolidar un agrupamiento inicial que despues nadie revisa, y que determina la "
               "trayectoria completa",
     "derecho": "revision periodica con criterio explicito y posibilidad de cambio",
     "firma": "la permanencia en un grupo por mas de un periodo sin revision"},
    {"uso": "generacion automatica de material didactico",
     "riesgo": "el error factual presentado con el tono de autoridad del material oficial, que "
               "es dificil de desmentir en el aula",
     "derecho": "saber que el material es generado y quien lo valido",
     "firma": "la validacion pedagogica del contenido"},
    {"uso": "deteccion de acoso en entornos escolares digitales",
     "riesgo": "el falso positivo sobre la jerga propia de la edad y el falso negativo en el "
               "acoso indirecto, que es el mas frecuente",
     "derecho": "del senalado: ser escuchado antes de cualquier medida",
     "firma": "toda medida disciplinaria y toda notificacion a las familias"},
    {"uso": "asignacion de becas y ayudas",
     "riesgo": "excluir por un dato administrativo faltante a quien mas necesita la ayuda, que "
               "suele ser quien tiene la documentacion mas incompleta",
     "derecho": "subsanar y ser evaluado con intervencion humana",
     "firma": "la denegacion de una beca"},
]
EDUCATIVO_EN = {
    "correccion automatica de examenes": "automated exam grading",
    "deteccion de plagio o de texto generado por IA": "plagiarism and AI-text detection",
    "tutor adaptativo que decide la secuencia de contenidos": "adaptive tutoring that sequences content",
    "admision y asignacion de vacantes": "admissions and place allocation",
    "prediccion de abandono escolar": "dropout prediction",
    "vigilancia de examenes a distancia": "remote exam proctoring",
    "recomendacion de itinerario profesional": "career-pathway recommendation",
    "evaluacion docente automatizada": "automated teacher evaluation",
    "acreditacion y verificacion de titulos": "credential and degree verification",
    "asistente de escritura para trabajos academicos": "writing assistance for academic work",
    "datos de menores en plataformas educativas": "children's data on education platforms",
    "traduccion automatica de material de clase": "machine translation of course material",
    "agrupamiento de estudiantes por nivel": "ability grouping of students",
    "generacion automatica de material didactico": "automated generation of teaching material",
    "deteccion de acoso en entornos escolares digitales": "bullying detection in school platforms",
    "asignacion de becas y ayudas": "scholarship and grant allocation",
}
EDUCATIVO_PT = {
    "correccion automatica de examenes": "correcao automatica de provas",
    "deteccion de plagio o de texto generado por IA": "deteccao de plagio e de texto gerado por IA",
    "tutor adaptativo que decide la secuencia de contenidos": "tutor adaptativo que define a sequencia de conteudos",
    "admision y asignacion de vacantes": "admissao e alocacao de vagas",
    "prediccion de abandono escolar": "predicao de evasao escolar",
    "vigilancia de examenes a distancia": "fiscalizacao remota de provas",
    "recomendacion de itinerario profesional": "recomendacao de itinerario profissional",
    "evaluacion docente automatizada": "avaliacao docente automatizada",
    "acreditacion y verificacion de titulos": "acreditacao e verificacao de diplomas",
    "asistente de escritura para trabajos academicos": "assistente de escrita para trabalhos academicos",
    "datos de menores en plataformas educativas": "dados de menores em plataformas educacionais",
    "traduccion automatica de material de clase": "traducao automatica de material de aula",
    "agrupamiento de estudiantes por nivel": "agrupamento de estudantes por nivel",
    "generacion automatica de material didactico": "geracao automatica de material didatico",
    "deteccion de acoso en entornos escolares digitales": "deteccao de assedio em ambientes escolares digitais",
    "asignacion de becas y ayudas": "alocacao de bolsas e auxilios",
}

# ──────────────────────────────────── trabajo del futuro: 16 decisiones
# Se ordena por DECISION laboral concreta, no por «empleos que desaparecen»:
# la pregunta con consecuencia juridica es quien decide y con que registro.
LABORALES = [
    {"uso": "cribado automatico de candidaturas",
     "riesgo": "descartar por un hueco en el curriculo que corresponde a una licencia por "
               "maternidad o a una enfermedad, variables que la ley protege",
     "impugnable": "si no se puede exhibir el criterio de descarte ni quien lo fijo",
     "firma": "el descarte definitivo de una candidatura"},
    {"uso": "entrevista en video analizada por IA",
     "riesgo": "puntuar rasgos de expresion correlacionados con origen, edad o neurodivergencia "
               "y presentarlos como competencias",
     "impugnable": "si no hubo aviso previo ni alternativa sin analisis automatico",
     "firma": "la decision de no avanzar a la etapa siguiente"},
    {"uso": "evaluacion de desempeno por metricas automaticas",
     "riesgo": "medir actividad en lugar de resultado y castigar el trabajo que no deja rastro "
               "digital, como la formacion de un compañero",
     "impugnable": "si el trabajador no conocia los indicadores ni su peso antes del periodo",
     "firma": "la calificacion final y todo efecto sobre remuneracion"},
    {"uso": "asignacion algoritmica de turnos",
     "riesgo": "la jornada fragmentada que cumple el maximo legal pero destruye la "
               "previsibilidad, y que no aparece en ningun indicador de cumplimiento",
     "impugnable": "si no se respeta el preaviso ni el descanso pactado",
     "firma": "el cambio de turno con menos preaviso que el convenido"},
    {"uso": "despido o desvinculacion sugerida por un sistema",
     "riesgo": "trasladar a la decision una correlacion espuria -antiguedad, uso de licencias- "
               "con apariencia de objetividad",
     "impugnable": "siempre: la causal tiene que ser humana, expresa y anterior",
     "firma": "toda extincion del vinculo, sin excepcion"},
    {"uso": "vigilancia de productividad en teletrabajo",
     "riesgo": "capturar datos del domicilio y de terceros que no son parte de la relacion "
               "laboral",
     "impugnable": "si la medida no es proporcionada ni fue informada con alcance preciso",
     "firma": "toda medida disciplinaria basada en lo capturado"},
    {"uso": "fijacion dinamica de remuneracion o tarifa",
     "riesgo": "la opacidad del calculo, que impide verificar si se cumplio lo pactado y "
               "convierte el salario en una variable no auditable",
     "impugnable": "si el trabajador no puede reconstruir como se llego a su liquidacion",
     "firma": "la aprobacion del periodo de liquidacion"},
    {"uso": "asignacion de tareas en plataformas de reparto y transporte",
     "riesgo": "la desconexion o el bloqueo de cuenta sin causa comunicada, que opera como "
               "sancion sin procedimiento",
     "impugnable": "si no hay via de reclamo con respuesta humana en plazo",
     "firma": "el bloqueo o la baja de la cuenta"},
    {"uso": "deteccion de fuga de informacion por parte de empleados",
     "riesgo": "leer comunicacion sindical o personal como exfiltracion, con efecto directo "
               "sobre la libertad sindical",
     "impugnable": "si alcanza comunicaciones excluidas del poder de direccion",
     "firma": "toda denuncia interna o externa sobre una persona identificada"},
    {"uso": "planificacion de reconversion y recualificacion",
     "riesgo": "ofrecer formacion para puestos que el mismo plan va a automatizar, y computarla "
               "como cumplida",
     "impugnable": "si la formacion no habilita una funcion efectivamente existente",
     "firma": "la declaracion de un puesto como redundante"},
    {"uso": "clasificacion de la relacion como autonoma o dependiente",
     "riesgo": "que el grado real de direccion lo ejerza un sistema y la relacion se declare "
               "autonoma porque no hay un jefe humano visible",
     "impugnable": "si el sistema fija tiempo, precio y modo de la tarea",
     "firma": "la calificacion juridica del vinculo, que no la decide el software"},
    {"uso": "prediccion de rotacion de personal",
     "riesgo": "actuar sobre la prediccion y provocarla, excluyendo de proyectos a quien el "
               "modelo marco como proximo a irse",
     "impugnable": "si la etiqueta tuvo efecto sin que la persona lo supiera",
     "firma": "toda exclusion de oportunidad derivada de la etiqueta"},
    {"uso": "accesibilidad y ajustes razonables asistidos por IA",
     "riesgo": "tratar el ajuste como excepcion a justificar en cada ciclo, con la carga de "
               "prueba siempre del lado del trabajador",
     "impugnable": "si el ajuste concedido se revoca por un criterio automatico",
     "firma": "la denegacion o revocacion de un ajuste"},
    {"uso": "negociacion colectiva sobre introduccion de agentes",
     "riesgo": "presentar la automatizacion como hecho tecnico consumado y sacarla del ambito "
               "negociable",
     "impugnable": "si se omitio la informacion y consulta previstas",
     "firma": "el acuerdo o su falta, que es un hecho juridico de las partes"},
    {"uso": "atribucion de autoria y propiedad de lo producido con IA",
     "riesgo": "la zona gris sobre quien es titular de lo generado en horario laboral con "
               "herramienta de la empresa y criterio del trabajador",
     "impugnable": "si no hay clausula previa y expresa",
     "firma": "la cesion de derechos, que requiere acuerdo y no uso"},
    {"uso": "seguridad e higiene con sensores y vision por computadora",
     "riesgo": "usar la deteccion de incumplimiento para sancionar en lugar de para corregir la "
               "condicion que lo provoca",
     "impugnable": "si el dato de seguridad se usa con fin disciplinario no declarado",
     "firma": "toda sancion derivada de un registro de seguridad"},
]
LABORAL_EN = {
    "cribado automatico de candidaturas": "automated CV screening",
    "entrevista en video analizada por IA": "AI-analysed video interviews",
    "evaluacion de desempeno por metricas automaticas": "performance review by automated metrics",
    "asignacion algoritmica de turnos": "algorithmic shift scheduling",
    "despido o desvinculacion sugerida por un sistema": "system-suggested dismissal",
    "vigilancia de productividad en teletrabajo": "productivity monitoring in remote work",
    "fijacion dinamica de remuneracion o tarifa": "dynamic pay or rate setting",
    "asignacion de tareas en plataformas de reparto y transporte": "task allocation on delivery and ride platforms",
    "deteccion de fuga de informacion por parte de empleados": "insider data-leak detection",
    "planificacion de reconversion y recualificacion": "reskilling and redeployment planning",
    "clasificacion de la relacion como autonoma o dependiente": "employment-status classification",
    "prediccion de rotacion de personal": "employee-attrition prediction",
    "accesibilidad y ajustes razonables asistidos por IA": "AI-assisted accessibility and reasonable adjustments",
    "negociacion colectiva sobre introduccion de agentes": "collective bargaining over agent deployment",
    "atribucion de autoria y propiedad de lo producido con IA": "authorship and ownership of AI-assisted output",
    "seguridad e higiene con sensores y vision por computadora": "health and safety with sensors and computer vision",
}
LABORAL_PT = {
    "cribado automatico de candidaturas": "triagem automatica de candidaturas",
    "entrevista en video analizada por IA": "entrevista em video analisada por IA",
    "evaluacion de desempeno por metricas automaticas": "avaliacao de desempenho por metricas automaticas",
    "asignacion algoritmica de turnos": "escala de turnos algoritmica",
    "despido o desvinculacion sugerida por un sistema": "demissao sugerida por um sistema",
    "vigilancia de productividad en teletrabajo": "monitoramento de produtividade no teletrabalho",
    "fijacion dinamica de remuneracion o tarifa": "definicao dinamica de remuneracao ou tarifa",
    "asignacion de tareas en plataformas de reparto y transporte": "alocacao de tarefas em plataformas de entrega e transporte",
    "deteccion de fuga de informacion por parte de empleados": "deteccao de vazamento por parte de empregados",
    "planificacion de reconversion y recualificacion": "planejamento de requalificacao",
    "clasificacion de la relacion como autonoma o dependiente": "classificacao do vinculo como autonomo ou empregaticio",
    "prediccion de rotacion de personal": "predicao de rotatividade de pessoal",
    "accesibilidad y ajustes razonables asistidos por IA": "acessibilidade e ajustes razoaveis assistidos por IA",
    "negociacion colectiva sobre introduccion de agentes": "negociacao coletiva sobre introducao de agentes",
    "atribucion de autoria y propiedad de lo producido con IA": "autoria e titularidade do produzido com IA",
    "seguridad e higiene con sensores y vision por computadora": "seguranca e saude com sensores e visao computacional",
}

# ──────────────────────────────── el AFECTADO: la pregunta en primera persona
# Esta es la dimension que mas rinde en AEO porque es el fraseo del buscador,
# no el del experto. `que_paso` arma la pregunta; `primero` es la accion
# inmediata; `exigible` es lo que se puede pedir por escrito.
AFECTADO = [
    {"rol": "paciente", "ambito": "salud",
     "que_paso": "mi medico uso un sistema de inteligencia artificial en mi diagnostico",
     "primero": "pedir por escrito la historia clinica completa, incluida la mencion del "
                "sistema utilizado y su version",
     "exigible": "que conste quien valido la salida del sistema y que la decision la firmo un "
                 "profesional identificable"},
    {"rol": "paciente", "ambito": "salud",
     "que_paso": "me negaron una cobertura y me dijeron que la decidio un sistema automatico",
     "primero": "solicitar la resolucion por escrito con la causal concreta, no la referencia "
                "al sistema",
     "exigible": "revision humana del rechazo y el criterio aplicado a mi caso"},
    {"rol": "familiar", "ambito": "salud",
     "que_paso": "un algoritmo cambio la prioridad de mi familiar en una lista de espera",
     "primero": "pedir el registro del orden anterior y posterior, y la razon del cambio",
     "exigible": "que toda modificacion de una prioridad ya asignada tenga firma humana"},
    {"rol": "estudiante", "ambito": "educacion",
     "que_paso": "me acusaron de usar inteligencia artificial en un trabajo que escribi yo",
     "primero": "pedir la evidencia concreta y no el porcentaje, y dejar constancia del "
                "descargo antes de cualquier procedimiento",
     "exigible": "que el detector no sea la unica prueba y que la revision no la haga el mismo "
                 "sistema que acuso"},
    {"rol": "estudiante", "ambito": "educacion",
     "que_paso": "un sistema me corrigio el examen y la nota no refleja lo que respondi",
     "primero": "solicitar revision humana por escrito dentro del plazo del reglamento",
     "exigible": "saber que la correccion fue automatica y que la revision la haga una persona"},
    {"rol": "familia", "ambito": "educacion",
     "que_paso": "a mi hijo lo clasifico un algoritmo en un grupo de nivel mas bajo",
     "primero": "pedir el criterio, los datos usados y la fecha de la ultima revision",
     "exigible": "revision periodica con criterio explicito y posibilidad efectiva de cambio"},
    {"rol": "familia", "ambito": "educacion",
     "que_paso": "la escuela usa una plataforma que recoge datos de mi hijo menor de edad",
     "primero": "pedir el detalle de que se recoge, con que finalidad y por cuanto tiempo",
     "exigible": "negar el uso secundario sin perder el acceso al servicio educativo"},
    {"rol": "postulante", "ambito": "trabajo",
     "que_paso": "me rechazaron en una busqueda laboral y nunca hablé con una persona",
     "primero": "pedir por escrito el criterio de descarte y si intervino un sistema automatico",
     "exigible": "intervencion humana en la decision y conocer las variables que pesaron"},
    {"rol": "trabajador", "ambito": "trabajo",
     "que_paso": "mi evaluacion de desempeno la hizo un sistema con metricas que no conocia",
     "primero": "pedir los indicadores, su peso y el periodo medido, y dejar constancia de la "
                "objecion",
     "exigible": "que los indicadores sean previos y conocidos, y poder impugnar la calificacion"},
    {"rol": "trabajador", "ambito": "trabajo",
     "que_paso": "me bloquearon la cuenta de una plataforma y perdi mi fuente de ingreso",
     "primero": "reclamar por la via formal y conservar la constancia con fecha",
     "exigible": "causa comunicada, plazo de respuesta y revision por una persona"},
    {"rol": "trabajador", "ambito": "trabajo",
     "que_paso": "mi empleador instalo un sistema que vigila lo que hago en mi casa",
     "primero": "pedir el alcance exacto de la captura y la norma interna que la habilita",
     "exigible": "proporcionalidad, informacion previa y exclusion de datos de terceros"},
    {"rol": "ciudadano", "ambito": "gobernanza",
     "que_paso": "un organismo publico me denego un tramite con una decision automatizada",
     "primero": "pedir la resolucion fundada y la mencion expresa de que hubo decision "
                "automatizada",
     "exigible": "fundamentacion, via de recurso y revision humana del rechazo"},
    {"rol": "consumidor", "ambito": "gobernanza",
     "que_paso": "un agente de inteligencia artificial contrato algo en mi nombre",
     "primero": "desconocer la operacion por escrito y pedir el registro de la autorizacion que "
                "el agente invoco",
     "exigible": "prueba de la autorizacion y del limite dentro del cual actuo el agente"},
    {"rol": "ciudadano", "ambito": "gobernanza",
     "que_paso": "un sistema me identifico por error como otra persona",
     "primero": "pedir la rectificacion y el registro de los sistemas a los que ya se propago "
                "el dato",
     "exigible": "rectificacion en origen y notificacion a todos los destinatarios del error"},
]
AFECTADO_EN = {
    "paciente": "patient", "familiar": "relative", "estudiante": "student",
    "familia": "family", "postulante": "job applicant", "trabajador": "worker",
    "ciudadano": "citizen", "consumidor": "consumer",
}
AFECTADO_PT = {
    "paciente": "paciente", "familiar": "familiar", "estudiante": "estudante",
    "familia": "familia", "postulante": "candidato", "trabajador": "trabalhador",
    "ciudadano": "cidadao", "consumidor": "consumidor",
}

# ───────────────────────────── que se puede EXIGIR, por rol: 10 pedidos
# Pedidos redactados para copiar y pegar en un escrito. Es contenido util,
# no relleno: es la forma en que la doctrina se vuelve accionable.
EXIGIBLE = [
    {"pedido": "la identificacion del sistema y su version",
     "porque": "sin version no se puede saber que modelo decidio, y los modelos cambian sin "
               "aviso entre una decision y la siguiente"},
    {"pedido": "la constancia de intervencion humana",
     "porque": "es la diferencia entre una decision asistida y una decision automatizada, y de "
               "eso depende el regimen que se aplica"},
    {"pedido": "el criterio aplicado al caso concreto",
     "porque": "la politica general no explica el resultado individual, y es el resultado "
               "individual el que se impugna"},
    {"pedido": "el registro de la actuacion con fecha y hora",
     "porque": "sin traza no hay forma de reconstruir que se decidio ni en que orden, y la "
               "carga de la prueba recae sobre quien no tiene el registro"},
    {"pedido": "la via de reclamo y su plazo de respuesta",
     "porque": "un derecho sin procedimiento ni plazo no es exigible en la practica"},
    {"pedido": "la identidad del responsable humano",
     "porque": "la responsabilidad no puede quedar difusa entre proveedor, operador y "
               "fabricante del modelo"},
    {"pedido": "los datos usados y su origen",
     "porque": "un dato incorrecto o desactualizado explica la mayor parte de los errores, y "
               "es lo primero que se puede rectificar"},
    {"pedido": "la posibilidad de una via alternativa sin sistema automatico",
     "porque": "cuando la via automatica falla para un perfil, la alternativa es lo unico que "
               "evita la exclusion"},
    {"pedido": "el plazo de conservacion y la eliminacion efectiva",
     "porque": "el dato que sobrevive a su finalidad se reutiliza para otra, que es como "
               "empieza casi todo uso indebido"},
    {"pedido": "la notificacion a terceros a los que se propago el dato",
     "porque": "rectificar en origen no alcanza si el error ya circula en otros sistemas"},
]
EXIGIBLE_EN = {
    "la identificacion del sistema y su version": "identification of the system and its version",
    "la constancia de intervencion humana": "evidence of human involvement",
    "el criterio aplicado al caso concreto": "the criterion applied to the specific case",
    "el registro de la actuacion con fecha y hora": "a timestamped record of the action",
    "la via de reclamo y su plazo de respuesta": "the complaint channel and its response deadline",
    "la identidad del responsable humano": "the identity of the accountable human",
    "los datos usados y su origen": "the data used and its provenance",
    "la posibilidad de una via alternativa sin sistema automatico": "the option of a non-automated alternative route",
    "el plazo de conservacion y la eliminacion efectiva": "the retention period and effective deletion",
    "la notificacion a terceros a los que se propago el dato": "notification to third parties the data reached",
}
EXIGIBLE_PT = {
    "la identificacion del sistema y su version": "a identificacao do sistema e sua versao",
    "la constancia de intervencion humana": "a comprovacao de intervencao humana",
    "el criterio aplicado al caso concreto": "o criterio aplicado ao caso concreto",
    "el registro de la actuacion con fecha y hora": "o registro da atuacao com data e hora",
    "la via de reclamo y su plazo de respuesta": "o canal de reclamacao e seu prazo de resposta",
    "la identidad del responsable humano": "a identidade do responsavel humano",
    "los datos usados y su origen": "os dados usados e sua origem",
    "la posibilidad de una via alternativa sin sistema automatico": "a possibilidade de uma via alternativa sem sistema automatico",
    "el plazo de conservacion y la eliminacion efectiva": "o prazo de conservacao e a eliminacao efetiva",
    "la notificacion a terceros a los que se propago el dato": "a notificacao a terceiros que receberam o dado",
}

AMBITO_EN = {"salud": "healthcare", "educacion": "education",
             "trabajo": "the workplace", "gobernanza": "public administration"}
AMBITO_PT = {"salud": "saude", "educacion": "educacao",
             "trabajo": "o trabalho", "gobernanza": "a administracao publica"}
