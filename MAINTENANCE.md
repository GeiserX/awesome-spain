# Guía de mantenimiento

> **Este fichero lo mantiene exclusivamente @GeiserX.** No se aceptan PRs que lo modifiquen.

Directrices para los mantenedores de esta lista. Esta guía es común a todas las awesome lists del ecosistema (awesome-spain + listas regionales). Seguirla garantiza que todos los repositorios mantengan la misma calidad, formato y criterios de inclusión, de modo que el conjunto funcione como una colección coherente.

## Filosofía de inclusión

El criterio fundamental es: **se acepta software que da soporte específico a España, no software hecho por alguien español.**

Un repositorio se incluye porque interactúa con instituciones, servicios, infraestructura, normativas o datos propios de España. No basta con que el autor sea español o resida aquí. Un framework genérico creado por un developer español no pertenece a esta lista. Un cliente para una API de servicios de España sí.

- **Sí:** Cliente para la API de AEMET, integración de Redsys para Django, validador de DNI/NIE, facturación electrónica FacturaE.
- **No:** Librería de visualización genérica creada por un equipo español, chatbot en español genérico, SDK de una empresa española cuya API es global e idéntica en todos los países.

Ver `AGENTS.md` para los criterios detallados, zonas grises y temas prohibidos.

## Revisar PRs

1. Comprobar el **mínimo para entrar**: 5 estrellas y 3 meses de historia, y que no sea un volcado. Si no llega, se cierra sin más revisión (ver `CLAUDE.md`). El software de organismos oficiales queda exento.
2. Comprobar que el proyecto **da soporte específico a España** (no simplemente que el autor es español).
3. Verificar que la PR incluye la **URL del servicio o institución de España** que el proyecto soporta.
4. Comprobar formato: entrada simple, orden alfabético, descripción en español que empieza en mayúscula y termina con punto.
5. **CI debe estar verde** antes de mergear: awesome-lint-extra (formato y orden) + `links-changed` (lychee sobre los enlaces que el PR añade o cambia).
6. Las insignias se generan automáticamente. Los contribuidores solo envían:
   ```markdown
   - [Nombre](https://github.com/owner/repo) - Descripción breve que empieza en mayúscula y termina con punto.
   ```
7. Tras mergear, ejecutar el pipeline de insignias y hacer push:
   ```bash
   bash scripts/gather-metadata.sh
   python3 scripts/transform-readme.py
   ```

## Añadir entradas como mantenedor

1. Añadir la entrada simple en la sección correcta, en orden alfabético.
2. Ejecutar el pipeline de insignias:
   ```bash
   bash scripts/gather-metadata.sh
   python3 scripts/transform-readme.py
   ```
   El pipeline también actualiza el recuento de proyectos y categorías de la cabecera del README.
3. Commit y push. Verificar que CI queda verde.
4. Si el propietario del proyecto no ha sido notificado, abrir un issue de cortesía en su repo:
   - Título: `Incluido en awesome-spain`
   - Cuerpo: mensaje breve en español (tuteo) explicando la inclusión y ofreciendo retirarlo si lo prefiere.
   - **Un solo issue por propietario** — nunca abrir múltiples issues en repos del mismo usuario/organización.

## Eliminar entradas y DELETED.md

Cada repositorio tiene (o debe tener) un fichero `DELETED.md`. Es una pieza fundamental del mantenimiento: registra todos los proyectos que estuvieron en la lista y fueron retirados, junto con el motivo. Su propósito es:

- **Evitar re-adiciones:** si alguien propone un proyecto ya retirado, se puede consultar por qué se eliminó.
- **Preservar el historial:** deja constancia de decisiones pasadas para futuros mantenedores.
- **Documentar razones:** cada entrada lleva contexto suficiente para entender la retirada.

Las entradas nunca se borran sin más del README. Se mueven a `DELETED.md` en la sección correspondiente:

| Razón | Sección en DELETED.md |
|-------|-----------------------|
| Repo archivado/solo lectura | Archivados |
| Repo eliminado (si solo se renombró, se queda y se actualiza el enlace) | Repos inexistentes o renombrados |
| Autor confirmó abandono y ya no funciona | Abandonados |
| No cumple criterios de inclusión | Eliminados por no ser específicos de España |
| Sustituido por otro proyecto | Reemplazados (enlazar sucesor) |
| Roto, viejo sin reputación que no se puede comprobar, o ligado a un sistema retirado | Retirados en la revisión (indicar el motivo y cómo se comprobó) |

