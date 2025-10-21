# ✅ CHECKLIST FINALE - MIGRATION PRÊTE

**Vérifiez que tout est en place avant de commencer la migration.**

---

## 📋 Fichiers et scripts

### Scripts de migration
```bash
# Vérifier que les scripts existent
test -f scripts/migrate_complete.py && echo "✅ Python script trouvé" || echo "❌ Manquant"
test -f migrate-cdn-complete.sh && echo "✅ Bash script trouvé" || echo "❌ Manquant"
test -f quick-migrate.sh && echo "✅ Quick script trouvé" || echo "❌ Manquant"
```

**Résultat attendu:**
```
✅ Python script trouvé
✅ Bash script trouvé
✅ Quick script trouvé
```

---

### Documentation
```bash
# Vérifier que les guides existent
test -f START_HERE_MIGRATION.md && echo "✅ Guide principal" || echo "❌ Manquant"
test -f MIGRATION_EXECUTION_STEPS.md && echo "✅ Étapes rapides" || echo "❌ Manquant"
test -f MIGRATION_COMPLETE_GUIDE.md && echo "✅ Guide complet" || echo "❌ Manquant"
test -f MIGRATION_SUMMARY.md && echo "✅ Résumé" || echo "❌ Manquant"
```

**Résultat attendu:**
```
✅ Guide principal
✅ Étapes rapides
✅ Guide complet
✅ Résumé
```

---

## 📁 Dossier source

### Vérifier le dossier principal
```bash
# Le dossier doit exister
test -d pharmaciecourcelles-demours-paris.mesoigner.fr && echo "✅ Dossier source existe" || echo "❌ MANQUANT!"

# Vérifier qu'il contient des fichiers
test -f pharmaciecourcelles-demours-paris.mesoigner.fr/index.html && echo "✅ index.html existe" || echo "❌ MANQUANT!"

# Compter les fichiers HTML
html_count=$(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f 2>/dev/null | wc -l)
echo "📊 Fichiers HTML: $html_count"
```

**Résultat attendu:**
```
✅ Dossier source existe
✅ index.html existe
📊 Fichiers HTML: 8000+
```

---

## 🔧 Environnement

### Vérifier Python (optionnel mais recommandé)
```bash
# Tester Python 3
python3 --version
# Résultat attendu: Python 3.x.x ou plus récent
```

### Vérifier Bash
```bash
# Tester bash
bash --version | head -1
# Résultat attendu: GNU bash, version ...
```

### Vérifier espace disque
```bash
# Vérifier l'espace disponible
df -h . | tail -1
# Résultat attendu: minimum 500 MB libres
```

---

## 📝 Index.html racine

### Vérifier la redirection
```bash
# Le fichier root/index.html doit rediriger vers nouveau domaine
grep "pharmacie-campguezo-cotonou.messoins.bj" index.html && echo "✅ Redirection mise à jour" || echo "⚠️  Ancienne redirection"
```

**Résultat attendu:**
```
✅ Redirection mise à jour
```

---

## 🎯 État pré-migration

### Résumé complet
```bash
echo "========================================="
echo "ÉTAT PRÉ-MIGRATION"
echo "========================================="
echo ""
echo "📁 DOSSIERS:"
test -d pharmaciecourcelles-demours-paris.mesoigner.fr && echo "  ✅ Dossier source" || echo "  ❌ Dossier source manquant"
test ! -d pharmacie-campguezo-cotonou.messoins.bj && echo "  ✅ Dossier cible n'existe pas" || echo "  ⚠️  Dossier cible existe déjà"
test ! -d public/assets && echo "  ✅ Assets non créés (ok)" || echo "  ⚠️  Assets déjà créés"
echo ""
echo "📄 FICHIERS:"
test -f scripts/migrate_complete.py && echo "  ✅ migrate_complete.py" || echo "  ❌ migrate_complete.py manquant"
test -f migrate-cdn-complete.sh && echo "  ✅ migrate-cdn-complete.sh" || echo "  ❌ migrate-cdn-complete.sh manquant"
test -f START_HERE_MIGRATION.md && echo "  ✅ Documentation" || echo "  ❌ Documentation manquante"
echo ""
echo "📊 DONNÉES:"
html_count=$(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f 2>/dev/null | wc -l)
echo "  📈 Fichiers HTML: $html_count"
size=$(du -sh pharmaciecourcelles-demours-paris.mesoigner.fr 2>/dev/null | cut -f1)
echo "  💾 Taille du dossier: $size"
echo ""
echo "========================================="
```

---

## ✅ Vérifications individuelles à faire

### ✓ Sauvegarde
```bash
# Créer une sauvegarde MAINTENANT
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr \
      pharmaciecourcelles-demours-paris.mesoigner.fr.backup

# Vérifier qu'elle existe
test -d pharmaciecourcelles-demours-paris.mesoigner.fr.backup && echo "✅ Sauvegarde créée"
```

### ✓ Espace disque
```bash
# Vérifier minimum 500 MB
available=$(df . | tail -1 | awk '{print $4}')
if [ "$available" -gt 500000 ]; then
  echo "✅ Espace disque suffisant: $(($available / 1024)) MB"
else
  echo "❌ Espace disque insuffisant!"
fi
```

### ✓ Permissions
```bash
# Vérifier permissions de lecture/écriture
test -r pharmaciecourcelles-demours-paris.mesoigner.fr && echo "✅ Lecture OK"
test -w . && echo "✅ Écriture OK"
```

### ✓ Accès au répertoire
```bash
# Vous devez être dans le bon répertoire
pwd
# Doit afficher le chemin du projet
```

---

