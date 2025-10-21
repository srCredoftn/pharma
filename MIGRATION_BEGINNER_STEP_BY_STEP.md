# 🚀 MIGRATION POUR DÉBUTANTS - ÉTAPE PAR ÉTAPE

**Ce guide est JUSTE POUR VOUS. Pas de coding, juste suivre les étapes.**

---

## ✅ Avant de commencer

**Vous allez:**
1. ✅ Changer le nom de votre site
2. ✅ Changer le logo
3. ✅ Vérifier que ça marche
4. ✅ **C'est tout!**

**Durée:** 30 minutes maximum  
**Difficulté:** Très facile (juste lire et cliquer)

---

## 🎯 Le changement (pour comprendre):

| Avant | Après |
|-------|-------|
| `pharmaciecourcelles-demours-paris.mesoigner.fr` | `pharmacie-campguezo-cotonou.messoins.bj` |
| Logo: `mesoigner` | Logo: `messoins` |
| Thème: `mesoigner` | Thème: `messoins` |

**C'est simplement des replacements = chercher/remplacer**

---

## 📋 ÉTAPE 1: Sauvegarder (OBLIGATOIRE!)

### Qu'est-ce que c'est?
C'est faire une copie de vos fichiers au cas où il y aurait un problème.

### Comment faire?
Je vais faire cette copie **POUR VOUS** automatiquement.

### Ce qui va se passer:
✅ Copie créée = vous êtes en sécurité!

---

## 📋 ÉTAPE 2: Préparer les dossiers

### Qu'est-ce que c'est?
Créer des dossiers pour stocker les fichiers (CSS, images, etc.)

### Comment faire?
Je vais créer ces dossiers **POUR VOUS**:
- `public/assets/css/` - Pour les fichiers de style
- `public/assets/uploads/` - Pour les images
- `public/assets/fonts/` - Pour les polices
- `public/assets/media/` - Pour les vidéos

### Ce qui va se passer:
✅ Dossiers créés = prêt pour la suite!

---

## 📋 ÉTAPE 3: Faire les replacements (LE TRAVAIL PRINCIPAL)

### Qu'est-ce que c'est?
**Chercher/remplacer** dans TOUS les fichiers HTML.

Exemple:
```
Chercher: pharmaciecourcelles-demours-paris.mesoigner.fr
Remplacer par: pharmacie-campguezo-cotonou.messoins.bj
```

### Combien de fichiers?
~8,000 fichiers HTML

### Comment je vais faire?
Je vais utiliser un **script Python** qui va:
1. Ouvrir chaque fichier
2. Chercher le vieux texte
3. Le remplacer par le nouveau
4. Sauvegarder le fichier

### Ce qui va se passer:
✅ ~8,000 fichiers modifiés automatiquement = FAIT!

### Les replacements qu'on va faire:

**Replacement 1: Le domaine principal**
```
Chercher: pharmaciecourcelles-demours-paris.mesoigner.fr
Remplacer: pharmacie-campguezo-cotonou.messoins.bj
```

**Replacement 2: Le logo**
```
Chercher: logo-mesoigner
Remplacer: logo-messoins
```

**Replacement 3: Le thème**
```
Chercher: data-theme="mesoigner"
Remplacer: data-theme="messoins"
```

**Replacement 4: CDN (serveur de contenu)**
```
Chercher: https://cdn.mesoigner.fr
Remplacer: https://cdn.messoins.bj
```

---

## 📋 ÉTAPE 4: Renommer le dossier principal

### Qu'est-ce que c'est?
Le dossier principal contient TOUS vos fichiers HTML. On doit le renommer.

### Avant:
```
pharmaciecourcelles-demours-paris.mesoigner.fr/  ← ANCIEN NOM
```

### Après:
```
pharmacie-campguezo-cotonou.messoins.bj/  ← NOUVEAU NOM
```

### Comment faire?
Je vais le faire **POUR VOUS**.

### Ce qui va se passer:
✅ Dossier renommé = votre site a un nouveau nom!

---

## ✅ ÉTAPE 5: Vérifier que ça a marché

### Qu'est-ce que c'est?
Vérifier que TOUS les replacements ont bien été faits.

### Comment faire?
Je vais exécuter un **script de vérification** qui va:
1. Compter combien de fichiers ont le nouveau texte
2. Vérifier que l'ancien texte n'existe plus
3. Vous montrer un rapport

### Résultats attendus:

**✅ Recherche 1: Nouveau domaine**
```
Résultat: 1000+ fichiers trouvés
✅ BON! Ça veut dire que le remplacement a marché
```

**✅ Recherche 2: Ancien domaine**
```
Résultat: 0 fichiers trouvés
✅ BON! L'ancien domaine n'existe plus
```

**✅ Recherche 3: Ancien CDN**
```
Résultat: 0 fichiers trouvés
✅ BON! L'ancien CDN n'existe plus
```

---

## 🧪 ÉTAPE 6: Tester localement

### Qu'est-ce que c'est?
Vérifier que votre site marche bien avec les modifications.

### Comment faire?
Je vais vous montrer comment **lancer le serveur test** et **vérifier** que le site s'affiche.

### Points à vérifier:
- ✅ La page s'affiche (pas d'erreur)
- ✅ Le logo est visible (en haut à gauche)
- ✅ Le CSS est chargé (les couleurs sont bonnes)
- ✅ Les images s'affichent
- ✅ Aucune erreur en console (appuyer sur F12)

---

## 📊 RÉCAPITULATIF DES ÉTAPES

| Étape | Ce qu'on fait | Temps |
|-------|---------------|-------|
| 1️⃣ Sauvegarder | Copier les fichiers pour la sécurité | 2 min |
| 2️⃣ Préparer | Créer les dossiers assets | 1 min |
| 3️⃣ Remplacer | Chercher/remplacer dans 8000 fichiers | 10 min |
| 4️⃣ Renommer | Renommer le dossier principal | 1 min |
| 5️⃣ Vérifier | Vérifier que tout est bon | 2 min |
| 6️⃣ Tester | Lancer le serveur et vérifier | 10 min |
| **TOTAL** | | **26 min** |

---

## ⚠️ Important à savoir

### Q: Va-t-il y avoir une erreur?
**R:** Non, nous avons un **plan B** (script de restauration) au cas où.

### Q: Vais-je perdre mes données?
**R:** Non, on fait une sauvegarde d'abord!

### Q: Combien ça coûte?
**R:** Rien! C'est gratuit.

### Q: Je dois installer quelque chose?
**R:** Non! On va faire tout ici (dans l'interface).

---

## 🎬 Prêt à commencer?

**Dites juste:** "Oui, commencez l'étape 1"

Et je vais vous faire chaque étape **une à une**, vous montrant exactement ce qui se passe.

---

## 📞 Besoin d'aide?

Pendant qu'on fait chaque étape, vous pouvez:
- Me poser des questions
- Me demander d'arrêter
- Me demander d'expliquer plus
- Vérifier que c'est correct

---

## ✨ Promesses

✅ **Simple** - Juste suivre les étapes  
✅ **Sûr** - On a une sauvegarde  
✅ **Rapide** - 30 minutes max  
✅ **Sans coding** - Pas besoin de programmer  
✅ **Guidé** - Je suis avec vous chaque étape  

---

## 🚀 Maintenant?

**Répondez juste:**

**"D'accord, commence l'étape 1!"**

Et je vais vous guider pour faire la sauvegarde.
