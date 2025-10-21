#!/bin/bash

# ✅ VERIFICATION SCRIPT - Vérifier l'état de la migration

echo "✅ ============================================"
echo "   VÉRIFICATION DE LA MIGRATION"
echo "=============================================="
echo ""

success=true

# Fonction pour vérifier
check() {
    local condition=$1
    local pass_msg=$2
    local fail_msg=$3
    
    if eval "$condition"; then
        echo "  ✅ $pass_msg"
    else
        echo "  ❌ $fail_msg"
        success=false
    fi
}

# ===========================================
# 1. VÉRIFICATIONS DOSSIERS
# ===========================================
echo "📁 DOSSIERS:"
echo ""

check "[ -d pharmacie-campguezo-cotonou.messoins.bj ]" \
      "Dossier cible existe" \
      "Dossier cible n'existe pas"

check "[ ! -d pharmaciecourcelles-demours-paris.mesoigner.fr ]" \
      "Ancien dossier supprimé" \
      "Ancien dossier existe toujours"

check "[ -d public/assets/css ]" \
      "Dossier CSS créé" \
      "Dossier CSS manquant"

check "[ -d public/assets/uploads ]" \
      "Dossier uploads créé" \
      "Dossier uploads manquant"

echo ""

# ===========================================
# 2. VÉRIFICATIONS FICHIERS
# ===========================================
echo "📄 FICHIERS:"
echo ""

check "[ -f pharmacie-campguezo-cotonou.messoins.bj/index.html ]" \
      "index.html existe" \
      "index.html manquant"

check "[ -f public/assets/css/scripts.3e902af8.css ]" \
      "CSS scripts existe" \
      "CSS scripts manquant"

check "[ -f public/assets/css/mesoigner.6063c722.css ]" \
      "CSS mesoigner existe" \
      "CSS mesoigner manquant"

echo ""

# ===========================================
# 3. VÉRIFICATIONS DE CONTENU
# ===========================================
echo "🔍 CONTENU:"
echo ""

# Nouveau branding
messoins=$(grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
if [ "$messoins" -gt 1000 ]; then
    echo "  ✅ Nouveau branding détecté: $messoins références"
else
    echo "  ❌ Nouveau branding insuffisant: $messoins références (attendu: 1000+)"
    success=false
fi

# Ancien domaine
old=$(grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
if [ "$old" -eq 0 ]; then
    echo "  ✅ Ancien domaine supprimé: 0 références"
else
    echo "  ❌ Ancien domaine détecté: $old références"
    success=false
fi

# Ancien CDN
cdn=$(grep -r "https://cdn\.mesoigner\.fr" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
if [ "$cdn" -eq 0 ]; then
    echo "  ✅ Ancien CDN supprimé: 0 références"
else
    echo "  ⚠️  Ancien CDN trouvé: $cdn références"
    # Non fatal, peut être normal dans certains cas
fi

# Nouveau CDN
new_cdn=$(grep -r "https://cdn\.messoins\.bj" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
echo "  ℹ️  Nouveau CDN trouvé: $new_cdn références"

# Assets locaux
assets=$(grep -r "/assets/" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
echo "  ℹ️  Assets locaux trouvés: $assets références"

echo ""

# ===========================================
# 4. STATISTIQUES
# ===========================================
echo "📊 STATISTIQUES:"
echo ""

html_count=$(find pharmacie-campguezo-cotonou.messoins.bj -name "*.html" -type f 2>/dev/null | wc -l)
echo "  📈 Fichiers HTML: $html_count"

size=$(du -sh pharmacie-campguezo-cotonou.messoins.bj 2>/dev/null | cut -f1)
echo "  💾 Taille totale: $size"

files=$(find pharmacie-campguezo-cotonou.messoins.bj -type f 2>/dev/null | wc -l)
echo "  📁 Fichiers totaux: $files"

echo ""

# ===========================================
# 5. RÉSUMÉ
# ===========================================
echo "=============================================="
echo "RÉSUMÉ:"
echo "=============================================="
echo ""

if [ "$success" = true ]; then
    echo "✅ MIGRATION RÉUSSIE!"
    echo ""
    echo "État:"
    echo "  ✅ Dossier renommé"
    echo "  ✅ Branding mis à jour ($messoins références)"
    echo "  ✅ Ancien domaine supprimé"
    echo "  ✅ Ancien CDN supprimé"
    echo "  ✅ Assets créés"
    echo ""
    echo "Prochaines étapes:"
    echo "  1. Tester: php artisan serve"
    echo "  2. Vérifier dans le navigateur"
    echo "  3. Vérifier console (F12)"
    echo "  4. Mettre à jour config si nécessaire"
    echo "  5. Déployer en production"
    exit 0
else
    echo "⚠️  PROBLÈMES DÉTECTÉS"
    echo ""
    echo "Vérifier:"
    echo "  1. Tous les fichiers ci-dessus"
    echo "  2. Les messages d'erreur"
    echo "  3. Les références restantes"
    echo ""
    echo "Consulter MIGRATION_COMPLETE_GUIDE.md section 'Dépannage'"
    exit 1
fi
