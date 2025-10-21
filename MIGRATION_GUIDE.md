# Guide de Migration CDN: mesoigner → messoins

## 🎯 Objectif
Convertir le projet d'une dépendance CDN externe (`mesoigner.fr`) à une structure locale complète avec le nouveau branding `messoins.bj`.

## 📋 Changements à effectuer

### 1. **Domaine**
- **De:** `pharmaciecourcelles-demours-paris.mesoigner.fr`
- **Vers:** `pharmacie-campguezo-cotonou.messoins.bj`

### 2. **Branding**
- **De:** `mesoigner`
- **Vers:** `messoins`

### 3. **CDN URLs**
- **De:** `https://cdn.mesoigner.fr/...`
- **Vers:** `/assets/...` (local)

---

## 🚀 Étapes d'exécution

### Étape 1: Rendre le script exécutable

```bash
chmod +x migrate-cdn.sh
```

### Étape 2: Exécuter la migration automatique

```bash
./migrate-cdn.sh
```

Ce script va:
- ✅ Créer la structure locale (`public/assets/`)
- ✅ Télécharger les CSS depuis le CDN mesoigner.fr
- ✅ Télécharger les images principales
- ✅ Faire le find/replace massif sur tous les fichiers HTML

### Étape 3: Télécharger les SVG des icons (optionnel)

Les SVG des icons sont directement référencées depuis les chemins relatifs (`fonts/icons.svg`). Elles doivent rester comme elles sont car elles sont dans le dossier `fonts/` du site.

### Étape 4: Renommer le dossier principal (optionnel)

```bash
mv pharmaciecourcelles-demours-paris.mesoigner.fr/ pharmacie-campguezo-cotonou.messoins.bj/
```

---

## 📂 Structure finale

```
project/
├── public/
│   └── assets/
│       ├── css/
│       │   ├── scripts.3e902af8.css
│       │   └── mesoigner.6063c722.css
│       └── uploads/
│           ├── header-wrapper.png
│           ├── que-prendre.png
│           └── logo-messoins.svg
├── pharmacie-campguezo-cotonou.messoins.bj/
│   ├── index.html (avec URLs mises à jour)
│   ├── fonts/
│   │   ├── icons.svg
│   │   └── mesoigner.svg
│   ├── media/
│   └── ... (autres fichiers HTML)
└── migrate-cdn.sh
```

---

## ⚠️ Points importants

1. **Google Fonts:** Reste en CDN externe (`https://fonts.googleapis.com/...`) car c'est une dépendance standard
2. **SVG des icons:** Restent en chemins relatifs (`fonts/icons.svg`)
3. **Images produits:** Restent en chemins externes dans les data attributes
4. **CSS compilés:** Le CSS compilé peut contenir d'autres URLs CDN - les vérifier manuellement

---

## ✅ Vérification

Après la migration, vérifier:

```bash
# Vérifier que les CSS sont en place
ls -la public/assets/css/

# Vérifier que les images sont téléchargées
ls -la public/assets/uploads/

# Chercher les URLs mesoigner restantes
grep -r "mesoigner" pharmacie-campguezo-cotonou.messoins.bj/ | head -20
```

---

## 🔧 Dépannage

### Les styles ne s'appliquent pas
→ Vérifier que les chemins `/assets/css/` sont corrects
→ Vérifier que les fichiers CSS existent dans `public/assets/css/`

### Les images manquent
→ Exécuter le script à nouveau avec les commandes curl correctes
→ Télécharger manuellement depuis: `https://cdn.mesoigner.fr/src/img/...`

### Les données-theme ne changeaient pas
→ Le script remplace `data-theme="mesoigner"` par `data-theme="messoins"`
→ Mettre à jour les fichiers CSS qui contendraient des références au thème

---

## 📝 Prochaines étapes

1. Exécuter le script `migrate-cdn.sh`
2. Vérifier les fichiers CSS et images
3. Tester le site localement
4. Renommer le dossier principal si nécessaire
5. Commiter les changements

---

**Besoin d'aide?** Exécute le script et envoie les erreurs si tu en rencontres!
