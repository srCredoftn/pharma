# 🎯 GUIDE VISUEL - ÉTAPE PAR ÉTAPE

**Avec images mentales et descriptions exactes**

---

## 📱 AVANT DE COMMENCER

### Prérequis
- ✅ Un terminal/CMD ouvert
- ✅ Tu sais où est ton dossier projet
- ✅ Internet fonctionne
- ✅ Tu as au moins 500MB libre sur ton disque

---

# 🚀 ÉTAPE 1: OUVRIR LE TERMINAL

## Sur Mac:
1. Appuie sur: **Cmd + Espace**
2. Tape: **Terminal**
3. Appuie sur: **Enter**

**Résultat:** Une fenêtre noire s'ouvre avec du texte blanc

```
Last login: Mon Jan 20 15:30:45 on ttys000
User@MacBook ~ %
```

## Sur Windows:
1. Appuie sur: **Win + R**
2. Tape: **cmd**
3. Appuie sur: **Enter**

**Résultat:** Une fenêtre noire s'ouvre avec du texte blanc

```
C:\Users\TonNom>
```

## Sur Linux:
1. Appuie sur: **Ctrl + Alt + T**

**Résultat:** Une fenêtre noire s'ouvre

```
user@computer:~$
```

---

# 📂 ÉTAPE 2: ALLER AU DOSSIER DU PROJET

### Qu'est-ce qu'on fait?
On dit au terminal: "Va dans le dossier du projet"

### Comment trouver le chemin?

**Option A: Méthode visuelle (sur Mac)**
1. Ouvre **Finder**
2. Cherche ton dossier projet (ex: "pharma", "pharmacie", etc.)
3. Clique droit sur le dossier
4. Maintiens **Option** et clique sur "Copy as Pathname"
5. Dans le terminal, tape: `cd ` puis colle (Cmd + V)

**Résultat:**
```bash
cd /Users/TonNom/Desktop/pharma
```

**Option B: Méthode visuelle (sur Windows)**
1. Ouvre **File Explorer**
2. Cherche ton dossier projet
3. Clique sur la barre d'adresse (en haut)
4. Copie le chemin (Ctrl + C)
5. Dans le CMD, tape: `cd ` puis colle (Ctrl + V)

**Résultat:**
```bash
cd C:\Users\TonNom\Desktop\pharma
```

**Option C: Simplement (si tu connais le chemin)**
```bash
cd ~/Desktop/pharma
```

### Vérifier que tu es au bon endroit:
```bash
pwd
```

**Résultat attendu:**
```
/Users/TonNom/Desktop/pharma
```

ou

```
C:\Users\TonNom\Desktop\pharma
```

✅ **Si tu vois le chemin de ton projet = C'est bon!**

---

# 📋 ÉTAPE 3: CRÉER LE DOSSIER PUBLIC/ASSETS/CSS

### Qu'est-ce qu'on fait?
On crée une structure de dossiers pour stocker les fichiers CSS

### Commande:
```bash
mkdir -p public/assets/css
```

### Que se passe-t-il?
- Le terminal crée un dossier `public`
- Dedans, crée un dossier `assets`
- Dedans, crée un dossier `css`

### Structure créée:
```
ton-projet/
├── public/              ← Créé
│   └── assets/          ← Créé
│       └── css/         ← Créé
└── ... (autres dossiers)
```

### Vérifier que c'est créé:
```bash
ls -la public/assets/css/
```

**Résultat attendu:**
```
total 0
drwxr-xr-x  2 user staff  64 Jan 20 15:35 .
drwxr-xr-x  3 user staff  96 Jan 20 15:35 ..
```

✅ **Si tu vois ça (dossier vide) = C'est bon!**

---

# ⬇️ ÉTAPE 4: TÉLÉCHARGER LE PREMIER CSS

### Qu'est-ce qu'on fait?
On télécharge un fichier depuis le serveur mesoigner.fr (Internet)

### Commande:
```bash
curl -o public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css"
```

### À quoi ça ressemble?
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 22053  100 22053    0     0  45678      0 --:--:-- --:--:-- --:--:-- 45678
```

(C'est une barre de progression, c'est normal!)

### Attendre:
🔄 Le téléchargement prend environ 2-5 secondes

### Résultat attendu:
Aucune erreur n'apparaît, juste la barre de progression

✅ **Si pas d'erreur rouge = C'est bon!**

---

# ⬇️ ÉTAPE 5: TÉLÉCHARGER LE DEUXIÈME CSS

### Qu'est-ce qu'on fait?
Télécharger le 2e fichier CSS (le plus gros)

### Commande:
```bash
curl -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"
```

### À quoi ça ressemble?
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Dload  Upload   Total   Spent    Left  Speed
100  271k  100  271k    0     0  92456      0 --:--:-- --:--:-- --:--:-- 92456
```

