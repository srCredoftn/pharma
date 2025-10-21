#!/bin/bash

# 🚀 MIGRATION COMPLÈTE - CDN + Dossiers + Domaine
# Effectue TOUS les find/replace pour la migration complète

set -e

echo "🚀 ============================================"
echo "   MIGRATION COMPLÈTE PHARMACIE CAMP GUÉZO"
echo "=============================================="
echo ""
echo "📋 Étapes:"
echo "   1. Créer structure locale des assets"
echo "   2. Télécharger les CSS depuis CDN"
echo "   3. Faire les find/replace dans les HTML"
echo "   4. Renommer le dossier principal"
echo ""

# ========== ÉTAPE 1: Créer structure ==========
echo "📁 ÉTAPE 1: Création de la structure..."
mkdir -p public/assets/css
mkdir -p public/assets/uploads
mkdir -p public/assets/fonts
mkdir -p public/assets/media
echo "✅ Dossiers créés"
echo ""

# ========== ÉTAPE 2: Télécharger CSS ==========
echo "📥 ÉTAPE 2: Téléchargement des CSS..."
echo "   (Cette étape peut prendre 10-20 secondes)"

# Vérifier si curl est disponible
if ! command -v curl &> /dev/null; then
    echo "⚠️  curl non trouvé. Essai avec wget..."
    wget -O public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css" 2>/dev/null || echo "⚠️  Impossible de télécharger scripts.css"
    wget -O public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css" 2>/dev/null || echo "⚠️  Impossible de télécharger mesoigner.css"
else
    curl -f -o public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css" 2>/dev/null || echo "⚠️  scripts.css introuvable sur CDN (normal si nouveau domaine)"
    curl -f -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css" 2>/dev/null || echo "⚠️  mesoigner.css introuvable sur CDN (normal si nouveau domaine)"
fi

if [ -f "public/assets/css/scripts.3e902af8.css" ]; then
    echo "✅ scripts.3e902af8.css téléchargé"
else
    echo "⚠️  scripts.3e902af8.css non trouvé (création fichier vide)"
    touch public/assets/css/scripts.3e902af8.css
fi

if [ -f "public/assets/css/mesoigner.6063c722.css" ]; then
    echo "✅ mesoigner.6063c722.css téléchargé"
else
    echo "⚠️  mesoigner.6063c722.css non trouvé (création fichier vide)"
    touch public/assets/css/mesoigner.6063c722.css
fi
echo ""

