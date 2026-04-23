#!/usr/bin/env python3
"""Transform awesome-spain README entries with metadata (stars, license, language, institution tags, demos)."""

import json
import re
import sys

# Load metadata
with open("scripts/metadata.json") as f:
    metadata = json.load(f)

# Section/subsection -> default institution tags
SECTION_TAGS = {
    "Televisión, Radio y Podcasts": ["TDT"],
    "Radio y Podcasts": [],
    "Facturación Electrónica": ["AEAT"],
    "VeriFactu": ["AEAT", "VeriFactu"],
    "Facturae": ["AEAT", "Facturae"],
    "TicketBAI": ["TicketBAI"],
    "SII y Modelos AEAT": ["AEAT", "SII"],
    "Pasarelas de Pago": ["Redsys"],
    "ERP y Contabilidad": [],
    "Firma Electrónica y Administración Pública": ["SEAP"],
    "AutoFirma y @firma": ["SEAP", "AutoFirma"],
    "Administración Electrónica": ["SEAP"],
    "Transparencia y Legal Tech": ["BOE"],
    "Datos Abiertos y Estadísticas": [],
    "Radar COVID": ["Gobierno"],
    "Energía y Electricidad": ["REE"],
    "Meteorología": ["AEMET"],
    "Transporte y Movilidad": [],
    "Bicicletas Públicas": [],
    "Aeropuertos": ["AENA"],
    "Metro y Cercanías": [],
    "Cartografía y Catastro": ["Catastro"],
    "Inmobiliaria y Mercados": [],
    "Portales Inmobiliarios": [],
    "Wallapop": ["Wallapop"],
    "Validación de Documentos": [],
    "Lengua Española y Diccionarios": ["RAE"],
    "Procesamiento de Lenguaje Natural": [],
    "Lenguas Cooficiales": [],
    "Combustible y Estaciones de Servicio": [],
    "Formatos Bancarios": ["AEB"],
    "Supermercados": [],
    "Alarmas y Seguridad del Hogar": [],
    "Telecomunicaciones": [],
    "Agua": [],
    "Logística y Mensajería": ["Correos"],
    "Deportes": [],
    "Cine y Entretenimiento": [],
    "FilmAffinity": ["FilmAffinity"],
    "Música y Flamenco": [],
    "DGT y Vehículos": ["DGT"],
    "Agricultura": ["SIGPAC"],
    "Smart Cities e IoT": [],
    "Blockchain e Identidad Digital": ["Alastria"],
    "Salud y Medicamentos": ["AEMPS"],
    "Educación y Oposiciones": [],
    "Extranjería y Visados": ["Extranjería"],
    "Empleo y Trabajo Remoto": [],
    "Participación Ciudadana": [],
    "Comunidades Autónomas y Administración Local": [],
    "Cataluña": ["Cataluña"],
    "País Vasco": ["País Vasco"],
    "Andalucía": ["Andalucía"],
    "Galicia": ["Galicia"],
    "Comunidad Valenciana": ["C. Valenciana"],
    "Comunidad de Madrid": ["C. Madrid"],
    "Canarias": ["Canarias"],
    "Aragón": ["Aragón"],
    "Islas Baleares": ["Baleares"],
    "La Rioja": ["La Rioja"],
    "Castilla y León": ["Castilla y León"],
    "Región de Murcia": [],
    "Ayuntamientos y Diputaciones": [],
    "Servidores MCP": ["MCP"],
}

