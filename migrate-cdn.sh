#!/bin/bash

# Script de migration CDN: mesoigner → messoins
# Remplace tous les liens CDN dans les fichiers HTML

echo "🔄 Démarrage de la migration CDN..."
echo "  mesoigner → messoins"
echo "  pharmaciecourcelles-demours-paris.mesoigner.fr → pharmacie-campguezo-cotonou.messoins.bj"
echo ""

# Vérifier que le dossier existe
if [ ! -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
    echo "❌ Dossier pharmaciecourcelles-demours-paris.mesoigner.fr non trouvé!"
    exit 1
fi

# Créer la structure des assets locaux
echo "📁 Création de la structure des assets..."
mkdir -p public/assets/css
mkdir -p public/assets/uploads
mkdir -p public/assets/img

# Télécharger les CSS depuis le CDN
echo "⬇️  Téléchargement des CSS..."
curl -s -o public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css"
curl -s -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"

# Télécharger les images
echo "⬇️  Téléchargement des images..."
curl -s -o public/assets/uploads/header-wrapper.png "https://cdn.mesoigner.fr/src/img/layout/header-wrapper.png"
curl -s -o public/assets/uploads/que-prendre.png "https://cdn.mesoigner.fr/src/img/widgets/que-prendre/que-prendre.png"

# Remplacer les URLs CDN dans tous les fichiers HTML
echo "🔄 Remplacement des URLs CDN..."

count=0
for file in $(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f); do
    # Remplacer les URLs CDN par des chemins locaux
    sed -i 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/scripts\.3e902af8\.css|/assets/css/scripts.3e902af8.css|g' "$file"
    sed -i 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/mesoigner\.6063c722\.css|/assets/css/mesoigner.6063c722.css|g' "$file"
    sed -i 's|https://cdn\.mesoigner\.fr/uploads/logos/logo-mesoigner\.svg|/assets/uploads/logo-messoins.svg|g' "$file"
    sed -i 's|https://cdn\.mesoigner\.fr/src/img/layout/header-wrapper\.png|/assets/uploads/header-wrapper.png|g' "$file"
    sed -i 's|https://cdn\.mesoigner\.fr/src/img/widgets/que-prendre/que-prendre\.png|/assets/uploads/que-prendre.png|g' "$file"
    
    # Remplacer les références à mesoigner.svg et autres ressources CDN
    sed -i 's|https://cdn\.mesoigner\.fr|/assets|g' "$file"
    
    # Remplacer le branding mesoigner → messoins
    sed -i 's|data-theme="mesoigner"|data-theme="messoins"|g' "$file"
    sed -i 's|logo-mesoigner|logo-messoins|g' "$file"
    sed -i 's|mesoigner\.svg|messoins.svg|g' "$file"
    sed -i 's|cdn\.mesoigner\.fr|cdn.messoins.bj|g' "$file"
    
    # Remplacer les domaines
    sed -i 's|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g' "$file"
    sed -i 's|https://pharmaciecourcelles-demours-paris\.mesoigner\.fr|https://pharmacie-campguezo-cotonou.messoins.bj|g' "$file"
    
    count=$((count + 1))
    if [ $((count % 100)) -eq 0 ]; then
        echo "  ✅ $count fichiers traités..."
    fi
done

echo ""
echo "✅ Migration terminée!"
echo "   $count fichiers HTML mises à jour"
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Vérifier les CSS/JS en accédant à /assets/css/"
echo "   2. Les images manquantes seront servies avec des erreurs 404"
echo "   3. Renommer le dossier si nécessaire:"
echo "      mv pharmaciecourcelles-demours-paris.mesoigner.fr/ pharmacie-campguezo-cotonou.messoins.bj/"
echo ""
echo "✅ Terminé! Le projet utilise maintenant des assets locaux."