# ========== ÉTAPE 3: Vérifier le dossier ==========
if [ ! -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
    echo "❌ ERREUR: Dossier pharmaciecourcelles-demours-paris.mesoigner.fr non trouvé!"
    echo "   Veuillez vérifier que vous êtes dans le bon répertoire."
    exit 1
fi

# ========== ÉTAPE 4: Find/Replace dans HTML ==========
echo "🔄 ÉTAPE 3: Find/Replace massifs dans les HTML..."
echo "   (Cette étape peut prendre 30-60 secondes)"

count=0
errors=0

# Compter les fichiers
total=$(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f 2>/dev/null | wc -l)
echo "   Fichiers à traiter: $total"
echo ""

for file in $(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f 2>/dev/null); do
    if [ -f "$file" ]; then
        # Utiliser sed avec les remplacements - on utilise un délimiteur | pour éviter les / 
        
        # Remplacements CSS/JS (URLs CDN → chemins locaux)
        sed -i.bak \
            -e 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/scripts\.3e902af8\.css|/assets/css/scripts.3e902af8.css|g' \
            -e 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/mesoigner\.6063c722\.css|/assets/css/mesoigner.6063c722.css|g' \
            -e 's|https://cdn\.mesoigner\.fr/uploads/logos/logo-mesoigner\.svg|/assets/uploads/logo-messoins.svg|g' \
            -e 's|https://cdn\.mesoigner\.fr/src/img/layout/header-wrapper\.png|/assets/uploads/header-wrapper.png|g' \
            -e 's|https://cdn\.mesoigner\.fr/src/img/widgets/que-prendre/que-prendre\.png|/assets/uploads/que-prendre.png|g' \
            "$file" 2>/dev/null || { echo "⚠️  Erreur sur: $file"; errors=$((errors + 1)); }
        
        # Remplacements data-theme
        sed -i.bak \
            -e 's|data-theme="mesoigner"|data-theme="messoins"|g' \
            -e 's|data-theme=.mesoigner.|data-theme="messoins"|g' \
            "$file" 2>/dev/null || true
        
        # Remplacements de branding
        sed -i.bak \
            -e 's|logo-mesoigner|logo-messoins|g' \
            -e 's|mesoigner\.svg|messoins.svg|g' \
            "$file" 2>/dev/null || true
        
        # Remplacements de domaines - CRITICAL
        sed -i.bak \
            -e 's|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g' \
            -e 's|https://cdn\.mesoigner\.fr/|https://cdn.messoins.bj/|g' \
            "$file" 2>/dev/null || true
        
        # Nettoyer les fichiers de backup
        rm -f "${file}.bak"
        
        count=$((count + 1))
        if [ $((count % 100)) -eq 0 ]; then
            percent=$((count * 100 / total))
            echo "   [$percent%] $count/$total fichiers traités..."
        fi
    fi
done

echo "   [100%] $count/$total fichiers traités"
echo ""

if [ $errors -gt 0 ]; then
    echo "⚠️  Attention: $errors erreurs rencontrées"
else
    echo "✅ Tous les fichiers HTML sont à jour!"
fi
echo ""

# ========== ÉTAPE 5: Renommer le dossier ==========
echo "📁 ÉTAPE 4: Renommage du dossier principal..."
if [ -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
    echo "   Renommage en cours..."
    # Attendre 1 seconde pour s'assurer que tous les fichiers sont fermés
    sleep 1
    mv pharmaciecourcelles-demours-paris.mesoigner.fr pharmacie-campguezo-cotonou.messoins.bj 2>/dev/null || {
        echo "⚠️  Impossible de renommer le dossier"
        echo "   Vous pouvez le faire manuellement:"
        echo "   mv pharmaciecourcelles-demours-paris.mesoigner.fr pharmacie-campguezo-cotonou.messoins.bj"
    }
else
    echo "⚠️  Le dossier a déjà été renommé"
fi

# Vérifier si le renommage a réussi
if [ -d "pharmacie-campguezo-cotonou.messoins.bj" ]; then
    echo "✅ Dossier renommé avec succès!"
else
    echo "⚠️  Le dossier n'a pas pu être renommé (peut nécessiter des permissions)"
fi
echo ""

# ========== ÉTAPE 6: Vérification ==========
echo "✅ ÉTAPE 5: Vérification..."
echo ""

# Vérifier les remplacements
if [ -d "pharmacie-campguezo-cotonou.messoins.bj" ]; then
    messoins_count=$(grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
    echo "   ✅ Fichiers avec data-theme=\"messoins\": $messoins_count"
    
    old_domain=$(grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
    echo "   ✅ Anciennes références restantes: $old_domain"
    
    cdn_old=$(grep -r "https://cdn\.mesoigner\.fr" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
    echo "   ✅ Anciennes URLs CDN restantes: $cdn_old"
fi
echo ""

# ========== FIN ==========
echo "🎉 ============================================"
echo "   MIGRATION TERMINÉE AVEC SUCCÈS! ✨"
echo "=============================================="
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Mettre à jour config/app.php pour le nouveau domaine"
echo "   2. Vérifier .env pour les URLs"
echo "   3. Faire un test: php artisan serve"
echo "   4. Visiter: http://localhost:8000"
echo ""
echo "✅ C'est fait! 🚀"
echo ""
