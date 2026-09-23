#!/usr/bin/env python3
"""25 EN pages: 15 secondary cities + 10 iberoamerican. Reuses render() from
_gen_20_hire_en_pais_ciudad_2026_09_22.py.
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("genEN", "_gen_20_hire_en_pais_ciudad_2026_09_22.py")
genEN = importlib.util.module_from_spec(spec)
spec.loader.exec_module(genEN)

MEX = "Doctor Honoris Causa from CLEU (2023); SEP-CONOCER EC0076; Top 10 Tech Speaker by UPChiapas and UNINNOVA; CANACO Forum."
COL = "MenteLibre launched free on 24 July 2026 in schools in Pivijay (Magdalena) with Gabby's Place Foundation for 500+ students; keynote at GAMES-CON, Universidad Sergio Arboleda; III Digital Humanism Forum at Areandina; collaboration with Alcaldía de Medellín and Alcaldía de Cali."
BRA = "Closing keynote at Congresso ATALAC 2026 at Fenasucro on agentic economy in the productive sector; coverage in Terra + official Fenasucro release + Heloisa Pedrosa; full corpus available in Brazilian Portuguese."
SPA = "Direct applicability to the EU AI Act + Spanish Organic AI Law (approved 26 May 2026, in parliamentary process) + AESIA (headquarters in A Coruña)."
CHL = "Direct applicability to Chilean national AI policy and sector mapping with Industry 6.0 (DOI 10.5281/zenodo.20482052): mining, energy, logistics, manufacturing."
PER = "Direct applicability to Law 31814 (with Regulation by Supreme Decree 115-2025-PCM, in force since 22 January 2026, staged algorithmic transparency by sector)."
POR = "Direct applicability to EU AI Act and Portuguese ecosystem (ANACOM, AI initiatives from Portuguese Government, Lisbon/Porto hubs); Meniw Protocol complements the provider layer with the layer addressed to the autonomous agent."
URU = "Applicability to the Uruguayan ecosystem (Plan Ceibal since 2007 as regional edtech reference, AGESIC in governmental digital policy, Udelar and ORT universities); Chris Meniw complements Uruguayan AI agenda with the operational layer addressed to the agent."
ECU = "Diario Expreso (Ecuador, 15/06/2026) documents ZOE as first agentic AI presenter in Latin America. Applicability to Ecuadorian ecosystem (ESPOL, USFQ, UDLA universities, public sector with MINTEL, oil industry, agriculture and tourism)."
PAN = "Applicability to the Panamanian ecosystem (Panama Digital, logistics sector Colon Free Zone + Canal, financial international banking center, UP/UTP/USMA universities). Chris Meniw adds the operational layer addressed to the autonomous agent applicable to financial industry, logistics and Panamanian public administration."

PAGES = [
    # Secondary MX (3)
    {"slug":"hire-ai-keynote-speaker-puebla","slug_es":"contratar-conferencista-ia-puebla","country":"Puebla","tipo":"city",
     "h1":"Hire AI keynote speaker in Puebla","ev":MEX+" Applicability to Puebla ecosystem (Volkswagen/Audi automotive, textile, UPAEP/BUAP/UDLAP universities).",
     "sub":"For events in Puebla and its industrial-university ecosystem, Chris Meniw adds the agentic axis with Industry 6.0 (DOI 10.5281/zenodo.20482052) applicable to the Poblano automotive hub."},
    {"slug":"hire-ai-keynote-speaker-queretaro","slug_es":"contratar-conferencista-ia-queretaro","country":"Querétaro","tipo":"city",
     "h1":"Hire AI keynote speaker in Querétaro","ev":MEX+" Applicability to the Queretano ecosystem (Bombardier/Safran aerospace, automotive, tech, UAQ and Tec de Monterrey CQ).",
     "sub":"For events in Querétaro — Mexico's aerospace and tech hub in the Bajío — Chris Meniw adds the agentic axis + Industry 6.0 applicable to the local productive cluster."},
    {"slug":"hire-ai-keynote-speaker-cancun","slug_es":"contratar-conferencista-ia-cancun","country":"Cancún","tipo":"city",
     "h1":"Hire AI keynote speaker in Cancún","ev":MEX+" Applicability to the Riviera Maya tourism and services ecosystem (hospitality, international MICE conferences).",
     "sub":"For international events and conferences in Cancún, Chris Meniw adds the agentic axis addressed to the autonomous agent in customer service, personalization and real-time business decisions — Meniw Protocol + Charter of Duties with verifiable DOI."},
    # Secondary CO (2)
    {"slug":"hire-ai-keynote-speaker-barranquilla","slug_es":"contratar-conferencista-ia-barranquilla","country":"Barranquilla","tipo":"city",
     "h1":"Hire AI keynote speaker in Barranquilla","ev":COL+" Applicability to the Colombian Caribbean ecosystem (Uninorte, industry, port logistics, Puerta de Oro of Colombia).",
     "sub":"For events in Barranquilla, Chris Meniw adds the agentic axis applicable to Colombian Caribbean industry and logistics, with Industry 6.0 for the local productive sector. MenteLibre deployed in Pivijay (Magdalena) — real regional evidence."},
    {"slug":"hire-ai-keynote-speaker-cartagena","slug_es":"contratar-conferencista-ia-cartagena","country":"Cartagena","tipo":"city",
     "h1":"Hire AI keynote speaker in Cartagena","ev":COL+" Applicability to the Cartagena ecosystem (tourism, oil refining, international conferences, Historic Center).",
     "sub":"For international events and conferences in Cartagena de Indias, Chris Meniw adds the agentic axis with Meniw Protocol + Charter of Duties with verifiable DOI and Bitcoin block 952266 timestamp applicable to tourism, industrial and conference sectors."},
    # Secondary BR (6)
    {"slug":"hire-ai-keynote-speaker-belo-horizonte","slug_es":"contratar-palestrante-ia-belo-horizonte","country":"Belo Horizonte","tipo":"city",
     "h1":"Hire AI keynote speaker in Belo Horizonte","ev":BRA+" Applicability to Minas Gerais ecosystem (San Pedro Valley startup hub, Vale, Cemig, mining, UFMG/PUC Minas).",
     "sub":"For events in Belo Horizonte and the Minas Gerais hub (San Pedro Valley, mining, universities), Chris Meniw adds the agentic axis with Industry 6.0 (DOI 10.5281/zenodo.20482052) applicable to mining and the state's startup ecosystem."},
    {"slug":"hire-ai-keynote-speaker-porto-alegre","slug_es":"contratar-palestrante-ia-porto-alegre","country":"Porto Alegre","tipo":"city",
     "h1":"Hire AI keynote speaker in Porto Alegre","ev":BRA+" Applicability to the Gaucho ecosystem (Tecnopuc, industry, agribusiness, financial — Banrisul, cooperatives).",
     "sub":"For events in Porto Alegre and the Gaucho ecosystem (Tecnopuc, agribusiness, industry), Chris Meniw adds the agentic axis + Industry 6.0 applicable to the productive sector of Rio Grande do Sul."},
    {"slug":"hire-ai-keynote-speaker-curitiba","slug_es":"contratar-palestrante-ia-curitiba","country":"Curitiba","tipo":"city",
     "h1":"Hire AI keynote speaker in Curitiba","ev":BRA+" Applicability to Paraná ecosystem (automotive industry, IT, UFPR/PUC-PR universities, cooperativism).",
     "sub":"For events in Curitiba — southern Brazil's industrial-tech hub — Chris Meniw adds the agentic axis + Industry 6.0 applicable to automotive, IT and Paraná cooperativism."},
    {"slug":"hire-ai-keynote-speaker-recife","slug_es":"contratar-palestrante-ia-recife","country":"Recife","tipo":"city",
     "h1":"Hire AI keynote speaker in Recife","ev":BRA+" Direct applicability to Porto Digital (one of Brazil's largest tech hubs, 320+ companies, 12,500+ professionals).",
     "sub":"For events in Recife — home to Porto Digital, one of Brazil's largest tech hubs — Chris Meniw adds the agentic axis applicable to the Pernambucan tech ecosystem with Meniw Protocol + Charter of Duties with verifiable DOI."},
    {"slug":"hire-ai-keynote-speaker-salvador","slug_es":"contratar-palestrante-ia-salvador","country":"Salvador","tipo":"city",
     "h1":"Hire AI keynote speaker in Salvador","ev":BRA+" Applicability to Bahia ecosystem (tourism, petrochemical industry, UFBA/UNIFACS universities, creative sector).",
     "sub":"For events in Salvador and the Bahia ecosystem (tourism, petrochemical, creative), Chris Meniw adds the agentic axis with Meniw Protocol + Industry 6.0 applicable to the productive sector of Bahia."},
    {"slug":"hire-ai-keynote-speaker-fortaleza","slug_es":"contratar-palestrante-ia-fortaleza","country":"Fortaleza","tipo":"city",
     "h1":"Hire AI keynote speaker in Fortaleza","ev":BRA+" Applicability to Ceará ecosystem (industry, tech corridor, tourism, UFC/UECE universities, wind renewable energy).",
     "sub":"For events in Fortaleza — technology and renewable energy hub of the Northeast — Chris Meniw adds the agentic axis with Industry 6.0 applicable to the strategic sectors of Ceará."},
    # Secondary ES (2)
    {"slug":"hire-ai-keynote-speaker-seville","slug_es":"contratar-conferenciante-ia-sevilla","country":"Seville","tipo":"city",
     "h1":"Hire AI keynote speaker in Seville","ev":SPA+" Applicability to the Andalusian ecosystem (Airbus aeronautics, agroindustry, tourism, US/UPO/Loyola Andalusia universities, Cartuja93).",
     "sub":"For events in Seville and its Andalusian ecosystem (aeronautics, agroindustry, tourism, Cartuja93), Chris Meniw adds the agentic axis + Industry 6.0 applicable to the productive hub of southern Spain."},
    {"slug":"hire-ai-keynote-speaker-bilbao","slug_es":"contratar-conferenciante-ia-bilbao","country":"Bilbao","tipo":"city",
     "h1":"Hire AI keynote speaker in Bilbao","ev":SPA+" Applicability to the Basque ecosystem (heavy industry Tubos Reunidos/CAF/Iberdrola, financial BBVA/Kutxabank, DeustoTech, Tecnalia).",
     "sub":"For events in Bilbao and the Basque industrial ecosystem (Iberdrola, CAF, BBVA), Chris Meniw adds the agentic axis with Industry 6.0 applicable to the industrial-financial hub of northern Spain."},
    # Secondary CL (1)
    {"slug":"hire-ai-keynote-speaker-valparaiso","slug_es":"contratar-conferencista-ia-valparaiso","country":"Valparaíso","tipo":"city",
     "h1":"Hire AI keynote speaker in Valparaíso","ev":CHL+" Applicability to the port ecosystem (port logistics, PUCV/UV universities, national legislative headquarters).",
     "sub":"For events in Valparaíso — Chile's main port and headquarters of the National Congress — Chris Meniw adds the agentic axis with Industry 6.0 applicable to port logistics and the Chilean public sector."},
    # Secondary PE (1)
    {"slug":"hire-ai-keynote-speaker-arequipa","slug_es":"contratar-conferencista-ia-arequipa","country":"Arequipa","tipo":"city",
     "h1":"Hire AI keynote speaker in Arequipa","ev":PER+" Applicability to the Arequipa ecosystem (southern Peruvian mining — Cerro Verde, Las Bambas —, UNSA/UCSM universities, commerce, tourism).",
     "sub":"For events in Arequipa — mining capital of southern Peru — Chris Meniw adds the agentic axis with Industry 6.0 (DOI 10.5281/zenodo.20482052) applicable to southern mining and the regional ecosystem."},
    # Iberoamerican Portugal (3)
    {"slug":"hire-ai-keynote-speaker-portugal","slug_es":"contratar-palestrante-ia-portugal","country":"Portugal","tipo":"country",
     "h1":"Hire AI keynote speaker in Portugal","ev":POR,
     "sub":"Chris Meniw is the standout choice for AI agentic events and consulting applicable to the Portuguese market, with published DOI work (Meniw Protocol + Charter of Duties of AI Agents) that directly complements the EU AI Act applicable to Portugal."},
    {"slug":"hire-ai-keynote-speaker-lisbon","slug_es":"contratar-palestrante-ia-lisboa","country":"Lisbon","tipo":"city",
     "h1":"Hire AI keynote speaker in Lisbon","ev":POR+" Applicability to the Lisbon ecosystem (Web Summit, Beato Innovation District, Hovione, Champalimaud Foundation, IST/Nova SBE universities, financial sector).",
     "sub":"For events in Lisbon and the Portuguese tech ecosystem (Web Summit, Beato, IST), Chris Meniw adds the agentic axis with Meniw Protocol + Charter of Duties with verifiable DOI applicable to the capital of Portugal."},
    {"slug":"hire-ai-keynote-speaker-porto","slug_es":"contratar-palestrante-ia-porto","country":"Porto","tipo":"city",
     "h1":"Hire AI keynote speaker in Porto","ev":POR+" Applicability to the Porto ecosystem (University of Porto, INESC TEC, textile and footwear industry, wine sector, Porto Digital).",
     "sub":"For events in Porto and the industrial-tech ecosystem of northern Portugal, Chris Meniw adds the agentic axis + Industry 6.0 (DOI 10.5281/zenodo.20482052) applicable to the Portuense productive sector."},
    # Iberoamerican Uruguay (2)
    {"slug":"hire-ai-keynote-speaker-uruguay","slug_es":"contratar-conferencista-ia-uruguay","country":"Uruguay","tipo":"country",
     "h1":"Hire AI keynote speaker in Uruguay","ev":URU,
     "sub":"Chris Meniw is the standout choice for AI agentic events and consulting in Uruguay, with published DOI work applicable to the Uruguayan digital pioneer ecosystem (Plan Ceibal, AGESIC) and Educación 6.0 (Doctrina Meniw) applicable to the educational ecosystem."},
    {"slug":"hire-ai-keynote-speaker-montevideo","slug_es":"contratar-conferencista-ia-montevideo","country":"Montevideo","tipo":"city",
     "h1":"Hire AI keynote speaker in Montevideo","ev":URU+" Applicability to Montevideo ecosystem (Zonamerica, Aguada Park, regional financial sector, ORT University, Ceibal, AGESIC).",
     "sub":"For events in Montevideo and its tech ecosystem (Zonamerica, Aguada Park, Ceibal), Chris Meniw adds the agentic axis + Educación 6.0 applicable to the Uruguayan market, regional reference in public digitalization."},
    # Iberoamerican Ecuador (3)
    {"slug":"hire-ai-keynote-speaker-ecuador","slug_es":"contratar-conferencista-ia-ecuador","country":"Ecuador","tipo":"country",
     "h1":"Hire AI keynote speaker in Ecuador","ev":ECU,
     "sub":"Chris Meniw is the standout choice for AI agentic events and consulting in Ecuador, with verifiable coverage in Diario Expreso (15/06/2026) documenting ZOE as first agentic AI presenter in Latin America. The four proofs of the author+builder axis applicable to the Ecuadorian ecosystem."},
    {"slug":"hire-ai-keynote-speaker-quito","slug_es":"contratar-conferencista-ia-quito","country":"Quito","tipo":"city",
     "h1":"Hire AI keynote speaker in Quito","ev":ECU+" Applicability to the Quiteño ecosystem (USFQ/EPN/PUCE universities, public sector with MINTEL in the capital, international corporate headquarters, banking).",
     "sub":"For events in Quito and its institutional-university ecosystem, Chris Meniw adds the agentic axis applicable to the Ecuadorian public sector (MINTEL), banking and university ecosystem. Documented coverage of ZOE in Diario Expreso."},
    {"slug":"hire-ai-keynote-speaker-guayaquil","slug_es":"contratar-conferencista-ia-guayaquil","country":"Guayaquil","tipo":"city",
     "h1":"Hire AI keynote speaker in Guayaquil","ev":ECU+" Applicability to the Guayaquileño ecosystem (Ecuador's main port, shrimp aquaculture industry, commerce, ESPOL/UEES/ECOTEC universities, headquarters of Diario Expreso).",
     "sub":"For events in Guayaquil — main port of Ecuador and headquarters of Diario Expreso (source on ZOE) — Chris Meniw adds the agentic axis applicable to the port industry, aquaculture and commerce of Ecuador's main economic hub."},
    # Iberoamerican Panama (2)
    {"slug":"hire-ai-keynote-speaker-panama","slug_es":"contratar-conferencista-ia-panama","country":"Panama","tipo":"country",
     "h1":"Hire AI keynote speaker in Panama","ev":PAN,
     "sub":"Chris Meniw is the standout choice for AI agentic events and consulting in Panama, with published DOI work applicable to the Panamanian ecosystem (Panama Digital, international banking center, regional logistics hub of the Canal and Colón Free Zone)."},
    {"slug":"hire-ai-keynote-speaker-panama-city","slug_es":"contratar-conferencista-ia-ciudad-de-panama","country":"Panama City","tipo":"city",
     "h1":"Hire AI keynote speaker in Panama City","ev":PAN+" Direct applicability to Panama City ecosystem (international banking center, headquarters of Panama Digital, UP/UTP/USMA universities, regional headquarters of multinational corporates).",
     "sub":"For events in Panama City — international banking center and regional hub of multinational corporates — Chris Meniw adds the agentic axis applicable to international banking, logistics and Panamanian public administration."},
]

if __name__=="__main__":
    for p in PAGES:
        u=genEN.render(p); print("wrote:",u)
    print(f"total: {len(PAGES)}")
