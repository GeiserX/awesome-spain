#!/bin/bash
# Gather metadata for all GitHub repos in README.md
# Output: metadata.json with language, license, homepage, topics per repo

set -euo pipefail
cd "$(dirname "$0")/.."

unset GITHUB_TOKEN GH_TOKEN 2>/dev/null || true

OUTFILE="scripts/metadata.json"
# Se escribe en un temporal y solo se sustituye el bueno al final. Si la
# ejecucion se corta a medias (limite de peticiones, red), metadata.json se
# queda como estaba en vez de quedar a medias o mal. El temporal va en el mismo
# directorio a proposito: asi el mv final es un renombrado dentro del mismo
# sistema de ficheros, que es atomico. Con cp habria un instante en el que el
# fichero bueno esta truncado.
TMPFILE="$(mktemp "scripts/.metadata.json.XXXXXX")"
trap 'rm -f "$TMPFILE"' EXIT

echo "{" > "$TMPFILE"
FIRST=true

# Extract unique GitHub repo URLs
grep -oE 'https://github\.com/[^/)]+/[^/)]+' README.md | sort -u | while read -r url; do
  owner_repo="${url#https://github.com/}"

  # Query GitHub API. En un 404 gh escribe el cuerpo del error en stdout y sale
  # con codigo != 0, asi que hay que descartar esa salida en vez de encadenarla:
  # concatenar los dos objetos JSON dejaba metadata.json invalido.
  if ! result=$(gh api "repos/$owner_repo" --jq '{
    language: (.language // ""),
    license: (.license.spdx_id // ""),
    homepage: (.homepage // ""),
    topics: (.topics // []),
    description: (.description // ""),
    stargazers_count: .stargazers_count,
    default_branch: (.default_branch // "main")
  }' 2>/dev/null); then
    result='{"error": true}'
  else
    # Ruta real del fichero de licencia. No sale de repos/OWNER/REPO, hace falta
    # el endpoint /license, que devuelve 404 cuando el repo no tiene ninguno.
    # Suponer "LICENSE" rompia el enlace de la insignia en los repos que usan
    # LICENSE.txt o LICENSE.md y en los que no tienen licencia.
    #
    # Hay que distinguir el 404 de cualquier otro fallo. Si se tratan igual, una
    # ejecucion con el limite de peticiones agotado marca TODOS los repos como
    # "sin licencia" y transform-readme.py reescribe los enlaces de la lista
    # entera. Por eso se aborta ante cualquier estado que no sea 200 o 404.
    # Se reintenta antes de rendirse: un corte de red puntual no debe tumbar una
    # ejecucion de trece minutos, pero un limite de peticiones agotado si tiene
    # que parar en seco.
    lic_path=""
    lic_ok=false
    for attempt in 1 2 3; do
      lic_out=$(gh api "repos/$owner_repo/license" 2>/dev/null) || true
      lic_status=$(printf '%s' "$lic_out" | jq -r '.status // "200"' 2>/dev/null || printf 'desconocido')
      case "$lic_status" in
        200) lic_path=$(printf '%s' "$lic_out" | jq -r '.path // ""'); lic_ok=true; break ;;
        404)
          # GitHub devuelve 404 cuando no RECONOCE la licencia, no solo cuando
          # no hay ninguna: los repos que siguen REUSE guardan un directorio
          # LICENSES/ y quedaban marcados como si no tuvieran licencia. Se mira
          # la raiz del repo antes de darlo por perdido.
          root_out=$(gh api "repos/$owner_repo/contents" 2>/dev/null) || true
          lic_path=$(printf '%s' "$root_out" | jq -r '
            if type=="array" then
              [.[] | select(.name | test("^(LICEN[CS]E|COPYING)"; "i")) | .path] | first // ""
            else "" end' 2>/dev/null || printf '')
          lic_ok=true; break ;;
        *)   sleep $((attempt * 2)) ;;
      esac
    done
    if [ "$lic_ok" != true ]; then
        echo "" >&2
        echo "ERROR: repos/$owner_repo/license devolvio '$lic_status', que no es 200 ni 404." >&2
        echo "Se aborta sin tocar $OUTFILE. Continuar marcaria como 'sin licencia'" >&2
        echo "repos que si la tienen y romperia los enlaces de toda la lista." >&2
        echo "Si es el limite de peticiones, mirar la cabecera X-Ratelimit-Reset:" >&2
        echo "  gh api repos/GeiserX/awesome-spain -i | grep -i x-ratelimit" >&2
        exit 1
    fi
    result=$(printf '%s' "$result" | jq --arg p "$lic_path" '. + {license_path: $p}')
  fi

  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo "," >> "$TMPFILE"
  fi

  echo "\"$owner_repo\": $result" >> "$TMPFILE"
  echo -n "."
done

echo ""
echo "}" >> "$TMPFILE"

# Solo se sustituye si lo generado es JSON valido.
if ! jq empty "$TMPFILE" 2>/dev/null; then
  echo "ERROR: lo generado no es JSON valido. $OUTFILE se queda como estaba." >&2
  exit 1
fi

mv "$TMPFILE" "$OUTFILE"
echo "Done! Saved to $OUTFILE"
