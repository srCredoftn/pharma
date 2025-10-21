# 📖 GUIDE COMPLET - Faire la migration en LOCAL

**Durée totale:** ~5-10 minutes  
**Difficulté:** Simple (copier/coller)  
**Prérequis:** Terminal/CMD + Internet

---

## 🎯 Ce que tu vas faire

1. **Télécharger les fichiers CSS du CDN mesoigner** (2-3 min)
2. **Exécuter le script de migration** (2-3 min)
3. **Vérifier que ça marche** (1-2 min)

---

# 📋 ÉTAPE 1: Télécharger les CSS

## Qu'est-ce qu'on télécharge?
- **2 fichiers CSS** depuis le serveur mesoigner.fr
- Ces fichiers contiennent tous les styles du site

## Comment faire?

### Étape 1a: Ouvrir le terminal
- **Mac/Linux:** Appuie sur `Cmd + Espace`, tape "Terminal", puis Enter
- **Windows:** Appuie sur `Win + R`, tape "cmd", puis Enter

### Étape 1b: Aller au dossier du projet
```bash
cd chemin/vers/ton/projet
```

**Exemple:**
```bash
# Sur Mac/Linux:
cd ~/Desktop/pharma

# Sur Windows:
cd C:\Users\TonNom\Desktop\pharma
```

### Étape 1c: Copie ces commandes (UNE PAR UNE)

**Commande 1:** Créer le dossier
```bash
mkdir -p public/assets/css
```
*(Crée un dossier pour stocker les CSS)*

**Commande 2:** Télécharger le 1er CSS
```bash
curl -o public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css"
```
*(Télécharge le fichier scripts... depuis Internet)*

**Attends que ce message apparaisse:**
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  ...
```

**Commande 3:** Télécharger le 2e CSS
```bash
curl -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"
```
*(Télécharge le fichier mesoigner... depuis Internet)*

**Attends que ce message apparaisse encore une fois**

### Étape 1d: Vérifier que les fichiers sont là
```bash
ls -lh public/assets/css/
```

**Tu dois voir:**
```
mesoigner.6063c722.css    (271K)
scripts.3e902af8.css       (22K)
```

✅ **Si tu vois ces fichiers = C'est bon!**

---

# 📋 ÉTAPE 2: Exécuter le script de migration

## Qu'est-ce qu'on fait?
On exécute un script qui va:
- Lire tous les fichiers HTML (~8000 fichiers)
- Changer "mesoigner" en "messoins"
- Changer les URLs CDN en URLs locales

## Comment faire?

### Étape 2a: Rendre le script exécutable
```bash
chmod +x quick-migrate.sh
```
*(Donne la permission d'exécuter le script)*

### Étape 2b: Exécuter le script
```bash
./quick-migrate.sh
```

### Étape 2c: Attendre
Tu verras des messages comme:
```
🔄 Démarrage de la migration CDN rapide...
   mesoigner → messoins

📝 Traitement des fichiers HTML...
  ✅ 500 fichiers traités...
  ✅ 1000 fichiers traités...
  ✅ 1500 fichiers traités...
...
✅ Migration terminée!
   ~8000 fichiers HTML modifiés