# Keyword -> tag overrides/additions
KEYWORD_TAGS = {
    # Government institutions
    "AEAT": "AEAT",
    "Agencia Tributaria": "AEAT",
    "Hacienda": "AEAT",
    "IRPF": "AEAT",
    "Renta": "AEAT",
    "modelo": "AEAT",
    "DGT": "DGT",
    "Dirección General de Tráfico": "DGT",
    "autoescuela": "DGT",
    "matrícula": "DGT",
    "Catastro": "Catastro",
    "catastral": "Catastro",
    "INSPIRE": "Catastro",
    "AEMET": "AEMET",
    "meteorológ": "AEMET",
    "INE": "INE",
    "Instituto Nacional de Estadística": "INE",
    "BOE": "BOE",
    "Boletín Oficial": "BOE",
    "BORME": "BOE",
    "AEMPS": "AEMPS",
    "CIMA": "AEMPS",
    "medicament": "AEMPS",
    "CNMC": "CNMC",
    "AENA": "AENA",
    "REE": "REE",
    "Red Eléctrica": "REE",
    "ESIOS": "REE",
    "esios": "REE",
    "PVPC": "REE",
    "OMIE": "REE",
    "SIGPAC": "SIGPAC",
    "RAE": "RAE",
    "Real Academia": "RAE",
    "CIS": "CIS",
    "Investigaciones Sociológicas": "CIS",
    "datos.gob.es": "datos.gob.es",
    "Correos": "Correos",
    "FNMT": "FNMT",
    "CERES": "FNMT",
    "SEAP": "SEAP",
    "CNIG": "CNIG",
    "CartoCiudad": "CNIG",
    "IGN": "CNIG",
    "CENDOJ": "CENDOJ",
    # Standards/platforms
    "VeriFactu": "VeriFactu",
    "TicketBAI": "TicketBAI",
    "Facturae": "Facturae",
    "FacturaE": "Facturae",
    "FACe": "Facturae",
    "SII": "SII",
    "Suministro Inmediato": "SII",
    "Redsys": "Redsys",
    "Sermepa": "Redsys",
    "Servired": "Redsys",
    "AutoFirma": "AutoFirma",
    "autofirma": "AutoFirma",
    "Cl@ve": "Cl@ve",
    "clave": "Cl@ve",
    "DNIe": "DNIe",
    "DNI electrónico": "DNIe",
    "Norma 43": "AEB",
    "Norma43": "AEB",
    "norma43": "AEB",
    "cuadernos AEB": "AEB",
    "AEB 19": "AEB",
    "AEB 43": "AEB",
    "19.14": "AEB",
    "34.14": "AEB",
    "TDT": "TDT",
    "Movistar+": "Movistar",
    "Movistar TV": "Movistar",
    "Movistar IPTV": "Movistar",
    "Movistar Home": "Movistar",
    "router Movistar": "Movistar",
    "router de Movistar": "Movistar",
    "MitraStar": "Movistar",
    "Tvheadend": "Movistar",
    "EPG": "TDT",
    "iVoox": "iVoox",
    # Companies/services
    "Renfe": "Renfe",
    "AVE": "Renfe",
    "Cercanías": "Renfe",
    "Mercadona": "Mercadona",
    "Wallapop": "Wallapop",
    "Idealista": "Idealista",
    "idealista": "Idealista",
    "Fotocasa": "Fotocasa",
    "FilmAffinity": "FilmAffinity",
    "filmaffinity": "FilmAffinity",
    "BiciMAD": "BiciMAD",
    "Bicing": "Bicing",
    "Valenbisi": "Valenbisi",
    "Securitas Direct": "Securitas",
    "Prosegur": "Prosegur",
    "Iberdrola": "Iberdrola",
    "i-DE": "Iberdrola",
    "Endesa": "Endesa",
    "e-distribución": "Endesa",
    "Datadis": "Datadis",
    "Som Energia": "Som Energia",
    "Octopus Energy": "Octopus",
    "Repsol": "Repsol",
    "Pepephone": "Pepephone",
    "Orange": "Orange",
    "Livebox": "Orange",
    "InfoJobs": "InfoJobs",
    "Manfred": "Manfred",
    "FacturaScripts": "FacturaScripts",
    "Odoo": "Odoo",
    "RTVE": "RTVE",
    "Filmin": "Filmin",
    "LaLiga": "LaLiga",
    "Fantasy": "LaLiga",
    "Kodi": "Kodi",
    "EMT Madrid": "EMT Madrid",
    "EMT Valencia": "EMT Valencia",
    "TUSSAM": "TUSSAM",
    "FGC": "FGC",
    "FGV": "FGV",
    "MetroValencia": "FGV",
    "Rodalies": "Rodalies",
    "AUCORSA": "AUCORSA",
    "Aigües de Barcelona": "Aigües BCN",
    "Nacex": "Nacex",
    "Correos Express": "Correos",
    # Regions (explicit, not from section)
    "Generalitat de Catalunya": "Cataluña",
    "Consorci AOC": "Cataluña",
    "IdCat": "Cataluña",
    "XTEC": "Cataluña",
    "Softcatalà": "Cataluña",
    "BSC": "Cataluña",
    "AINA": "Cataluña",
    "Idescat": "Cataluña",
    "catalán": "Cataluña",
    "català": "Cataluña",
    "Selectivitat": "Cataluña",
    "Junta de Andalucía": "Andalucía",
    "Guadalinex": "Andalucía",
    "EducaAndOS": "Andalucía",
    "Andaluces": "Andalucía",
    "andaluz": "Andalucía",
    "euskera": "País Vasco",
    "Hacienda Foral": "País Vasco",
    "Bizkaia": "País Vasco",
    "Batuz": "País Vasco",
    "Eustat": "País Vasco",
    "Euskadi": "País Vasco",
    "Open Data Euskadi": "País Vasco",
    "galego": "Galicia",
    "gallego": "Galicia",
    "galleg": "Galicia",
    "Xunta": "Galicia",
    "CiTIUS": "Galicia",
    "USC": "Galicia",
    "Proxecto Nós": "Galicia",
    "MeteoGalicia": "Galicia",
    "LliureX": "C. Valenciana",
    "Govern de les Illes Balears": "Baleares",
    "GovernIB": "Baleares",
    "Mallorca": "Baleares",
    "ISTAC": "Canarias",
    "FRONTUR": "Canarias",
    "Canarias": "Canarias",
    "Aragón": "Aragón",
    "aragonés": "Aragón",
    "IDERioja": "La Rioja",
    "La Rioja": "La Rioja",
    "ICANE": "Cantabria",
    "Santander": "Cantabria",
    "LOMLOE": "Educación",
    "ANECA": "Educación",
    "oposiciones": "Educación",
    "PAU": "Educación",
    "Navarra": "Navarra",
    "SITNA": "Navarra",
    "Catastro de Navarra": "Navarra",
    # Cities
    "Madrid": "Madrid",
    "Ayuntamiento de Madrid": "Madrid",
    "Barcelona": "Barcelona",
    "Ajuntament de Barcelona": "Barcelona",
    "Diputació de Barcelona": "Barcelona",
    "Open Data BCN": "Barcelona",
    "Valencia": "Valencia",
    "VLCTechHub": "Valencia",
    "Vigo": "Vigo",
    "Zaragoza": "Zaragoza",
    "Valladolid": "Valladolid",
    "Sevilla": "Sevilla",
    "Córdoba": "Córdoba",
    # Technologies/protocols
    "Home Assistant": "Home Assistant",
    "HACS": "Home Assistant",
    "Lovelace": "Home Assistant",
    "GOBL": "GOBL",
    "Decidim": "Decidim",
    "CONSUL": "CONSUL",
    "CKAN": "CKAN",
    "sentilo": "Sentilo",
    "Alastria": "Alastria",
    "MCP": "MCP",
    "flamenco": "Flamenco",
    "Flamenco": "Flamenco",
    "COVID": "COVID-19",
    "Radar COVID": "COVID-19",
    "Civio": "Civio",
    "civio": "Civio",
    "Datania": "Datania",
    "rOpenSpain": "rOpenSpain",
    "Policía Nacional": "Policía",
    "Webpol": "Policía",
    "E-Hotel": "Policía",
    # Document validation
    "DNI": "DNI/NIE",
    "NIE": "DNI/NIE",
    "NIF": "DNI/NIE",
    "CIF": "DNI/NIE",
    "NSS": "DNI/NIE",
    "código postal": "DNI/NIE",
    # Spanish data/statistics
    "calidad del aire": "datos.gob.es",
    "municipios": "INE",
    "sección censal": "INE",
    "microdatos": "INE",
    "Banco de España": "BdE",
    "Censo": "INE",
    "movilidad": "INE",
    # Fuel/gas stations
    "gasolinera": "Geoportal",
    "combustible": "Geoportal",
    "precio-gasolina": "Geoportal",
    "precio gasolina": "Geoportal",
    "Geoportal": "Geoportal",
    # Football/sports
    "fútbol": "LaLiga",
    "futbol": "LaLiga",
    "Primera División": "LaLiga",
    "Segunda División": "LaLiga",
    "quiniela": "LaLiga",
    # Spanish maps/geodata
    "TopoJSON": "CNIG",
    "comunidades autónomas": "INE",
    "provincias": "INE",
    "CCAA": "INE",
    # Galicia transport
    "bus.gal": "Galicia",
    # NLP generic spanish
    "guitarra": "Flamenco",
    # Generic Spain data
    "datos abiertos españoles": "datos.gob.es",
    "datos públicos": "datos.gob.es",
    "datos abiertos": "datos.gob.es",
    # Telecom
    "spam": "Telecomunicaciones",
    "teléfono": "Telecomunicaciones",
    "router": "Telecomunicaciones",
    "UART": "Telecomunicaciones",
    "Askey": "Movistar",
    # Admin
    "TPV": "Redsys",
    "AGE": "SEAP",
    "PreparaTIC": "SEAP",
    "TAI": "SEAP",
    "RPT": "SEAP",
    "trabajo remoto": "Empleo",
    "empleo": "Empleo",
    # Remaining edge cases
    "códigos postales": "INE",
    "COVID-19": "COVID-19",
    "COVID19": "COVID-19",
    "COVID-19 de España": "COVID-19",
    "periodismo de investigación": "datos.gob.es",
    "DATADISTA": "datos.gob.es",
    "mapas oficiales españoles": "CNIG",
    "nombres": "INE",
    "apellidos": "INE",
    "catalán": "Cataluña",
    "catalana": "Cataluña",
    "directorios telefónicos": "Telecomunicaciones",
}

