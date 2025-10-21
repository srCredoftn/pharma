# ✅ APRÈS LA MIGRATION - Guide Post-Exécution

**Ce guide explique ce qu'il faut faire APRÈS avoir exécuté la migration**

---

## 🎯 Immédiatement après la migration

### 1️⃣ Vérifications rapides (2 minutes)

```bash
# Vérification 1: Le dossier a été renommé?
test -d pharmacie-campguezo-cotonou.messoins.bj && echo "✅ Dossier renommé" || echo "❌ Dossier manquant!"

# Vérification 2: Nouveau branding appliqué?
grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
# Attendu: 1000+

# Vérification 3: Ancien domaine supprimé?
grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
# Attendu: 0

# Vérification 4: Ancien CDN supprimé?
grep -r "https://cdn\.mesoigner\.fr" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
# Attendu: 0
```

### Si toutes les vérifications réussissent:
```bash
echo "✅ Migration réussie! Passer à l'étape suivante"
```

### Si une vérification échoue:
```bash
# Voir la section "Problèmes" ci-dessous
```

---

## 🧪 Test local complet (5 minutes)

### Démarrer le serveur
```bash
php artisan serve
```

Vous devez voir:
```
   INFO  Server running on [http://127.0.0.1:8000].
```

### Tester dans le navigateur

**Ouvrir:**
```
http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/index.html
```

### Points de vérification visuels

- [ ] **Page charge** - Pas d'erreur 500 ou blanc
- [ ] **Logo visible** - En haut à gauche (messoins)
- [ ] **CSS chargé** - Page bien stylisée, pas d'alarme visuelle
- [ ] **Images s'affichent** - Pas de petits carrés cassés
- [ ] **Menu répond** - Cliquer sur "Médicaments" fonctionne
- [ ] **Formulaire de recherche** - Peut cliquer dans la barre
- [ ] **Footer visible** - En bas de page

### Tester la console (F12)

1. Appuyer sur **F12**
2. Aller à l'onglet **Console**
3. Chercher les **erreurs rouges**
4. Chercher les **404** (ressources manquantes)

**Résultat attendu:**
- Aucune erreur rouge
- Aucun 404 pour les assets
- Peut y avoir des avertissements (warn) - c'est OK

### Tester les pages principales

```bash
# Via le terminal, vérifier quelques pages
curl -s http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/index.html | grep -q "data-theme=\"messoins\"" && echo "✅ index.html OK"
curl -s http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/connexion.html | grep -q "data-theme=\"messoins\"" && echo "✅ connexion.html OK"
curl -s http://localhost:8000/pharmacie-campguezo-cotonou.messoins.bj/inscription.html | grep -q "data-theme=\"messoins\"" && echo "✅ inscription.html OK"
```

### Arrêter le serveur
```
Ctrl + C
```

---

## ⚙️ Configuration Laravel

### Si le site n'affiche pas correctement:

#### Vérifier config/app.php
```php
'url' => env('APP_URL', 'https://pharmacie-campguezo-cotonou.messoins.bj'),
'asset_url' => env('ASSET_URL', 'https://pharmacie-campguezo-cotonou.messoins.bj'),
```

#### Vérifier .env
```env
APP_URL=https://pharmacie-campguezo-cotonou.messoins.bj
ASSET_URL=https://pharmacie-campguezo-cotonou.messoins.bj
```

#### Mettre en cache la config
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

---

## 📁 Vérifier la structure des fichiers

### Vérifier que les fichiers clés existent
```bash
# CSS doit exister
test -f public/assets/css/scripts.3e902af8.css && echo "✅ scripts.css" || echo "❌ scripts.css manquant"
test -f public/assets/css/mesoigner.6063c722.css && echo "✅ mesoigner.css" || echo "❌ mesoigner.css manquant"

# Dossier uploads doit exister
test -d public/assets/uploads && echo "✅ uploads/" || echo "❌ uploads/ manquant"

# HTML files doit exister
test -d pharmacie-campguezo-cotonou.messoins.bj && echo "✅ Dossier HTML" || echo "❌ Dossier manquant"
```

---

## 🔍 Recherches et vérifications avancées

