#!/bin/bash

# 🚀 Quick Migration Script
# Effectue tous les find/replace en une seule passe

echo "🔄 Démarrage de la migration CDN rapide..."
echo "   mesoigner → messoins"
echo ""

# Vérifier que le dossier existe
if [ ! -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
    echo "❌ Dossier pharmaciecourcelles-demours-paris.mesoigner.fr non trouvé!"
    exit 1
fi

# Créer la structure si elle n'existe pas
mkdir -p public/assets/css
mkdir -p public/assets/uploads

echo "📝 Traitement des fichiers HTML..."
count=0

# Effectuer tous les remplacements avec sed
# Utiliser -i avec backup (.bak) pour sécurité, puis supprimer les backups
for file in $(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f); do
    # Remplacements CSS/JS
    sed -i.bak \
        -e 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/scripts\.3e902af8\.css|/assets/css/scripts.3e902af8.css|g' \
        -e 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/mesoigner\.6063c722\.css|/assets/css/mesoigner.6063c722.css|g' \
        -e 's|https://cdn\.mesoigner\.fr/uploads/logos/logo-mesoigner\.svg|/assets/uploads/logo-messoins.svg|g' \
        -e 's|https://cdn\.mesoigner\.fr/src/img/layout/header-wrapper\.png|/assets/uploads/header-wrapper.png|g' \
        -e 's|https://cdn\.mesoigner\.fr/src/img/widgets/que-prendre/que-prendre\.png|/assets/uploads/que-prendre.png|g' \
        \
        -e 's|data-theme="mesoigner"|data-theme="messoins"|g' \
        -e 's|logo-mesoigner|logo-messoins|g' \
        -e 's|mesoigner\.svg|messoins.svg|g' \
        \
        -e 's|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g' \
        -e 's|https://cdn\.mesoigner\.fr|https://cdn.messoins.bj|g' \
        \
        "$file"
    
    rm -f "${file}.bak"
    
    count=$((count + 1))
    if [ $((count % 500)) -eq 0 ]; then
        echo "  ✅ $count fichiers traités..."
    fi
done

echo ""
echo "✅ Migration terminée!"
echo "   $count fichiers HTML modifiés"
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Vérifier: grep -r 'mesoigner' pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l"
echo "   2. Renommer: mv pharmaciecourcelles-demours-paris.mesoigner.fr/ pharmacie-campguezo-cotonou.messoins.bj/"
echo "   3. Tester: php artisan serve"
echo ""
echo "✅ Fait!"