# Tag -> URL for clickable badges
TAG_URLS = {
    # Government institutions
    "AEAT": "https://sede.agenciatributaria.gob.es/",
    "DGT": "https://www.dgt.es/",
    "Catastro": "https://www.sedecatastro.gob.es/",
    "AEMET": "https://www.aemet.es/",
    "INE": "https://www.ine.es/",
    "BOE": "https://www.boe.es/",
    "AEMPS": "https://www.aemps.gob.es/",
    "CNMC": "https://www.cnmc.es/",
    "AENA": "https://www.aena.es/",
    "REE": "https://www.ree.es/",
    "SIGPAC": "https://sigpac.mapama.gob.es/",
    "RAE": "https://www.rae.es/",
    "CIS": "https://www.cis.es/",
    "datos.gob.es": "https://datos.gob.es/",
    "Correos": "https://www.correos.es/",
    "FNMT": "https://www.fnmt.es/",
    "SEAP": "https://administracion.gob.es/",
    "CNIG": "https://www.ign.es/",
    "CENDOJ": "https://www.poderjudicial.es/search/",
    "Gobierno": "https://administracion.gob.es/",
    "Extranjería": "https://sede.administracionespublicas.gob.es/",
    "Policía": "https://www.policia.es/",
    # Standards/platforms
    "VeriFactu": "https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu.html",
    "TicketBAI": "https://www.batuz.eus/",
    "Facturae": "https://face.gob.es/",
    "SII": "https://sede.agenciatributaria.gob.es/",
    "Redsys": "https://www.redsys.es/",
    "AutoFirma": "https://firmaelectronica.gob.es/Home/Descargas.html",
    "Cl@ve": "https://clave.gob.es/",
    "DNIe": "https://www.dnielectronico.es/",
    "AEB": "https://www.aebanca.es/",
    "TDT": "https://www.tdt.es/",
    # Companies
    "Renfe": "https://www.renfe.com/",
    "Redsys": "https://www.redsys.es/",
    "Mercadona": "https://www.mercadona.es/",
    "Wallapop": "https://es.wallapop.com/",
    "Idealista": "https://www.idealista.com/",
    "Fotocasa": "https://www.fotocasa.es/",
    "FilmAffinity": "https://www.filmaffinity.com/",
    "BiciMAD": "https://www.bicimad.com/",
    "Bicing": "https://www.bicing.barcelona/",
    "Valenbisi": "https://www.valenbisi.es/",
    "Securitas": "https://www.securitasdirect.es/",
    "Prosegur": "https://www.prosegur.es/",
    "Iberdrola": "https://www.iberdrola.es/",
    "Endesa": "https://www.endesa.com/",
    "Datadis": "https://datadis.es/",
    "Som Energia": "https://www.somenergia.coop/",
    "Octopus": "https://octopusenergy.es/",
    "Repsol": "https://www.repsol.es/",
    "Pepephone": "https://www.pepephone.com/",
    "Movistar": "https://www.movistar.es/",
    "Orange": "https://www.orange.es/",
    "InfoJobs": "https://www.infojobs.net/",
    "Manfred": "https://www.getmanfred.com/",
    "FacturaScripts": "https://facturascripts.com/",
    "Odoo": "https://www.odoo.com/",
    "RTVE": "https://www.rtve.es/",
    "Filmin": "https://www.filmin.es/",
    "iVoox": "https://www.ivoox.com/",
    "LaLiga": "https://www.laliga.com/",
    "Kodi": "https://kodi.tv/",
    "EMT Madrid": "https://www.emtmadrid.es/",
    "EMT Valencia": "https://www.emtvalencia.es/",
    "TUSSAM": "https://www.tussam.es/",
    "FGC": "https://www.fgc.cat/",
    "FGV": "https://www.fgv.es/",
    "Rodalies": "https://rodalies.gencat.cat/",
    "AUCORSA": "https://www.aucorsa.es/",
    "Aigües BCN": "https://www.aiguesdebarcelona.cat/",
    "Nacex": "https://www.nacex.es/",
    "Sentilo": "https://www.sentilo.io/",
    "CONSUL": "https://consuldemocracy.org/",
    "Decidim": "https://decidim.org/",
    "CKAN": "https://ckan.org/",
    "Alastria": "https://alastria.io/",
    "GOBL": "https://gobl.org/",
    "Civio": "https://civio.es/",
    "Datania": "https://datania.cc/",
    "rOpenSpain": "https://ropenspain.es/",
    "Flamenco": "https://www.juntadeandalucia.es/cultura/flamenco/",
    "COVID-19": "https://www.sanidad.gob.es/",
    "DNI/NIE": "https://www.interior.gob.es/",
    "BdE": "https://www.bde.es/",
    "Geoportal": "https://geoportalgasolineras.es/",
    "Telecomunicaciones": "https://www.cnmc.es/",
    "Empleo": "https://www.sepe.es/",
    "Home Assistant": "https://www.home-assistant.io/",
    "MCP": "https://modelcontextprotocol.io/",
    "Educación": "https://www.educacionyfp.gob.es/",
    # Regions
    "Cataluña": "https://web.gencat.cat/",
    "País Vasco": "https://www.euskadi.eus/",
    "Andalucía": "https://www.juntadeandalucia.es/",
    "Galicia": "https://www.xunta.gal/",
    "C. Valenciana": "https://www.gva.es/",
    "C. Madrid": "https://www.comunidad.madrid/",
    "Canarias": "https://www.gobiernodecanarias.org/",
    "Aragón": "https://www.aragon.es/",
    "Baleares": "https://www.caib.es/",
    "La Rioja": "https://www.larioja.org/",
    "Cantabria": "https://www.cantabria.es/",
    "Castilla y León": "https://www.jcyl.es/",
    "Navarra": "https://www.navarra.es/",
    # Cities
    "Madrid": "https://www.madrid.es/",
    "Barcelona": "https://www.barcelona.cat/",
    "Valencia": "https://www.valencia.es/",
    "Vigo": "https://www.vigo.org/",
    "Zaragoza": "https://www.zaragoza.es/",
    "Valladolid": "https://www.valladolid.es/",
    "Sevilla": "https://www.sevilla.org/",
    "Córdoba": "https://www.cordoba.es/",
}

