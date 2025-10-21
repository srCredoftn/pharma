# 🚀 Guide Complet: Migration CDN mesoigner → messoins

## Situation actuelle
✅ Scripts de migration créés:
- `migrate-cdn.sh` (Bash script)
- `scripts/migrate_cdn.py` (Python script - RECOMMANDÉ)
- `MIGRATION_GUIDE.md` (Guide détaillé)

✅ Assets locaux:
- `/public/assets/css/` - Créé
- `/public/assets/uploads/` - Créé avec logo-messoins.svg

---

## 📋 Plan d'exécution (4 étapes)

### **ÉTAPE 1: Télécharger les fichiers CSS/assets manquants**

Exécute cette commande dans le terminal à la racine du projet:

```bash
# Télécharger les CSS
curl -o public/assets/css/scripts.3e902af8.css \
  https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css

curl -o public/assets/css/mesoigner.6063c722.css \
  https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css

# Télécharger les images
curl -o public/assets/uploads/header-wrapper.png \
  https://cdn.mesoigner.fr/src/img/layout/header-wrapper.png

curl -o public/assets/uploads/que-prendre.png \
  https://cdn.mesoigner.fr/src/img/widgets/que-prendre/que-prendre.png
```

**Vérification:**
```bash
ls -lh public/assets/css/
ls -lh public/assets/uploads/
```

### **ÉTAPE 2: Exécuter le script Python de migration (RECOMMANDÉ)**

```bash
# Rendre le script exécutable
chmod +x scripts/migrate_cdn.py

# Exécuter la migration
python3 scripts/migrate_cdn.py
```

**Ou utiliser le script Bash:**
```bash
chmod +x migrate-cdn.sh
./migrate-cdn.sh
```

### **ÉTAPE 3: Vérifier que les remplacements ont fonctionné**

```bash
# Chercher les restes de "mesoigner" (devrait être très peu)
grep -r "mesoigner" pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l

# Chercher les restes de l'ancien domaine
grep -r "pharmaciecourcelles-demours-paris" pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l

# Vérifier que les nouveaux chemins existent
grep -r "/assets/css/" pharmaciecourcelles-demours-paris.mesoigner.fr/index.html

# Vérifier que le data-theme a changé
grep "data-theme=" pharmaciecourcelles-demours-paris.mesoigner.fr/index.html
```

### **ÉTAPE 4: (Optionnel) Renommer le dossier principal**

```bash
# Renommer le dossier de base
mv pharmaciecourcelles-demours-paris.mesoigner.fr/ pharmacie-campguezo-cotonou.messoins.bj/
```

---

## 🔄 Remplacements effectués

| Ancien | Nouveau |
|--------|---------|
| `https://cdn.mesoigner.fr/...` | `/assets/...` |
| `logo-mesoigner.svg` | `logo-messoins.svg` |
| `data-theme="mesoigner"` | `data-theme="messoins"` |
| `pharmaciecourcelles-demours-paris.mesoigner.fr` | `pharmacie-campguezo-cotonou.messoins.bj` |
| `mesoigner.svg` | `messoins.svg` |
| `cdn.mesoigner.fr` | `cdn.messoins.bj` |

---

## ✅ Checklist finale

- [ ] **Étape 1**: Télécharger les CSS et images  (`curl` commands)
- [ ] **Étape 2**: Exécuter `python3 scripts/migrate_cdn.py`
- [ ] **Étape 3**: Vérifier les remplacements avec `grep`
- [ ] **Étape 4**: Renommer le dossier (optionnel)
- [ ] **Vérification**: Accéder au site et vérifier que les styles s'appliquent
- [ ] **Git**: Commiter les changements

---

## 🧪 Test rapide

Après la migration, tu peux vérifier rapidement:

```bash
# Compter le nombre de fichiers modifiés
find pharmaciecourcelles-demours-paris.mesoigner.fr -name "*.html" -type f | wc -l

# Afficher les premières lignes du fichier index.html
head -50 pharmaciecourcelles-demours-paris.mesoigner.fr/index.html | grep -E "(assets|data-theme|logo-messoins)"
```

---

## ⚠️ Dépannage

### Les CSS ne s'appliquent pas?
1. Vérifier que les fichiers CSS existent: `ls -la public/assets/css/`
2. Vérifier les chemins dans le HTML: `grep -o 'href="[^"]*css[^"]*"' index.html`
3. Vérifier les erreurs 404 dans la console du navigateur

### Les chemins des images sont faux?
1. Certaines images peuvent être sur d'autres URLs (data attributes)
2. Utiliser: `grep -r "data-src=" pharmaciecourcelles-demours-paris.mesoigner.fr/ | head -5`
3. Faire des remplacements supplémentaires si nécessaire

### Le script Python ne s'exécute pas?
1. Vérifier Python: `python3 --version`
2. Créer un symlink: `python3 scripts/migrate_cdn.py`
3. Ou utiliser le script Bash: `./migrate-cdn.sh`

---

## 📊 Résultats attendus

Après l'exécution:
- ✅ ~8,000 fichiers HTML traités
- ✅ ~50,000+ remplacements effectués
- ✅ Structure `/public/assets/` peuplée
- ✅ Tous les liens CDN remplacés par des chemins locaux
- ✅ Branding mesoigner → messoins appliqué partout
- ✅ Domaine pharmaciecourcelles-demours-paris.mesoigner.fr → pharmacie-campguezo-cotonou.messoins.bj

---

## 📝 Prochaines étapes après la migration

1. **Tester le site localement**
   ```bash
   php artisan serve
   ```

2. **Vérifier les assets**
   - Accéder à: `http://localhost:8000/assets/css/mesoigner.6063c722.css`
   - Doit retourner le CSS, pas une 404

3. **Renommer le dossier du site** (si nécessaire)
   ```bash
   mv pharmaciecourcelles-demours-paris.mesoigner.fr/ pharmacie-campguezo-cotonou.messoins.bj/
   ```

4. **Commiter les changements**
   ```bash
   git add -A
   git commit -m "Migration CDN: mesoigner → messoins, domaine personnalisé"
   git push
   ```

5. **Mettre à jour Laravel config** (si nécessaire)
   - Vérifier `config/app.php`
   - Vérifier `.env` pour les variables d'app

---

## 🎯 Résumé

Tu as maintenant:
1. ✅ Structure locale `/public/assets/`
2. ✅ Logo branded `logo-messoins.svg`
3. ✅ Scripts de migration Python et Bash
4. ✅ Guide complet d'exécution

**Prochaine action:** Exécute `python3 scripts/migrate_cdn.py` et envoie les résultats!

---

**Questions ou problèmes?** Consul te ce guide ou exécute les commandes de vérification ci-dessus.
