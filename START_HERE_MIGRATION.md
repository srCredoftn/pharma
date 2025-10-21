# 🚀 MIGRATION - COMMENCEZ ICI

**Bienvenue!** Ce guide vous explique comment migrer votre site de `pharmaciecourcelles-demours-paris.mesoigner.fr` vers `pharmacie-campguezo-cotonou.messoins.bj`

---

## ⏱️ Combien de temps ça prend?

**5-10 minutes** si vous suivez ce guide!

---

## 📚 Quel document lire?

### 🏃 Je suis pressé - Juste les commandes!
→ Ouvrir: `MIGRATION_EXECUTION_STEPS.md`

### 🚶 Je veux comprendre chaque étape
→ Ouvrir: `MIGRATION_COMPLETE_GUIDE.md`

### 📊 Je veux voir le résumé complet
→ Ouvrir: `MIGRATION_SUMMARY.md`

### 📝 Je préfère les commandes simples (sans code complexe)
→ Ouvrir: `COMMANDES_SIMPLES.md`

---

## 🎯 Ce qui va se passer

### Avant:
```
Site: pharmaciecourcelles-demours-paris.mesoigner.fr
Logo: logo-mesoigner.svg
CDN: cdn.mesoigner.fr
```

### Après:
```
Site: pharmacie-campguezo-cotonou.messoins.bj
Logo: logo-messoins.svg
CDN: cdn.messoins.bj
```

---

## ✅ 3 étapes simples

### 1️⃣ Sauvegarder (IMPORTANT!)
```bash
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr \
      pharmaciecourcelles-demours-paris.mesoigner.fr.backup
```

### 2️⃣ Exécuter la migration
```bash
python3 scripts/migrate_complete.py
```

### 3️⃣ Renommer le dossier
```bash
mv pharmaciecourcelles-demours-paris.mesoigner.fr \
   pharmacie-campguezo-cotonou.messoins.bj
```

---

## 🆘 J'ai un problème!

### Python n'est pas installé?
→ Utiliser: `migrate-cdn-complete.sh` (Bash script)

### Je suis sur Windows?
→ Utiliser Git Bash ou WSL, puis les mêmes commandes

### Je n'aime pas les scripts?
→ Ouvrir: `MIGRATION_COMPLETE_GUIDE.md` section "sed directement"

### Autre problème?
→ Ouvrir: `MIGRATION_COMPLETE_GUIDE.md` section "Dépannage"

---

## 📋 Checklist avant de commencer

- [ ] J'ai créé une sauvegarde du dossier
- [ ] Je suis dans le bon répertoire du projet
- [ ] J'ai Python 3 installé (ou j'utiliserai Bash)
- [ ] J'ai 500 MB d'espace disque libre
- [ ] Je ne modifie pas le dossier pendant la migration

---

## 🎬 ALLEZ-Y MAINTENANT!

**Choisissez votre chemin:**

```
┌─────────────────────────────────────────┐
│  Je suis pressé (5 minutes)             │
│  → MIGRATION_EXECUTION_STEPS.md         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Je veux tout comprendre (10 minutes)   │
│  → MIGRATION_COMPLETE_GUIDE.md          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Je veux juste exécuter              │
│  → COMMANDES_SIMPLES.md                 │
└─────────────────────────────────────────┘
```

---

## 🔑 Fichiers clés

```
Scripts de migration:
  ✅ scripts/migrate_complete.py     - Script Python (RECOMMANDÉ)
  ✅ migrate-cdn-complete.sh          - Script Bash (alternative)
  ✅ quick-migrate.sh                 - Autre script

Documentation:
  📖 MIGRATION_EXECUTION_STEPS.md      - COMMENCEZ PAR CELUI-CI
  📖 MIGRATION_COMPLETE_GUIDE.md       - Guide détaillé
  📖 MIGRATION_SUMMARY.md              - Résumé complet
  📖 COMMANDES_SIMPLES.md              - Juste les commandes

Fichiers modifiés:
  ✅ index.html                        - Redirection mise à jour
  ✅ migrate-cdn-complete.sh           - Script complet
  ✅ scripts/migrate_complete.py       - Script Python
```

---

## 📞 Aide rapide

| Situation | Action |
|-----------|--------|
| Pas sûr par où commencer | Lire `MIGRATION_EXECUTION_STEPS.md` |
| Python ne marche pas | Utiliser `migrate-cdn-complete.sh` |
| Je veux tout comprendre | Lire `MIGRATION_COMPLETE_GUIDE.md` |
| Erreur ou problème | Section "Dépannage" dans guide complet |
| Besoin de vérifier | Lire "Vérifications" dans le guide |

---

## ✨ Promesses

✅ **Rapide** - 5-10 minutes d'exécution  
✅ **Sûr** - Scripts testés et non destructifs  
✅ **Simple** - Juste copier/coller des commandes  
✅ **Complet** - Tous les fichiers inclus  
✅ **Documenté** - Guides détaillés inclus  
✅ **Vérifiable** - Scripts de vérification inclus  

---

## 🚀 Maintenant?

**Ouvrez:** `MIGRATION_EXECUTION_STEPS.md`

Et suivez simplement les étapes! 

---

**Version:** 1.0  
**Date:** Octobre 2025  
**Prêt?** Let's go! 🎉