# Normalize language names
LANG_MAP = {
    "Jupyter Notebook": "Python",
    "GLSL": None,
    "Makefile": None,
    "Dockerfile": None,
    "Shell": None,
    "Batchfile": None,
    "Nix": None,
    "CMake": None,
    "Smarty": "PHP",
    "Mustache": "JavaScript",
    "Vue": "JavaScript",
    "Svelte": "JavaScript",
    "CSS": None,
    "SCSS": None,
    "Sass": None,
    "Less": None,
    "Roff": None,
    "PLpgSQL": "SQL",
    "TSQL": "SQL",
    "HCL": "Terraform",
    "Gherkin": None,
    "Groovy": "Java",
    "Scala": "Scala",
    "Elixir": "Elixir",
    "Erlang": "Erlang",
    "Haskell": "Haskell",
    "Lua": "Lua",
    "Perl": "Perl",
    "Dart": "Dart",
    "Swift": "Swift",
    "Objective-C": "Objective-C",
    "Assembly": None,
    "Fortran": "Fortran",
    "Mathematica": None,
    "TeX": None,
    "Jinja": "Python",
    "Starlark": None,
    "AutoIt": None,
    "Inno Setup": None,
    "Processing": "Java",
    "NSIS": None,
    "Rich Text Format": None,
}