### Chercher les URL qui pourraient encore avoir l'ancien domaine
```bash
# Chercher dans les fichiers JSON
grep -r "pharmaciecourcelles" pharmacie-campguezo-cotonou.messoins.bj/*.json 2>/dev/null | head -5

# Chercher dans les fichiers PHP
grep -r "pharmaciecourcelles" pharmacie-campguezo-cotonou.messoins.bj/*.php 2>/dev/null | head -5

# Chercher des patterns de CDN cassés
grep -r "cdn\.mesoigner" pharmacie-campguezo-cotonou.messoins.bj/ | head -5

# Chercher les chemins relatifs problématiques
grep -r "\.\./cdn\." pharmacie-campguezo-cotonou.messoins.bj/ | head -5
```

### Chercher les images lazy-loading qui ne seraient pas à jour
```bash
# Chercher data-src avec ancien domaine
grep -r 'data-src.*pharmaciecourcelles' pharmacie-campguezo-cotonou.messoins.bj/ | head -3

# Chercher data-src avec ancien CDN
grep -r 'data-src.*cdn\.mesoigner' pharmacie-campguezo-cotonou.messoins.bj/ | head -3
```

---

## 🐛 Problèmes courants et solutions

### Problème 1: Les CSS ne chargent pas

**Symptômes:** Aucun style, page blanche ou mal stylisée

**Solution:**
```bash
# Vérifier que les fichiers CSS existent
ls -lh public/assets/css/

# S'ils sont vides, c'est normal. Vérifier le chemin dans HTML:
grep -n "href.*assets/css" pharmacie-campguezo-cotonou.messoins.bj/index.html | head -3

# Le chemin doit être /assets/css/... (avec slash initial)
# Si c'est ../assets/css/... c'est un problème
```

### Problème 2: Les images ne s'affichent pas

**Symptômes:** Petits carrés cassés ou images manquantes

**Solution:**
```bash
# Vérifier les URLs d'images
grep -r "<img" pharmacie-campguezo-cotonou.messoins.bj/index.html | grep -o 'src="[^"]*"' | head -5

# Elles doivent être soit:
# - /assets/uploads/... (local)
# - https://pharmacie-campguezo-cotonou.messoins.bj/media/... (CDN)
# - /fonts/... (pour les icones SVG)
```

### Problème 3: Le logo n'affiche pas

**Symptômes:** Pas d'image en haut à gauche

**Solution:**
```bash
# Vérifier que le logo est correct
grep -r "logo-messoins" pharmacie-campguezo-cotonou.messoins.bj/index.html | head -3

# Vérifier le chemin
# Doit être: /assets/uploads/logo-messoins.svg
# OU: https://pharmacie-campguezo-cotonou.messoins.bj/media/...

# Créer un logo vide si manquant (placeholder):
echo '<svg></svg>' > public/assets/uploads/logo-messoins.svg
```

### Problème 4: data-theme n'est pas bon

**Symptômes:** Les couleurs ne sont pas correctes

**Solution:**
```bash
# Vérifier que tous les headers ont data-theme="messoins"
grep -c 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/index.html
# Attendu: au moins 1

# S'il y en a 0, faire un remplacement manuel
sed -i 's/data-theme="mesoigner"/data-theme="messoins"/g' \
  pharmacie-campguezo-cotonou.messoins.bj/index.html
```

### Problème 5: Les URLs restent mal

**Symptômes:** Certains liens pointent vers l'ancien domaine

**Solution:**
```bash
# Trouver les mauvaises URLs
grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ | head -5

# Remplacer manuellement
sed -i 's/pharmaciecourcelles-demours-paris\.mesoigner\.fr/pharmacie-campguezo-cotonou.messoins.bj/g' \
  pharmacie-campguezo-cotonou.messoins.bj/fichier.html
```

---

## ✅ Checklist post-migration

### Vérifications
- [ ] `grep -r 'data-theme="messoins"'` retourne 1000+
- [ ] `grep -r 'pharmaciecourcelles-demours-paris'` retourne 0
- [ ] `grep -r 'https://cdn\.mesoigner\.fr'` retourne 0
- [ ] `public/assets/css/` contient les 2 fichiers CSS
- [ ] `php artisan serve` marche sans erreur
- [ ] Page s'affiche dans le navigateur
- [ ] Logo visible
- [ ] Aucune erreur 404 en console (F12)
- [ ] Aucune erreur rouge en console
- [ ] Menus fonctionnent