## 🚨 ATTENTION - Points critiques

### ⚠️ Avant de commencer:

| Vérification | Commande | OK? |
|---|---|---|
| Sauvegarde existe | `test -d *backup` | ☐ |
| Python ou Bash disponible | `python3 --version` ou `bash --version` | ☐ |
| Espace disque > 500MB | `df -h .` | ☐ |
| Dossier source existe | `test -d pharmaciecourcelles*` | ☐ |
| Pas d'accès concurrents | Aucun autre programme ne modifie le dossier | ☐ |
| Documentation lue | Au moins `MIGRATION_EXECUTION_STEPS.md` | ☐ |

---

## 🎯 Choix de la méthode

### Méthode recommandée
```
✅ Python + scripts/migrate_complete.py
   - Fonctionnera sur Windows, Mac, Linux
   - Rapport détaillé
   - Récupération possible en cas d'erreur
```

### Méthode alternative
```
✅ Bash + migrate-cdn-complete.sh
   - Natif sur Mac/Linux
   - Plus rapide
   - Moins de dépendances
```

### Méthode manuelle
```
✅ Commandes sed directes
   - Maximum de contrôle
   - À faire ligne par ligne
   - Pour experts
```

---

## 📊 Statistiques pré-migration

```bash
#!/bin/bash
# Exécuter ce script pour un résumé complet

echo "📊 STATISTIQUES DE MIGRATION"
echo "======================================"
echo ""

# Dossier
if [ -d "pharmaciecourcelles-demours-paris.mesoigner.fr" ]; then
  size=$(du -sh pharmaciecourcelles-demours-paris.mesoigner.fr 2>/dev/null | cut -f1)
  count=$(find pharmaciecourcelles-demours-paris.mesoigner.fr -type f | wc -l)
  html=$(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" | wc -l)
  
  echo "Source: pharmaciecourcelles-demours-paris.mesoigner.fr"
  echo "  Taille: $size"
  echo "  Fichiers totaux: $count"
  echo "  Fichiers HTML: $html"
  echo ""
fi

# Domaines actuels
echo "Domaines/URLs actuels:"
if grep -r "pharmaciecourcelles-demours-paris.mesoigner.fr" pharmaciecourcelles-demours-paris.mesoigner.fr/ 2>/dev/null | wc -l | grep -q "^0$"; then
  echo "  Ancien domaine: DÉJÀ MIGRÉ"
else
  count=$(grep -r "pharmaciecourcelles-demours-paris.mesoigner.fr" pharmaciecourcelles-demours-paris.mesoigner.fr/ 2>/dev/null | wc -l)
  echo "  Ancien domaine: $count références"
fi

cdn=$(grep -r "https://cdn\.mesoigner\.fr" pharmaciecourcelles-demours-paris.mesoigner.fr/ 2>/dev/null | wc -l)
echo "  CDN mesoigner: $cdn références"
echo ""

echo "======================================"
echo "✅ Prêt pour migration"
```

---

## 🟢 FEUX VERTS - Vous pouvez commencer si:

- ✅ Dossier source existe avec 8000+ fichiers HTML
- ✅ Sauvegarde créée
- ✅ Python 3 OU Bash disponible
- ✅ 500 MB+ d'espace disque libre
- ✅ Vous êtes dans le bon répertoire du projet
- ✅ Vous avez lu `MIGRATION_EXECUTION_STEPS.md`
- ✅ Pas d'autres programmes modifiant le dossier

---

## 🟡 FEUX JAUNES - Attention:

- ⚠️ Dossier `pharmacie-campguezo-cotonou.messoins.bj` existe déjà
- ⚠️ Espace disque faible (< 1 GB libre)
- ⚠️ Python et Bash tous deux manquants
- ⚠️ Dossier source semble vide (< 100 fichiers HTML)

---

## 🔴 FEUX ROUGES - ARRÊTEZ:

- ❌ Dossier source n'existe pas
- ❌ Sauvegarde n'existe pas et vous êtes prêt à commencer
- ❌ Espace disque < 100 MB
- ❌ Pas de permissions en lecture/écriture
- ❌ Plusieurs personnes accèdent au dossier en même temps

---

## ✨ Prochaines étapes

### Si tout est OK:
1. Ouvrir `MIGRATION_EXECUTION_STEPS.md`
2. Copier/coller les commandes dans l'ordre
3. Vérifier que chaque étape réussit
4. Tester localement avec `php artisan serve`

### Si problème:
1. Consulter `MIGRATION_COMPLETE_GUIDE.md` section "Dépannage"
2. Restaurer la sauvegarde si nécessaire
3. Recommencer depuis le début

---

## 📞 Support

**Documentation incluse:**
- `MIGRATION_EXECUTION_STEPS.md` - Étapes rapides
- `MIGRATION_COMPLETE_GUIDE.md` - Guide détaillé
- `COMMANDES_SIMPLES.md` - Juste les commandes

**Scripts disponibles:**
- `scripts/migrate_complete.py` - Python (recommandé)
- `migrate-cdn-complete.sh` - Bash
- `quick-migrate.sh` - Alternative

---

## 🎯 Statut final

```
┌─────────────────────────────────────────┐
│   ✅ MIGRATION PRÊTE À COMMENCER        │
│                                          │
│   Tous les scripts et documents sont    │
│   en place. Vous pouvez maintenant      │
│   exécuter la migration!                │
│                                          │
│   → MIGRATION_EXECUTION_STEPS.md        │
└─────────────────────────────────────────┘
```

---

**Version:** 1.0  
**Date:** Octobre 2025  
**État:** ✅ Prêt pour production