```

**C'est normal, ça prend 30-60 secondes**

---

# 📋 ÉTAPE 3: Vérifier que ça marche

## Vérification 1: Les fichiers CSS sont là?
```bash
ls -lh public/assets/css/
```

**Résultat attendu:**
```
mesoigner.6063c722.css    271K
scripts.3e902af8.css       22K
```

✅ **Si tu vois ça = C'est bon!**

---

## Vérification 2: Les remplacements ont marché?
```bash
grep -r 'data-theme="messoins"' pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l
```

**Résultat attendu:**
```
1000+
```

✅ **Si tu vois un grand nombre = C'est bon!**

---

## Vérification 3: Il reste des anciennes URLs?
```bash
grep -r "https://cdn.mesoigner.fr" pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l
```

**Résultat attendu:**
```
0
```

✅ **Si c'est 0 ou très petit = C'est bon!**

---

# 📋 ÉTAPE 4: Tester le site

## Comment tester?

### Étape 4a: Lancer le serveur
```bash
php artisan serve
```

Tu verras:
```
Laravel development server started: http://127.0.0.1:8000
```

### Étape 4b: Ouvrir dans le navigateur
Ouvre: **http://localhost:8000**

### Étape 4c: Vérifier
- ✅ La page se charge?
- ✅ Le header s'affiche correctement?
- ✅ Les couleurs sont là?
- ✅ Le logo s'affiche?

### Étape 4d: Arrêter le serveur
```
Ctrl + C
```

---

# 🔍 Si quelque chose ne marche pas

## Problème 1: "curl: command not found"
**Solution:**
- Installer curl via: https://curl.se/download.html
- Ou télécharger les fichiers manuellement via le navigateur

## Problème 2: "Permission denied" sur quick-migrate.sh
**Solution:**
```bash
chmod +x quick-migrate.sh
./quick-migrate.sh
```

## Problème 3: Les fichiers CSS n'existent pas après téléchargement
**Solution:**
```bash
# Vérifier que le dossier existe
mkdir -p public/assets/css

# Retenter le téléchargement
curl -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"
```

## Problème 4: Le script ne trouve pas de fichiers
**Solution:**
Vérifier que le dossier `pharmaciecourcelles-demours-paris.mesoigner.fr` existe:
```bash
ls -la | grep pharmacie
```

Doit afficher quelque chose comme:
```
drwxr-xr-x  pharmaciecourcilles-demours-paris.mesoigner.fr
```

---

# 🎯 RÉSUMÉ - Toutes les commandes

**Copie/colle ces commandes dans l'ordre:**

```bash
# 1. Aller au dossier du projet
cd chemin/vers/ton/projet

# 2. Créer le dossier pour les CSS
mkdir -p public/assets/css

# 3. Télécharger CSS #1
curl -o public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css"

# 4. Télécharger CSS #2
curl -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"

# 5. Vérifier que les CSS sont là
ls -lh public/assets/css/

# 6. Rendre le script exécutable
chmod +x quick-migrate.sh

# 7. Exécuter la migration
./quick-migrate.sh

# 8. Vérifier que ça a marché
grep -r 'data-theme="messoins"' pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l

# 9. Lancer le serveur pour tester
php artisan serve

# 10. Arrêter le serveur (Ctrl + C)
```

---

# 📝 Notes importantes

- **Les fichiers CSS sont gros** (300KB total) - le téléchargement peut prendre 10-30 secondes
- **Le script de migration est rapide** - il traite 8000 fichiers en 30-60 secondes
- **Tout ça se passe EN LOCAL** - tu n'as pas besoin de git ou GitHub pour cette étape
- **Aucun fichier n'est supprimé** - c'est juste des modifications de contenu

---

# ✅ CHECKLIST FINALE

- [ ] Étape 1a: Terminal ouvert
- [ ] Étape 1b: Je suis dans le bon dossier (`cd ...`)
- [ ] Étape 1c: Commande 1 exécutée (`mkdir -p ...`)
- [ ] Étape 1c: Commande 2 exécutée (téléchargement CSS #1)
- [ ] Étape 1c: Commande 3 exécutée (téléchargement CSS #2)
- [ ] Étape 1d: Vérification (`ls -lh ...`) - Les fichiers sont là ✅
- [ ] Étape 2a: Script rendu exécutable (`chmod +x ...`)
- [ ] Étape 2b: Migration exécutée (`./quick-migrate.sh`)
- [ ] Étape 3: Vérification 1 OK (CSS présents)
- [ ] Étape 3: Vérification 2 OK (remplacements faits)
- [ ] Étape 3: Vérification 3 OK (anciennes URLs supprimées)
- [ ] Étape 4: Serveur lancé et testé
- [ ] 🎉 Migration complétée!

---

# 🚀 C'EST PRÊT!

Suis simplement les étapes 1-4 dans l'ordre, utilise les commandes prêtes à copier/coller, et tu auras fini en 10 minutes! 

**Bonne chance! 💪**