LICENSE_MAP = {
    "NOASSERTION": None,
    "0BSD": "0BSD",
}

DEMO_URLS = {}


def encode_tag(tag):
    """Encode tag name for shields.io badge URL."""
    return tag.replace("-", "--").replace("_", "__").replace(" ", "%20").replace("+", "%2B").replace("@", "%40")


def get_spain_tags(section_name, entry_name, description):
    """Determine institution/service tags for an entry."""
    tags = set()

    # Add section defaults
    if section_name in SECTION_TAGS:
        tags.update(SECTION_TAGS[section_name])

    # Scan description + name for keyword matches
    text = f"{entry_name} {description}"
    for keyword, tag in KEYWORD_TAGS.items():
        if keyword in text:
            tags.add(tag)

    # Remove overly broad tags when more specific ones exist
    # "Madrid" city tag vs "C. Madrid" region tag
    if "C. Madrid" in tags and "Madrid" in tags:
        tags.discard("Madrid")
    # "Barcelona" city tag vs "Cataluña" region tag — keep both, they're different
    # Remove "AEAT" when VeriFactu/TicketBAI/SII/Facturae is more specific
    # Actually keep AEAT as it's the parent institution

    return sorted(tags)


def get_language(owner_repo):
    meta = metadata.get(owner_repo, {})
    lang = meta.get("language", "")
    if not lang:
        return None
    if lang in LANG_MAP:
        return LANG_MAP[lang]
    return lang


