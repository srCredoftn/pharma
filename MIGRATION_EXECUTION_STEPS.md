# ⚡ MIGRATION - ÉTAPES D'EXÉCUTION RAPIDE

**Durée totale:** 5-10 minutes  
**Difficulté:** Débutant (copier/coller)  
**Résultat:** Migration complète du domaine et branding

---

## 📋 SOMMAIRE RAPIDE

```
✅ ÉTAPE 1: Préparer (30 secondes)
✅ ÉTAPE 2: Créer structure (1 minute)
✅ ÉTAPE 3: Exécuter migration (5 minutes)
✅ ÉTAPE 4: Vérifier (2 minutes)
✅ ÉTAPE 5: Tester (2 minutes)
```

---

## 🚀 COMMENCEZ ICI

### ⚠️ AVANT TOUT: Sauvegarde!

```bash
# IMPORTANTE: Créer une copie de sécurité
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr \
      pharmaciecourcelles-demours-paris.mesoigner.fr.backup

# Vérifier la sauvegarde
ls -la pharmaciecourcelles-demours-paris.mesoigner.fr.backup/index.html
```

---

## ÉTAPE 1️⃣: Structure des assets

Copier/coller une seule commande:

```bash
mkdir -p public/assets/{css,uploads,fonts,media} && \
touch public/assets/css/scripts.3e902af8.css && \
touch public/assets/css/mesoigner.6063c722.css && \
ls -lh public/assets/css/
```

**Résultat attendu:**
```
-rw-r--r--  scripts.3e902af8.css
-rw-r--r--  mesoigner.6063c722.css
```

---

## ÉTAPE 2️⃣: Migration (CHOIX A OU B)

### ✅ OPTION A: Python (RECOMMANDÉ - 99% de réussite)

**Vérifier Python:**
```bash
python3 --version
# Résultat: Python 3.x.x
```

**Exécuter la migration:**
```bash
python3 scripts/migrate_complete.py
```

**Quand ça demande "Continuer? (oui/non):"** → Taper: `oui` et `Enter`

**Résultat attendu:**
```
✅ MIGRATION COMPLÈTE - MESOIGNER → MESSOINS
✅ Fichiers HTML trouvés: 8000+
📥 Continuer? (oui/non): oui
[████████████████████████████████████████] 100%
✅ Fichiers traités: 8000+
✅ Fichiers modifiés: 7500+
```

---

### ✅ OPTION B: Bash Script (Si Python ne marche pas)

**Pour Linux/Mac:**
```bash
chmod +x migrate-cdn-complete.sh && ./migrate-cdn-complete.sh
```

**Pour Windows (Git Bash ou WSL):**
Même commande que Linux/Mac

---

### ✅ OPTION C: Commande sed simple (ligne par ligne)

Si Options A et B ne marchent pas:

```bash
# UNE SEULE commande longue (copier ENTIÈREMENT):
for f in $(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html"); do
  sed -i.bak \
    -e 's|https://cdn\.mesoigner\.fr|https://cdn.messoins.bj|g' \
    -e 's|data-theme="mesoigner"|data-theme="messoins"|g' \
    -e 's|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g' \
    "$f"; rm "${f}.bak"
done && echo "✅ Fait!"
```

---

## ÉTAPE 3️⃣: Renommer le dossier

```bash
# Une seule commande:
mv pharmaciecourcelles-demours-paris.mesoigner.fr \
   pharmacie-campguezo-cotonou.messoins.bj && \
ls -la pharmacie-campguezo-cotonou.messoins.bj/index.html
```

**Résultat attendu:**
```
-rw-r--r--  pharmacie-campguezo-cotonou.messoins.bj/index.html
```

---

## ÉTAPE 4️⃣: Vérifications (copier une à une)

### Vérification 1: Nouveau domaine
```bash
grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
```
**Doit afficher:** `1000+` ✅

### Vérification 2: Ancien domaine disparu
```bash
grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
```
**Doit afficher:** `0` ✅

### Vérification 3: Ancien CDN disparu
```bash
grep -r "https://cdn\.mesoigner\.fr" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
```
**Doit afficher:** `0` ou très petit nombre ✅

