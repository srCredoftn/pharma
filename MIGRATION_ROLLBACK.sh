#!/bin/bash

# 🔄 ROLLBACK SCRIPT - Restaurer la migration si problème

set -e

echo "⚠️  ============================================"
echo "   ROLLBACK - Restauration de la migration"
echo "=============================================="
echo ""

# Vérifier si la sauvegarde existe
if [ ! -d "pharmaciecourcelles-demours-paris.mesoigner.fr.backup" ]; then
    echo "❌ ERREUR: Sauvegarde introuvable!"
    echo "   pharmaciecourcelles-demours-paris.mesoigner.fr.backup"
    echo ""
    echo "   La sauvegarde n'existe pas. Impossible de restaurer."
    echo "   Vous devrez restaurer manuellement ou à partir d'un backup."
    exit 1
fi

echo "⚠️  Ceci va SUPPRIMER le dossier migré et restaurer l'original."
echo ""
echo "À faire AVANT de continuer:"
echo "  1. Arrêter le serveur (Ctrl+C si actif)"
echo "  2. Fermer tous les fichiers du dossier dans l'éditeur"
echo "  3. Vérifier que vous êtes au bon endroit"
echo ""
read -p "Êtes-vous SÛR de vouloir continuer? (oui/non): " confirm

if [ "$confirm" != "oui" ] && [ "$confirm" != "yes" ] && [ "$confirm" != "o" ] && [ "$confirm" != "y" ]; then
    echo "Rollback annulé."
    exit 0
fi

echo ""
echo "🔄 Restauration en cours..."
echo ""

# Supprimer le dossier migré
if [ -d "pharmacie-campguezo-cotonou.messoins.bj" ]; then
    echo "  Suppression de pharmacie-campguezo-cotonou.messoins.bj..."
    rm -rf pharmacie-campguezo-cotonou.messoins.bj
    echo "  ✅ Supprimé"
else
    echo "  ℹ️  Dossier cible n'existe pas (c'est ok)"
fi

echo ""

# Restaurer la sauvegarde
if [ -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
    echo "❌ ATTENTION: Le dossier original existe déjà!"
    echo "   Cela ne devrait pas arriver. Vérifier l'état."
    read -p "Voulez-vous le supprimer avant la restauration? (oui/non): " del_confirm
    
    if [ "$del_confirm" = "oui" ] || [ "$del_confirm" = "yes" ] || [ "$del_confirm" = "o" ] || [ "$del_confirm" = "y" ]; then
        echo "  Suppression du dossier existant..."
        rm -rf pharmaciecourcelles-demours-paris.mesoigner.fr
        echo "  ✅ Supprimé"
    else
        echo "❌ Impossible de continuer. Le dossier existe déjà."
        exit 1
    fi
fi

echo ""
echo "  Restauration de la sauvegarde..."
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr.backup \
      pharmaciecourcelles-demours-paris.mesoigner.fr
echo "  ✅ Restauré"

echo ""
echo "✅ ============================================"
echo "   ROLLBACK COMPLÉTÉ"
echo "=============================================="
echo ""

# Vérifier l'état
if [ -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
    echo "✅ Dossier original restauré: pharmaciecourcelles-demours-paris.mesoigner.fr"
    echo ""
    echo "État:"
    echo "  ✅ Ancien dossier restauré"
    
    if [ ! -d "pharmacie-campguezo-cotonou.messoins.bj" ]; then
        echo "  ✅ Dossier migré supprimé"
    else
        echo "  ⚠️  Dossier migré existe toujours"
    fi
    
    if [ -d "pharmaciecourcelles-demours-paris.mesoigner.fr.backup" ]; then
        echo "  ✅ Sauvegarde existe toujours (vous pouvez la supprimer)"
        echo ""
        echo "Pour nettoyer complètement:"
        echo "  rm -rf pharmaciecourcelles-demours-paris.mesoigner.fr.backup"
    fi
else
    echo "❌ ERREUR: Le rollback n'a pas fonctionné!"
    echo "   Le dossier pharmaciecourcelles-demours-paris.mesoigner.fr n'existe pas."
    exit 1
fi

echo ""
echo "✅ Vous pouvez maintenant relancer la migration si nécessaire"
echo ""