### Attendre:
🔄 Le téléchargement prend environ 3-8 secondes

### Résultat attendu:
Aucune erreur, juste la barre de progression

✅ **Si pas d'erreur rouge = C'est bon!**

---

# ✅ ÉTAPE 6: VÉRIFIER QUE LES FICHIERS SONT LÀ

### Qu'est-ce qu'on fait?
Vérifier que les fichiers ont bien été téléchargés

### Commande:
```bash
ls -lh public/assets/css/
```

### Résultat attendu:
```
total 296
-rw-r--r--  1 user staff   22K Jan 20 15:37 scripts.3e902af8.css
-rw-r--r--  1 user staff  271K Jan 20 15:38 mesoigner.6063c722.css
```

### À vérifier:
- ✅ `scripts.3e902af8.css` existe (22K)
- ✅ `mesoigner.6063c722.css` existe (271K)
- ✅ Les tailles correspondent

✅ **Si tu vois ces 2 fichiers = Les téléchargements ont marché!**

---

# 🔧 ÉTAPE 7: RENDRE LE SCRIPT EXÉCUTABLE

### Qu'est-ce qu'on fait?
Donner la permission au script `quick-migrate.sh` de s'exécuter

### Commande:
```bash
chmod +x quick-migrate.sh
```

### Que se passe-t-il?
Le terminal change les permissions du fichier `quick-migrate.sh`

### Vérifier:
```bash
ls -la quick-migrate.sh
```

### Résultat attendu:
```
-rwxr-xr-x  1 user staff  1.2K Jan 20 15:30 quick-migrate.sh
```

(Remarque le `x` dans `rwxr-xr-x` = exécutable)

✅ **Si tu vois le `x` = C'est bon!**

---

# 🚀 ÉTAPE 8: EXÉCUTER LA MIGRATION

### Qu'est-ce qu'on fait?
Lancer le script qui va modifier tous les fichiers HTML

### Commande:
```bash
./quick-migrate.sh
```

### À quoi ça ressemble?
```
🔄 Démarrage de la migration CDN rapide...
   mesoigner → messoins
   pharmaciecourcelles-demours-paris.mesoigner.fr → pharmacie-campguezo-cotonou.messoins.bj

📁 Création de la structure des assets...
⬇️  Téléchargement des CSS...
🔄 Remplacement des URLs CDN...
  ✅ 500 fichiers traités...
  ✅ 1000 fichiers traités...
  ✅ 1500 fichiers traités...
  ✅ 2000 fichiers traités...
  ...
  ✅ 8000 fichiers traités...

✅ Migration terminée!
   8000 fichiers HTML mises à jour
```

### Durée:
⏱️ 30-90 secondes (selon la vitesse de ton ordinateur)

### À ne pas faire:
❌ N'appuie pas sur Ctrl+C
❌ Ne ferme pas le terminal
❌ N'éteins pas l'ordinateur

### Attendre le message:
```
✅ Migration terminée!
```

✅ **Quand tu vois ce message = Migration réussie!**

---

# 🔍 ÉTAPE 9: VÉRIFIER QUE LA MIGRATION A MARCHÉ

### Vérification 1: Nouveau branding appliqué?

**Commande:**
```bash
grep -r 'data-theme="messoins"' pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l
```

**Résultat attendu:**
```
1000
```

(Un grand nombre, pas zéro!)

✅ **Si tu vois un grand nombre = Branding appliqué!**

---

### Vérification 2: Anciennes URLs supprimées?

**Commande:**
```bash
grep -r "https://cdn.mesoigner.fr" pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l
```

**Résultat attendu:**
```
0
```

(Zéro ancienne URL!)

✅ **Si c'est 0 = Remplacements réussis!**

---

### Vérification 3: Nouvelles URLs locales?

**Commande:**
```bash
grep -r "/assets/css/" pharmaciecourcelles-demours-paris.mesoigner.fr/ | head -3
```

**Résultat attendu:**
```
pharmaciecourcelles-demours-paris.mesoigner.fr/index.html:        <link rel="stylesheet" type="text/css" href="/assets/css/scripts.3e902af8.css">
pharmaciecourcilles-demours-paris.mesoigner.fr/index.html:    <link rel="stylesheet" type="text/css" href="/assets/css/mesoigner.6063c722.css">
...
```

