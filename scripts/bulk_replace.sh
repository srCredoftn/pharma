#!/bin/bash

# Script de remplacement en masse utilisant sed
# Plus rapide et plus robuste que Python pour les gros volumes

set -e

echo "🚀 REMPLACEMENT EN MASSE: mesoigner → messoins"
echo "================================================"

# Définir les remplacements
declare -a PATTERNS=(
    "s|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g"
    "s|logo-mesoigner|logo-messoins|g"
    's|data-theme="mesoigner"|data-theme="messoins"|g'
    "s|data-theme='mesoigner'|data-theme='messoins'|g"
)

# Dossiers à exclure
EXCLUDE_DIRS=(-path "./.git" -o -path "./.backups" -o -path "./node_modules" -o -path "./vendor" -o -path "./storage")

# Extensions à traiter
EXTENSIONS=(-name "*.php" -o -name "*.html" -o -name "*.htm" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.css" -o -name "*.scss" -o -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.xml" -o -name "*.ini" -o -name "*.env" -o -name "*.conf")

echo ""
echo "📋 Patterns à remplacer:"
for pattern in "${PATTERNS[@]}"; do
    echo "   - $pattern"
done

echo ""
echo "🔍 Recherche des fichiers à traiter..."

# Compter les fichiers
FILE_COUNT=$(find . ! \( "${EXCLUDE_DIRS[@]}" \) \( "${EXTENSIONS[@]}" \) -type f | wc -l)
echo "   Trouvé: $FILE_COUNT fichiers"

echo ""
echo "⏳ Traitement en cours... (cela peut prendre quelques minutes)"

MODIFIED_COUNT=0
CHANGES_MADE=0

# Traiter chaque fichier avec sed
while IFS= read -r file; do
    if [ -z "$file" ]; then
        continue
    fi
    
    # Créer un fichier temporaire
    temp_file="$file.tmp.$$"
    
    # Appliquer tous les patterns
    sed_cmd="sed"
    for pattern in "${PATTERNS[@]}"; do
        sed_cmd="$sed_cmd -e '$pattern'"
    done
    
    # Appliquer les remplacements
    eval "$sed_cmd '$file' > '$temp_file' 2>/dev/null"
    
    # Vérifier si le fichier a changé
    if ! cmp -s "$file" "$temp_file"; then
        mv "$temp_file" "$file"
        ((MODIFIED_COUNT++))
        
        # Compter les changements (approximation)
        CHANGES=$(diff "$file" "$temp_file" 2>/dev/null | wc -l || echo "0")
        ((CHANGES_MADE+=CHANGES))
        
        # Afficher la progression
        if [ $((MODIFIED_COUNT % 100)) -eq 0 ]; then
            echo "   ✓ $MODIFIED_COUNT fichiers modifiés..."
        fi
    else
        rm -f "$temp_file"
    fi
done < <(find . ! \( "${EXCLUDE_DIRS[@]}" \) \( "${EXTENSIONS[@]}" \) -type f)

echo ""
echo "📝 Renommage des dossiers et fichiers..."

# Renommer les dossiers contenant le domaine
find . -maxdepth 1 -type d -name "*pharmaciecourcelles-demours-paris.mesoigner.fr*" | while read dir; do
    newdir="${dir//pharmaciecourcelles-demours-paris.mesoigner.fr/pharmacie-campguezo-cotonou.messoins.bj}"
    if [ "$dir" != "$newdir" ]; then
        mv "$dir" "$newdir"
        echo "   ✓ Dossier renommé: $(basename "$dir") → $(basename "$newdir")"
    fi
done

# Renommer les fichiers contenant "logo-mesoigner"
find . ! \( "${EXCLUDE_DIRS[@]}" \) -type f -name "*logo-mesoigner*" | while read file; do
    newfile="${file//logo-mesoigner/logo-messoins}"
    if [ "$file" != "$newfile" ]; then
        mv "$file" "$newfile"
        echo "   ✓ Fichier renommé: $(basename "$file") → $(basename "$newfile")"
    fi
done

echo ""
echo "================================================"
echo "✅ REMPLACEMENT TERMINÉ!"
echo "================================================"
echo ""
echo "📊 Résumé:"
echo "   Fichiers modifiés: $MODIFIED_COUNT"
echo ""
echo "🔍 Vérification:"
echo ""
echo "   Domaine restant:"
grep -RIn "pharmaciecourcelles-demours-paris.mesoigner.fr" . 2>/dev/null | wc -l || echo "   0"
echo ""
echo "   Logo restant:"
grep -RIn "logo-mesoigner" . 2>/dev/null | wc -l || echo "   0"
echo ""
echo "   Thème restant:"
grep -RIn 'data-theme="mesoigner"' . 2>/dev/null | wc -l || echo "   0"
echo ""
echo "✨ Fait!"