def get_license(owner_repo):
    meta = metadata.get(owner_repo, {})
    lic = meta.get("license", "")
    if not lic:
        return None
    if lic in LICENSE_MAP:
        return LICENSE_MAP[lic]
    return lic


def get_default_branch(owner_repo):
    meta = metadata.get(owner_repo, {})
    return meta.get("default_branch", "main")


def get_demo_url(owner_repo):
    return DEMO_URLS.get(owner_repo)


def transform_entry(line, current_section):
    """Transform a single entry line with metadata."""
    badge_pat = r'(?:\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)|!\[[^\]]*\]\([^)]+\))'
    demo_pat = r'\(\[Demo\]\([^)]+\)\)'

    m = re.match(
        rf'^- \[([^\]]+)\]\((https://github\.com/([^)]+))\)\s+'
        rf'(?:{badge_pat}\s*)*'
        rf'(?:{demo_pat}\s*)?'
        rf'- (.+)$',
        line
    )
    if not m:
        m = re.match(r'^- \[([^\]]+)\]\((https://github\.com/([^)]+))\) - (.+)$', line)
    if not m:
        return line

    name = m.group(1)
    url = m.group(2)
    owner_repo = m.group(3)
    raw_desc = m.group(4)

    # Strip any existing backtick tags and demo links from description
    description = re.sub(r'\s*\(\[Demo\]\([^)]+\)\)', '', raw_desc)
    description = re.sub(r'\s*`[^`]+`', '', description).strip()

    # Clickable auto-updating shields.io badges
    branch = get_default_branch(owner_repo)
    star_badge = f"[![Stars](https://img.shields.io/github/stars/{owner_repo}?style=flat-square&label=%E2%AD%90)](https://github.com/{owner_repo}/stargazers)"
    commit_badge = f"[![Last Commit](https://img.shields.io/github/last-commit/{owner_repo}?style=flat-square)](https://github.com/{owner_repo}/commits/{branch})"
    lang_badge = f"[![Language](https://img.shields.io/github/languages/top/{owner_repo}?style=flat-square)](https://github.com/{owner_repo})"
    license_badge = f"[![License](https://img.shields.io/github/license/{owner_repo}?style=flat-square)](https://github.com/{owner_repo}/blob/{branch}/LICENSE)"

    # Institution/service tags as clickable Spain red badges (#c60b1e)
    spain_tags = get_spain_tags(current_section, name, raw_desc)
    tag_badge_parts = []
    for t in spain_tags:
        encoded = encode_tag(t)
        if t in TAG_URLS:
            tag_badge_parts.append(
                f"[![{t}](https://img.shields.io/badge/{encoded}-c60b1e?style=flat-square)]({TAG_URLS[t]})"
            )
        else:
            tag_badge_parts.append(
                f"![{t}](https://img.shields.io/badge/{encoded}-c60b1e?style=flat-square)"
            )
    tag_badges = " ".join(tag_badge_parts)

    # Demo link
    demo = get_demo_url(owner_repo)
    demo_str = f" ([Demo]({demo}))" if demo else ""

    # Build line
    parts = [f"- [{name}]({url}) {star_badge} {commit_badge} {lang_badge} {license_badge}"]
    if tag_badges:
        parts[0] += f" {tag_badges}"
    if demo_str:
        parts[0] += demo_str
    parts[0] += f" - {description}"

    return parts[0]


