# 🚀 GUIDE COMPLET DE MIGRATION

**De:** `pharmaciecourcelles-demours-paris.mesoigner.fr`  
**À:** `pharmacie-campguezo-cotonou.messoins.bj`

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#vue-densemble)
2. [Préparation](#préparation)
3. [Étape 1: Structure locale des assets](#étape-1-structure-locale-des-assets)
4. [Étape 2: Mass find/replace](#étape-2-mass-findreplace)
5. [Étape 3: Renommer le dossier](#étape-3-renommer-le-dossier)
6. [Étape 4: Configuration Laravel](#étape-4-configuration-laravel)
7. [Étape 5: Vérification](#étape-5-vérification)
8. [Dépannage](#dépannage)

---

## 🎯 Vue d'ensemble

Cette migration effectue **5 remplacements majeurs**:

1. **CDN CSS/JS** → chemins locaux
   - `https://cdn.mesoigner.fr/dist/.../*.css` → `/assets/css/*.css`
   
2. **CDN Assets** → chemins locaux
   - `https://cdn.mesoigner.fr/uploads/logos/logo-mesoigner.svg` → `/assets/uploads/logo-messoins.svg`
   - `https://cdn.mesoigner.fr/src/img/.../*` → `/assets/uploads/*`

3. **Data-theme**
   - `data-theme="mesoigner"` → `data-theme="messoins"`

4. **Logo/Branding**
   - `logo-mesoigner` → `logo-messoins`
   - `mesoigner.svg` → `messoins.svg`

5. **Domaine**
   - `pharmaciecourcelles-demours-paris.mesoigner.fr` → `pharmacie-campguezo-cotonou.messoins.bj`
   - `https://cdn.mesoigner.fr/` → `https://cdn.messoins.bj/`

**Scope:** ~8000 fichiers HTML, ~300MB de contenu

---

## ✅ Préparation

### Vérifier la structure
```bash
# Vérifier que le dossier existe
ls -la pharmaciecourcelles-demours-paris.mesoigner.fr/
```

### Faire une sauvegarde (IMPORTANT!)
```bash
# Créer une copie de sécurité
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr pharmaciecourcelles-demours-paris.mesoigner.fr.backup
```

---

## 🔧 ÉTAPE 1: Structure locale des assets

### 1.1 Créer les dossiers
```bash
mkdir -p public/assets/css
mkdir -p public/assets/uploads
mkdir -p public/assets/fonts
mkdir -p public/assets/media
```

### 1.2 Télécharger les CSS (OPTIONNEL - ils peuvent être vides)

Si vous avez les CSS disponibles:

```bash
# CSS 1 (22KB)
curl -o public/assets/css/scripts.3e902af8.css \
  "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css"

# CSS 2 (271KB)
curl -o public/assets/css/mesoigner.6063c722.css \
  "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"
```

**Vérifier:**
```bash
ls -lh public/assets/css/
```

Si les fichiers n'existent pas, créer des fichiers vides:
```bash
touch public/assets/css/scripts.3e902af8.css
touch public/assets/css/mesoigner.6063c722.css
```

---

## 🔄 ÉTAPE 2: Mass find/replace

### Option A: Script Python (RECOMMANDÉ)

**Avantages:**
- Fonctionne sur tous les OS (Windows, Mac, Linux)
- Rapport détaillé
- Sûr et testé

**Installation:**
```bash
# Vérifier que Python 3 est installé
python3 --version

# Ou sur Windows:
python --version
```

**Exécution:**
```bash
# Exécuter le script
python3 scripts/migrate_complete.py

# Ou sur Windows:
python scripts/migrate_complete.py
```

**Résultat attendu:**
```
✅ Fichiers traités: 8000+
✅ Fichiers modifiés: 7500+
✅ Références au nouveau domaine (messoins): 15000+
✅ Anciennes références restantes: 0
```

---

### Option B: Script Bash (si Python n'est pas disponible)

**Pour Linux/Mac:**
```bash
# Rendre exécutable
chmod +x migrate-cdn-complete.sh

# Exécuter
./migrate-cdn-complete.sh
```

---

### Option C: Utiliser sed directement (ligne par ligne)

Si vous préférez faire à la main (pour contrôle maximal):

```bash
# Remplacements CSS/JS
for file in $(find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f); do
  sed -i.bak \
    -e 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/scripts\.3e902af8\.css|/assets/css/scripts.3e902af8.css|g' \
    -e 's|https://cdn\.mesoigner\.fr/dist/front_pharmacies/mesoigner\.6063c722\.css|/assets/css/mesoigner.6063c722.css|g' \
    -e 's|data-theme="mesoigner"|data-theme="messoins"|g' \
    -e 's|logo-mesoigner|logo-messoins|g' \
    -e 's|pharmaciecourcelles-demours-paris\.mesoigner\.fr|pharmacie-campguezo-cotonou.messoins.bj|g' \
    "$file"
  rm "${file}.bak"
done
```

---

## 📁 ÉTAPE 3: Renommer le dossier

### Après les find/replace, renommer le dossier principal:

```bash
# Renommer
mv pharmaciecourcelles-demours-paris.mesoigner.fr \
   pharmacie-campguezo-cotonou.messoins.bj
```

### Vérifier:
```bash
# Le dossier doit exister avec le nouveau nom
ls -la pharmacie-campguezo-cotonou.messoins.bj/

# L'ancien dossier ne doit pas exister
ls -la pharmaciecourcelles-demours-paris.mesoigner.fr/ 2>&1 | grep -q "No such file"
```

---

## ⚙️ ÉTAPE 4: Configuration Laravel

### 4.1 Vérifier config/app.php

```php
// Vérifier ou mettre à jour l'URL de l'application
'url' => env('APP_URL', 'https://pharmacie-campguezo-cotonou.messoins.bj'),

// Asset URL
'asset_url' => env('ASSET_URL', 'https://pharmacie-campguezo-cotonou.messoins.bj'),
```

### 4.2 Vérifier .env

```env
APP_URL=https://pharmacie-campguezo-cotonou.messoins.bj
ASSET_URL=https://pharmacie-campguezo-cotonou.messoins.bj
```

### 4.3 Si utilisant une base de données (si nécessaire)

```bash
# Mettre en cache la configuration
php artisan config:cache
```

---

## ✔️ ÉTAPE 5: Vérification

### 5.1 Vérifier le nombre de fichiers traités

```bash
# Doit retourner 1000+
grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l

# Exemple de résultat:
# 1523
```

### 5.2 Vérifier qu'il n'y a pas d'anciennes URL

```bash
# Doit retourner 0
grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l

# Exemple de résultat:
# 0
```

### 5.3 Vérifier les anciennes URL CDN

```bash
# Doit retourner 0 (ou un petit nombre acceptable)
grep -r "https://cdn\.mesoigner\.fr" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l

# Exemple de résultat:
# 0
```

### 5.4 Tester le serveur local

```bash
# Démarrer le serveur
php artisan serve

# Ouvrir dans le navigateur:
# http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/
```

### 5.5 Points de vérification dans le navigateur

- ✅ Page s'affiche correctement
- ✅ Logo visible (pas de 404)
- ✅ CSS chargé (pas de style cassé)
- ✅ Images affichées
- ✅ Pas de messages d'erreur en console

---

## 🔍 Vérifications avancées

### Chercher les fichiers non modifiés

```bash
# Chercher les fichiers HTML qui n'ont pas data-theme="messoins"
find pharmacie-campguezo-cotonou.messoins.bj -name "*.html" \
  ! -exec grep -l 'data-theme="messoins"' {} \; | head -10
```

### Vérifier les URL relatives cassées

```bash
# Chercher les chemins relatifs qui peuvent être problématiques
grep -r "\.\.\/cdn\." pharmacie-campguezo-cotonou.messoins.bj/ | head -5
```

### Vérifier les images data-src (lazy loading)

```bash
# Chercher les images avec data-src
grep -r "data-src" pharmacie-campguezo-cotonou.messoins.bj/ | grep "pharmaciecourcelles" | head -5
```

---

## 🆘 Dépannage

### Problème: "permission denied" lors du renommage

```bash
# Solution: Vérifier les permissions
ls -la | grep pharmacie

# Si nécessaire, changer les permissions:
chmod -R 755 pharmaciecourcelles-demours-paris.mesoigner.fr
```

### Problème: Certaines URL ne sont pas remplacées

**Cause possible:** Encodage différent (Unicode, accents)

```bash
# Vérifier l'encodage
file pharmacie-campguezo-cotonou.messoins.bj/*.html

# Si UTF-8, c'est bon. Sinon, convertir:
for file in pharmacie-campguezo-cotonou.messoins.bj/*.html; do
  iconv -f ISO-8859-1 -t UTF-8 "$file" > "$file.tmp"
  mv "$file.tmp" "$file"
done
```

### Problème: Les CSS/images ne chargent pas

```bash
# Vérifier que les fichiers CSS existent
ls -la public/assets/css/

# Si vides ou manquants:
touch public/assets/css/scripts.3e902af8.css
touch public/assets/css/mesoigner.6063c722.css

# Vérifier les permissions
chmod 644 public/assets/css/*
```

### Problème: Erreurs 404 sur les assets

```bash
# Dans .htaccess (si Apache), vérifier:
# RewriteRule ^/assets/ - [L]

# Ou créer un symlink:
ln -s public/assets pharmacie-campguezo-cotonou.messoins.bj/assets
```

### Problème: Script Python non trouvé

```bash
# Vérifier que Python 3 est installé
python3 --version

# Si non installé:
# - Linux/Mac: brew install python3 ou apt install python3
# - Windows: https://www.python.org/downloads/

# Essayer avec le chemin complet:
/usr/bin/python3 scripts/migrate_complete.py
```

---

## 📊 Checklist finale

- [ ] Dossier `pharmaciecourcelles-demours-paris.mesoigner.fr` renommé
- [ ] Structure `public/assets/` créée
- [ ] CSS téléchargés ou fichiers vides créés
- [ ] Script Python/Bash exécuté
- [ ] Vérification: `grep -r data-theme="messoins"` > 1000
- [ ] Vérification: `grep -r pharmaciecourcelles` = 0
- [ ] Configuration Laravel mise à jour
- [ ] Serveur local testé et fonctionne
- [ ] Pas de 404 dans la console
- [ ] Logo, CSS, images s'affichent correctement

---

## 📞 Support

Si vous rencontrez des problèmes:

1. **Consultez le dossier de logs:**
   ```bash
   tail -f storage/logs/laravel.log
   ```

2. **Vérifiez la console du navigateur:**
   - F12 → Console → chercher les erreurs rouges

3. **Consultez les fichiers de documentation:**
   - `COMMANDES_SIMPLES.md` - Commands simplifiées
   - `GUIDE_LOCAL_COMPLET.md` - Guide détaillé
   - `GUIDE_VISUEL_ETAPE_PAR_ETAPE.md` - Guide avec screenshots

---

## ✅ Fait!

La migration est terminée! 🎉

**Prochaines étapes:**
1. Déployer vers production
2. Mettre à jour DNS/domaine
3. Configurer SSL/TLS
4. Tester en production

---

**Créé:** Oct 2025  
**Version:** 1.0  
**Script:** `scripts/migrate_complete.py`
