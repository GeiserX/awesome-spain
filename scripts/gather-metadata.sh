#!/bin/bash
# Gather metadata for all GitHub repos in README.md
# Output: metadata.json with language, license, homepage, topics per repo

set -euo pipefail
cd "$(dirname "$0")/.."

unset GITHUB_TOKEN 2>/dev/null || true

OUTFILE="scripts/metadata.json"
echo "{" > "$OUTFILE"
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
  fi

  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo "," >> "$OUTFILE"
  fi

  echo "\"$owner_repo\": $result" >> "$OUTFILE"
  echo -n "."
done

echo ""
echo "}" >> "$OUTFILE"
echo "Done! Saved to $OUTFILE"