def main():
    with open("README.md") as f:
        lines = f.readlines()

    output = []
    current_section = ""

    for line in lines:
        stripped = line.rstrip("\n")

        # Track current section (## or ###)
        section_match = re.match(r'^#{2,3} (.+)$', stripped)
        if section_match:
            current_section = section_match.group(1)

        # Transform entry lines
        if stripped.startswith("- [") and "github.com/" in stripped and "](#" not in stripped:
            transformed = transform_entry(stripped, current_section)
            output.append(transformed + "\n")
        else:
            output.append(line)

    with open("README.md", "w") as f:
        f.writelines(output)

    print(f"Transformed README.md")


# Known demo URLs
DEMO_URLS.update({
    "LaQuay/TDTChannels": "https://www.tdtchannels.com",
    "civio/verba": "https://verba.civio.es",
    "NeoRazorX/facturascripts": "https://facturascripts.com",
    "ctt-gob-es/clienteafirma": "https://firmaelectronica.gob.es/Home/Descargas.html",
    "ctt-gob-es/datos.gob.es": "https://datos.gob.es",
    "consuldemocracy/consuldemocracy": "https://consuldemocracy.org",
    "decidim/decidim": "https://decidim.org",
    # "azogue/aiopvpc": demo removed (site dead)
    "JaimeObregon/ladonacion.es": "https://ladonacion.es",
    "JaimeObregon/observatoriospublicos.es": "https://observatoriospublicos.es",
    "JaimeObregon/retrosantander": "https://retrosantander.com",
    # "JaimeObregon/infoelectoral": demo removed (connection refused)
    # "civio/presupuesto": demo removed (connection refused)
    # "Webierta/open_luz": demo removed (app delisted from Play Store)
    "paumrch/larenta": "https://larenta.es",
    "gencat/ICGC-comparador-gificador": "https://www.instamaps.cat/visor.html",
    "DvzZDev/AcuaNet": "https://acuanet.es",
    # "hadronomy/canary": demo removed (connection refused)
    "Enchufa2/irpf": "https://enchufa2.shinyapps.io/irpf",
    "gerardgimenezadsuar/contractes-cat": "https://contractes.cat",
    "goiblas/open-data-la-rioja": "https://opendatalarioja.com",
    "imartinezl/bicing-deckgl": "https://barcelona-bicing.firebaseapp.com",
    "javierarce/bicimap": "https://bicimap.javierarce.com",
    "singuerinc/better-dni": "https://better-dni.singuerinc.com",
    "xBaank/MadridTransporte": "https://www.madridtransporte.com",
    "datania/hub": "https://datania.cc",
    "Naritsumi/EstudiaTAI-app": "https://estudiatai.es",
    "mpuig/rentagpt": "https://rentagpt.com",
    "AjuntamentdeBarcelona/decidim-barcelona": "https://www.decidim.barcelona",
    "AyuntamientoMadrid/transparencia": "https://transparencia.madrid.es",
    "ConsorciAOC/signador": "https://signador.aoc.cat/signador/init",
    "akrck02/salary": "https://akrck02.org/salary",
    "mdiago/VeriFactu": "https://facturae.irenesolutions.com/verifactu/go",
    "NeoRazorX/facturascripts_2015": "https://facturascripts.com/2015",
    "alxgarci/marca-fantasy-api-scraper-updated": "https://fantasy.relevo.com",
    "compl-ai/compl-ai": "https://compl-ai.org",
    "sentilo/sentilo": "https://www.sentilo.io",
    "projectestac/jclic": "https://projectestac.github.io/jclic/",
    "PopulateTools/gobierto": "https://gobierto.es",
    "VallaBus/vallabus": "https://vallabus.com",
    # "open-transport-mallorca/ViaMallorca": demo removed (connection refused)
})

if __name__ == "__main__":
    main()