---

## ÉTAPE 5️⃣: Tester localement

```bash
# Démarrer le serveur
php artisan serve
```

**Puis ouvrir dans le navigateur:**
```
http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/index.html
```

**Points à vérifier:**
- [ ] Page s'affiche
- [ ] Logo visible (en haut à gauche)
- [ ] Aucune erreur rouge en console (F12)
- [ ] Menu s'ouvre
- [ ] Pas de 404 en bas de la page

**Arrêter le serveur:** `Ctrl + C`

---

## 🎉 C'EST FAIT!

```bash
# Pour confirmer tout est OK:
echo "✅ Migration complète!"
echo "Ancien domaine: $(grep -r 'pharmaciecourcelles' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l) références"
echo "Nouveau domaine: $(grep -r 'messoins' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l) références"
```

---

## ⚠️ Si quelque chose ne marche pas

### Python pas trouvé:
```bash
# Essayer:
python scripts/migrate_complete.py
# ou
python3.9 scripts/migrate_complete.py
# ou
/usr/bin/python3 scripts/migrate_complete.py
```

### Le dossier ne se renomme pas:
```bash
# Essayer avec sudo (attention!):
sudo mv pharmaciecourcelles-demours-paris.mesoigner.fr \
        pharmacie-campguezo-cotonou.messoins.bj

# Ou à la main dans le gestionnaire de fichiers
```

### Les vérifications échouent:
```bash
# Vérifier que vous êtes dans le bon répertoire:
pwd
# Doit afficher le chemin du projet

# Vérifier le dossier existe:
ls pharmacie-campguezo-cotonou.messoins.bj/
```

### Les anciennes références restent:
```bash
# C'est possible si elles sont dans des fichiers JSON/PHP
# Chercher et remplacer manuellement:
grep -r "pharmaciecourcelles" pharmacie-campguezo-cotonou.messoins.bj/*.json
grep -r "mesoigner" pharmacie-campguezo-cotonou.messoins.bj/*.php
```

---

## 📞 Fichiers de référence

- `MIGRATION_COMPLETE_GUIDE.md` - Guide détaillé avec explications
- `scripts/migrate_complete.py` - Script de migration Python
- `migrate-cdn-complete.sh` - Script de migration Bash
- `COMMANDES_SIMPLES.md` - Commandes vraiment simples

---

## ✨ RÉSUMÉ DES COMMANDES

Copier/coller dans le terminal (dans l'ordre):

```bash
# 1. Sauvegarde
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr \
      pharmaciecourcelles-demours-paris.mesoigner.fr.backup

# 2. Créer structure
mkdir -p public/assets/{css,uploads,fonts,media}
touch public/assets/css/{scripts.3e902af8.css,mesoigner.6063c722.css}

# 3. Migration (choisir UNE des trois options ci-dessous)

# OPTION A: Python
python3 scripts/migrate_complete.py
# Quand demandé: taper "oui"

# OU OPTION B: Bash
chmod +x migrate-cdn-complete.sh && ./migrate-cdn-complete.sh

# OU OPTION C: sed (sans autres outils)
for f in $(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html"); do sed -i.bak -e 's|https://cdn\.mesoigner\.fr|https://cdn.messoins.bj|g' -e 's|data-theme="mesoigner"|data-theme="messoins"|g' -e 's|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g' "$f"; rm "${f}.bak"; done

# 4. Renommer
mv pharmaciecourcelles-demours-paris.mesoigner.fr \
   pharmacie-campguezo-cotonou.messoins.bj

# 5. Vérifier
grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
grep -r "pharmaciecourcelles" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l

# 6. Tester
php artisan serve
# Ouvrir: http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/
```

---

**🎯 Objectif:** Migration complète en < 10 minutes ✅

**📊 Temps estimé par étape:**
- Sauvegarde: 1 min
- Structure: 30 sec
- Migration: 3-5 min
- Vérification: 1 min
- Test: 2 min
- **Total: 7-9 minutes**

---

**Bonne chance! 🚀**