### Configuration
- [ ] `config/app.php` mis à jour (si nécessaire)
- [ ] `.env` mis à jour (si nécessaire)
- [ ] `php artisan config:cache` exécuté

### Tests
- [ ] Accueil charge
- [ ] Connexion charge
- [ ] Inscription charge
- [ ] Recherche fonctionne
- [ ] Menu fonctionne
- [ ] Footer s'affiche

---

## 🚀 Prochaines étapes (Avant production)

### 1. Mettre en cache
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### 2. Vérifier les assets compilés
```bash
# Si vous utilisez Laravel Mix:
npm run production
# Ou Vite:
npm run build
```

### 3. Vérifier la base de données (si applicable)
```bash
# Si vous devez mettre à jour les URLs en base:
php artisan migrate
# Ou faire un search/replace sur les tables
```

### 4. Tester en staging
```bash
# Déployer sur un serveur de test
# Vérifier que tout fonctionne
# Vérifier les logs
```

### 5. Mettre à jour le DNS (avant de passer en production)
```bash
# Faire pointer le domaine vers le serveur
# Attendre la propagation DNS (jusqu'à 24h)
# Vérifier avec: nslookup pharmacie-campguezo-cotonou.messoins.bj
```

### 6. Configurer SSL/TLS
```bash
# Générer certificat SSL (Let's Encrypt recommandé)
# Configurer nginx/Apache pour HTTPS
# Faire redirection HTTP → HTTPS
```

### 7. Deployment final
```bash
# Déployer en production
# Vérifier les logs
# Tester dans navigateur
# Monitorer les erreurs
```

---

## 📊 Vérification d'intégrité

### Créer un rapport complet
```bash
#!/bin/bash

echo "========================================="
echo "RAPPORT DE MIGRATION"
echo "========================================="
echo ""

# Fichiers traités
html_count=$(find pharmacie-campguezo-cotonou.messoins.bj -name "*.html" -type f | wc -l)
echo "✅ Fichiers HTML: $html_count"

# Nouveau branding
messoins=$(grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
echo "✅ Référence au nouveau domaine: $messoins"

# Ancien branding supprimé
old=$(grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
echo "✅ Ancien domaine restant: $old"

# Ancien CDN supprimé
cdn=$(grep -r "https://cdn\.mesoigner\.fr" pharmacie-campguezo-cotonou.messoins.bj/ 2>/dev/null | wc -l)
echo "✅ Ancien CDN restant: $cdn"

# CSS existent
css1=$(test -f public/assets/css/scripts.3e902af8.css && echo "OUI" || echo "NON")
css2=$(test -f public/assets/css/mesoigner.6063c722.css && echo "OUI" || echo "NON")
echo "✅ CSS scripts: $css1"
echo "✅ CSS mesoigner: $css2"

echo ""
echo "========================================="
echo "RÉSUMÉ"
echo "========================================="
if [ "$old" -eq 0 ] && [ "$cdn" -eq 0 ] && [ "$messoins" -gt 1000 ]; then
  echo "✅ MIGRATION RÉUSSIE!"
else
  echo "⚠️  Vérifier les détails ci-dessus"
fi
echo "========================================="
```

---

## 🎉 Vous avez terminé!

Si vous êtes ici et que tout fonctionne:

1. ✅ Migration complète
2. ✅ Tests réussis
3. ✅ Configuration vérifiée
4. ✅ Prêt pour production

**Prochaine étape:** Deployment vers production!

---

## 📞 Support

### Si vous avez encore des problèmes:

1. **Vérifications rapides:**
   - `grep -r 'data-theme="messoins"'` doit retourner 1000+
   - `grep -r 'pharmaciecourcelles'` doit retourner 0
   - `php artisan serve` doit démarrer sans erreur

2. **Vérifications navigateur (F12):**
   - Console: Aucune erreur rouge
   - Network: Aucun 404
   - Sources: Les fichiers CSS chargent

3. **Documentation:**
   - Voir `MIGRATION_COMPLETE_GUIDE.md` section "Dépannage"
   - Voir les logs Laravel: `storage/logs/laravel.log`

---

**Félicitations! Vous avez réussi la migration! 🎉**