Si el repo aún no tiene `DELETED.md`, crearlo con las secciones anteriores la primera vez que se retire un proyecto.

## Mantenimiento periódico

- **Semanal:** una comprobación compartida por todas las listas revisa cada lunes todos los enlaces del README desde España (muchas webs oficiales no responden a los runners de GitHub) y mantiene abierta una sola issue «Dead links» con los que siguen fallando en una segunda pasada cinco minutos después. Corregir esos enlaces. Un enlace caído no demuestra por sí solo que el proyecto esté roto. Si un enlace no tiene arreglo, su entrada se revisa con los criterios de «Permanencia» de `CLAUDE.md`. Si hay que retirarla, entra en una propuesta de retirada, que Sergio aprueba antes de moverla a `DELETED.md`. La issue se cierra sola en la siguiente ejecución limpia.
- **Trimestral:** Revisar las entradas con más de 3 años sin commits en la rama por defecto con los criterios de «Permanencia» de `CLAUDE.md`: las archivadas, rotas, sustituidas por una entrada mantenida o ligadas a un sistema retirado se retiran; las demás se quedan si tienen reputación, o si no la tienen pero se comprueba que funcionan (ejecutándolas, cotejándolas con el servicio que consumen o cotejando sus datos con la fuente oficial). La propuesta de retiradas se aprueba antes de tocar `DELETED.md`. Refrescar insignias (`gather-metadata.sh` + `transform-readme.py`). Comprobar si hay repos recién archivados:
  ```bash
  grep -oE 'https://github\.com/[^/)]+/[^/)]+' README.md | sort -u | while read url; do
    repo="${url#https://github.com/}"
    archived=$(gh api "repos/$repo" --jq '.archived') || { echo "ERROR: no se pudo consultar $repo" >&2; continue; }
    [ "$archived" = "true" ] && echo "ARCHIVADO: $repo"
  done
  ```
  Los archivados entran en esa misma propuesta y pasan a `DELETED.md` cuando se aprueba. Una entrada más reciente que resulta rota, ligada a un sistema retirado o sustituida por una entrada mantenida entra en una propuesta en cuanto se detecta: el filtro de 3 años solo marca cuándo se revisa la antigüedad.

## Herramientas

- **awesome-lint-extra** — Linter propio. Valida formato, orden alfabético, insignias y descripciones. Se ejecuta como GitHub Action (`GeiserX/awesome-lint-extra@main`) y como script standalone (`python3 lint.py`). Configuración en `.awesomerc.json`.
- **transform-readme.py** — Genera insignias de shields.io y etiquetas de institución/servicio a partir de `scripts/metadata.json`.
- **gather-metadata.sh** — Obtiene metadatos (estrellas, lenguaje, licencia, rama) de la API de GitHub para cada repo listado.
- **lychee** — Comprobador de enlaces. `links-changed.yml` revisa en cada PR solo las líneas del README que añade o cambia, con la acción `links-changed` de awesome-lint-extra, y sí bloquea el merge: 403 y 429 cuentan como válidos (bloqueos de bots); cualquier otro error o timeout falla si se repite en una segunda pasada un minuto después. La revisión semanal del README entero corre fuera de este repositorio, nunca falla por un enlace roto y abre o actualiza la issue «Dead links». Los hosts que siempre bloquean al comprobador van en `.lycheeignore`.

## Reglas de formato

- La descripción **no debe empezar con el nombre** del proyecto.
- Una línea por entrada, sin saltos de línea.
- Descripciones en **español**.
- **Orden alfabético** dentro de cada sección/subsección (sin distinguir mayúsculas/minúsculas).
- Evitar el anglicismo «curar/curado» — usar «selección» o «recopilación» (según FundéuRAE).
- Nuevas categorías: preferiblemente con al menos 3 proyectos.

## Contenido prohibido

No se aceptan proyectos relacionados con: pornografía, NSFW, apuestas, loterías, religión, política partidista.

## Difusión

- Abrir issues de notificación en repos de proyectos incluidos (uno por propietario, en español).
- Publicar en comunidades de desarrollo relevantes tras alcanzar masa crítica.
