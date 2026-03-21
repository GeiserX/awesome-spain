# AGENTS.md — awesome-spain

## Objetivo

Selección de software open source que da **soporte específico a España, sus comunidades autónomas y provincias**. Todo el contenido debe estar en español. El nombre del repositorio se mantiene en inglés (`awesome-spain`).

## Criterios de inclusión

### Sí incluir

- Software que interactúa con **instituciones, servicios o infraestructura española** (AEAT, DGT, Catastro, AEMET, Renfe, Redsys, AEMPS, BOE, INE, etc.).
- Integraciones con **empresas cuyo mercado principal es España** (Movistar routers, Securitas Direct, Mercadona, Wallapop, Milanuncios, Idealista, Fotocasa, BiciMAD, iVoox, FilmAffinity, etc.).
- Software de **comunidades autónomas, ayuntamientos y diputaciones** españolas (Consorci AOC, Govern Balear, Junta de Andalucía, CARM, etc.), incluso si el código en sí es genérico (p.ej. un portafirmas), porque está creado y desplegado para la administración española.
- Validadores de **documentos españoles** (DNI, NIE, NIF, CIF, matrículas, NSS, códigos postales).
- Formatos bancarios **específicamente españoles** (cuadernos AEB, Norma 43, formatos CaixaBank, etc.).
- Herramientas para **lenguas cooficiales de España** (catalán, gallego, euskera) cuando están financiadas o producidas por instituciones españolas (Projecte AINA/BSC, CiTIUS/USC, etc.).
- Software **nacido en España para resolver un problema español** que luego se internacionalizó, si sigue teniendo relevancia especial en España (Decidim, CONSUL Democracy, Pumperly, etc.).
- Distribuciones Linux o software educativo de gobiernos autonómicos (Guadalinex, LliureX).

### No incluir

- Software genérico creado por desarrolladores españoles pero sin funcionalidad específica para España (p.ej. una librería de visualización genérica, un framework JS genérico, un sistema de diseño global).
- Software en **idioma español** que no tiene relación con España como país. "Español" ≠ "España". Herramientas de NLP en español genérico, conjugadores de verbos, modelos de voz en español, etc. van en listas de NLP español, no aquí.
- Estándares **europeos genéricos** sin adaptación española (SEPA puro, Euribor, normativas EU genéricas). Excepción: si la librería implementa específicamente la variante española o los cuadernos AEB.
- APIs de empresas **nacidas en España pero globalizadas** cuya API es idéntica en todos los países (p.ej. Glovo Business API).
- Productos SaaS españoles cuya librería open source es para uso internacional sin funcionalidad específica española (p.ej. Quaderno.js para tax compliance global).
- Herramientas IoT genéricas que simplemente se crearon en un FabLab español (Smart Citizen Kit).
- Frameworks o librerías genéricas de desarrollo creadas por gobiernos autonómicos si no tienen funcionalidad específica regional (p.ej. un generador de aplicaciones genérico, un framework Java/JS estándar).

### Zona gris — preguntar al usuario

- Software que **nació en España** para un caso español pero se expandió globalmente → incluir si sigue teniendo relevancia especial aquí.
- Plataformas IoT desplegadas principalmente en ciudades españolas aunque el código sea genérico → incluir con matiz en la descripción.
- Software de gobierno autonómico genérico (sistemas de diseño, portafirmas) → incluir si está activamente en uso por la administración.

## Formato de entradas

```markdown
- [Nombre](https://github.com/owner/repo) - Descripción que empieza en mayúscula y termina en punto.
```

- La descripción **no debe empezar con el nombre del proyecto**.
- Máximo una línea por entrada.
- Usar awesome-lint para validar: `npx awesome-lint`.
- Evitar el anglicismo «curar/curado» (de *curated*). Según la FundéuRAE, las alternativas preferidas son «selección», «recopilación» o «responsable de contenidos». Ver: https://www.fundeu.es/recomendacion/responsable-de-contenidos-mejor-que-content-curator/

## Verificación antes de añadir

Antes de incluir un repositorio, comprobar:

- **Existe y es público**: el enlace GitHub funciona y el repo no es privado.
- **No está archivado ni en solo lectura**: si está archivado, va a `DELETED.md` (sección "Archivados").
- **Actividad razonable**: al menos un commit en los últimos 3 años, salvo proyectos estables/completos que no necesitan actualizaciones.
- **No es un duplicado**: cruzar con `README.md` y `DELETED.md` para evitar repeticiones.
- **Calidad mínima**: tiene documentación básica (README) y no es un repositorio vacío o de pruebas.

## Pull requests y contribuciones

- Las PRs deben usar la plantilla en `.github/PULL_REQUEST_TEMPLATE.md`.
- **Obligatorio**: incluir en la PR la **URL del servicio, API o institución española** a la que el software da soporte (p.ej. aeat.es, renfe.com, catastro.meh.es). Esto permite verificar que el proyecto es relevante.
- Hay issue templates para sugerir proyectos (`anadir-proyecto.md`) y para solicitar retirada (`retirar-proyecto.md`).
- Si un repo está archivado o ya no existe, eliminarlo de la lista.

## Estructura

- Secciones con `##`, subsecciones con `###`.
- Las secciones suelen tener al menos 3 entradas, pero se admiten secciones con 1-2 entradas en casos excepcionales si el nicho es suficientemente relevante para España.
- Tabla de contenido al inicio entre comentarios `<!--lint disable/enable awesome-list-item-->`.
- Al final: sección Contribuir, Nota y Descargo de responsabilidad.

## Temas prohibidos

No se aceptan proyectos de: pornografía, NSFW, loterías, apuestas, religión, política partidista.

## Promoción

- Notificar a propietarios de repos incluidos abriendo un issue con título "Incluido en awesome-spain 🇪🇸" y mensaje breve en español ofreciendo retirar si prefieren.
- Publicar en comunidades españolas de desarrollo (Meneame, Reddit r/spain, Slacks españoles) tras alcanzar masa crítica.
- Enviar a sindresorhus/awesome después de 30 días desde la creación del repo.

## Git

- Identidad: `GeiserX` / `9169332+GeiserX@users.noreply.github.com`
- Sin `Co-Authored-By` en commits.
- Sin atribución a Claude/Anthropic en texto público.
- Rama por defecto: `main`.
- Siempre `unset GITHUB_TOKEN` antes de comandos `gh`.
