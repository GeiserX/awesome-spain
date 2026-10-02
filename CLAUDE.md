# CLAUDE.md — awesome-spain

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
- Software **nacido en España para resolver un problema español** que luego se internacionalizó, si sigue teniendo relevancia especial en España (Decidim, CONSUL Democracy, etc.).
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
- [Nombre](https://github.com/owner/repo) [![Stars](...)](stargazers) [![Last Commit](...)](commits) [![Language](...)](repo) [![License](...)](LICENSE) [![Tag](...)](url) - Descripción que empieza en mayúscula y termina en punto.
```

Las insignias se generan automáticamente con `scripts/transform-readme.py`. Para contribuir, basta con añadir la entrada en formato simple:

```markdown
- [Nombre](https://github.com/owner/repo) - Descripción que empieza en mayúscula y termina en punto.
```

- La descripción **no debe empezar con el nombre del proyecto**.
- Máximo una línea por entrada.
- Entradas **ordenadas alfabéticamente** (por nombre visible, sin distinguir mayúsculas/minúsculas) dentro de cada sección y subsección.
- Validar con awesome-lint-extra: `python3 lint.py` o mediante el workflow de CI.
- Evitar el anglicismo «curar/curado» (de *curated*). Según la FundéuRAE, las alternativas preferidas son «selección», «recopilación» o «responsable de contenidos». Ver: https://www.fundeu.es/recomendacion/responsable-de-contenidos-mejor-que-content-curator/

## Verificación antes de añadir

Antes de incluir un repositorio, comprobar:

- **Existe y es público**: el enlace GitHub funciona y el repo no es privado.
- **No está archivado ni en solo lectura**: si está archivado, va a `DELETED.md` (sección "Archivados").
- **Sigue haciendo su trabajo**: este es el criterio que decide. Si el proyecto **consume un servicio** (una API, una sede electrónica, una web que raspa), sigue haciéndolo hoy. Si **no consume ninguno** (un validador de NIF, un lector de cuadernos AEB, una librería XAdES, un dataset), basta con que su lógica siga siendo correcta: un formato o un algoritmo que no cambia no se rompe solo. Un proyecto estable y completo se queda aunque lleve años sin commits; uno que ya no funciona se retira aunque tenga commits de esta semana.
- **La carga de la prueba es del que retira**: hay que enseñar el fallo, ejecutando el proyecto o comprobando que el servicio que consume ya no responde como espera. La falta de releases, de estrellas o de actividad no es un fallo. Si no se puede demostrar que está roto, se queda.
- **La fecha del último commit es un aviso, no una sentencia**: más de 3 años sin actividad obliga a mirar el proyecto, nunca a retirarlo de forma automática. Y mirar el último commit de la rama por defecto, no `pushed_at`: las ramas de bots lo rejuvenecen sin que nadie mantenga nada.
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

## Difusión

- Notificar a propietarios de repos incluidos abriendo un issue con título "Incluido en awesome-spain 🇪🇸" y mensaje breve en español (tuteo) ofreciendo retirar si prefieren. Solo 1 issue por organización/usuario — no spamear repos del mismo propietario.
- Publicar en comunidades españolas de desarrollo (Meneame, Reddit r/spain, Slacks españoles) tras alcanzar masa crítica.
- Enviar PR a [sindresorhus/awesome](https://github.com/sindresorhus/awesome) después de 30 días desde la creación del repo.

---

*Generated by [LynxPrompt](https://lynxprompt.com) CLI*

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:6cd5cc61 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->

## Where the tracker syncs

This repo is public, so its tracker syncs only to the private Dolt remote named by `sync.remote` in `.beads/config.yaml` (`giteaer/awesome-spain-beads` on Gitea). The block above says sync uses "your git remote". Here that never means this GitHub repo. Don't add it as a Dolt remote and don't push `refs/dolt/*` to it.