(Des URLs locales `/assets/css/`!)

✅ **Si tu vois `/assets/css/` = URLs mises à jour!**

---

# 🧪 ÉTAPE 10: TESTER LE SITE

### Qu'est-ce qu'on fait?
Lancer le serveur Laravel pour vérifier que le site fonctionne

### Commande:
```bash
php artisan serve
```

### À quoi ça ressemble?
```
 INFO  Server running on [http://127.0.0.1:8000]

  Press Ctrl+C to quit
```

### Ouvrir dans le navigateur:
1. Ouvre un navigateur (Chrome, Firefox, Safari, Edge, etc.)
2. Va à: **http://localhost:8000**
3. La page doit se charger

### À vérifier:
- ✅ La page s'affiche?
- ✅ Le header a un fond blanc/gris?
- ✅ Le logo s'affiche (petite image en haut à gauche)?
- ✅ Les couleurs sont présentes (pas juste du texte noir)?
- ✅ Aucune erreur en bas du terminal?

### Si ça ne marche pas:
Ouvre le **DevTools** (F12 → Network):
- Cherche les erreurs rouges
- Clique sur les erreurs pour voir pourquoi

### Arrêter le serveur:
```
Ctrl + C
```

(Appuie en même temps sur Ctrl et C)

✅ **Quand tout fonctionne = Migration complète!**

---

# 📊 RÉSUMÉ - Toutes les étapes

| # | Étape | Commande | Temps |
|---|-------|----------|-------|
| 1 | Ouvrir terminal | Cmd+Espace (Mac) ou Win+R (Windows) | 10 sec |
| 2 | Aller au projet | `cd ~/Desktop/pharma` | 5 sec |
| 3 | Créer dossiers | `mkdir -p public/assets/css` | 1 sec |
| 4 | Télécharger CSS 1 | `curl -o public/assets/css/scripts...` | 5 sec |
| 5 | Télécharger CSS 2 | `curl -o public/assets/css/mesoigner...` | 5 sec |
| 6 | Vérifier CSS | `ls -lh public/assets/css/` | 1 sec |
| 7 | Rendre exécutable | `chmod +x quick-migrate.sh` | 1 sec |
| 8 | Migration | `./quick-migrate.sh` | 60 sec |
| 9 | Vérifications | `grep -r ...` | 30 sec |
| 10 | Tester site | `php artisan serve` | 2 min |

**Total: ~5-10 minutes** ⏱️

---

# ✅ CHECKLIST - À cocher au fur et à mesure

- [ ] Terminal ouvert
- [ ] Je suis dans le bon dossier (`pwd` affiche le bon chemin)
- [ ] Dossiers créés (`ls -la public/` affiche `assets`)
- [ ] CSS #1 téléchargé (pas d'erreur)
- [ ] CSS #2 téléchargé (pas d'erreur)
- [ ] Fichiers vérifiés (`ls -lh` affiche 2 fichiers)
- [ ] Script rendu exécutable (`ls -la quick-migrate.sh` affiche `x`)
- [ ] Migration exécutée (message "Migration terminée!")
- [ ] Vérification 1 OK (grand nombre)
- [ ] Vérification 2 OK (0 ou très petit)
- [ ] Vérification 3 OK (/assets/css/ présents)
- [ ] Site testé (localhost:8000 fonctionne)
- [ ] 🎉 TOUT EST FINI!

---

# 🆘 TROUBLESHOOTING RAPIDE

**Erreur: "command not found: curl"**
→ Installer curl ou utiliser la méthode de téléchargement manuel

**Erreur: "quick-migrate.sh: Permission denied"**
→ Exécuter: `chmod +x quick-migrate.sh`

**Le script ne trouve pas les fichiers**
→ Vérifier que le dossier `pharmaciecourcilles-demours-paris.mesoigner.fr` existe

**Les CSS ne s'appliquent pas au test**
→ Faire: `php artisan cache:clear && php artisan view:clear`

**Erreurs 404 en consultant DevTools**
→ Vérifier que les fichiers CSS existent: `ls -lh public/assets/css/`

---

# 🎉 VOILÀ! C'EST FINI!

Tu as réussi à:
✅ Télécharger les CSS du CDN
✅ Exécuter la migration sur 8000 fichiers
✅ Vérifier que tout fonctionne
✅ Tester le site localement

**Migration complétée avec succès! 🚀**
