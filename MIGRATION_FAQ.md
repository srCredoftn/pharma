# ❓ FAQ - Questions Fréquemment Posées

**Réponses rapides aux questions les plus courantes sur la migration.**

---

## 🚀 Avant la migration

### Q: Par où commencer?
**R:** Ouvrir `START_HERE_MIGRATION.md` qui vous orientera vers le bon document.

---

### Q: Combien de temps ça prend?
**R:** La migration complète prend **5-10 minutes** selon votre machine.
- Sauvegarde: 1-2 min
- Migration Python: 3-5 min
- Vérification: 1-2 min
- Test local: 2-3 min
- **Total: 7-12 minutes**

---

### Q: Est-ce dangereux?
**R:** Non, si vous créez d'abord une sauvegarde (3 lignes de commande).
```bash
cp -r pharmaciecourcelles-demours-paris.mesoigner.fr \
      pharmaciecourcelles-demours-paris.mesoigner.fr.backup
```
C'est votre filet de sécurité. En cas de problème, exécuter `MIGRATION_ROLLBACK.sh`.

---

### Q: Python est-il obligatoire?
**R:** Non. Vous avez 3 options:
1. **Python** (recommandé) - `python3 scripts/migrate_complete.py`
2. **Bash** - `./migrate-cdn-complete.sh`
3. **sed direct** - commandes manuelles

Choisissez selon votre système.

---

### Q: Dois-je arrêter le serveur avant?
**R:** Oui, si Laravel est en train de servir. Arrêter avec `Ctrl+C`.

Sinon, pas besoin. Les fichiers statiques se modifient sans problème.

---

### Q: Combien d'espace disque faut-il?
**R:** Minimum **500 MB** libres.
```bash
df -h .
# Vérifier la colonne "Avail"
```

---

### Q: Puis-je faire la migration sur un serveur en prod?
**R:** **Non, pas recommandé.** Faire d'abord en local ou en staging.

1. Test local
2. Test staging
3. Puis production

---

### Q: Que se passe-t-il pendant la migration?
**R:** Les scripts font des `grep` et `sed` sur les fichiers HTML:
```
Chercher: pharmaciecourcelles-demours-paris.mesoigner.fr
Remplacer: pharmacie-campguezo-cotonou.messoins.bj

Chercher: data-theme="mesoigner"
Remplacer: data-theme="messoins"

Chercher: https://cdn.mesoigner.fr
Remplacer: https://cdn.messoins.bj

...etc (5+ remplacements)
```

---

## ⚙️ Pendant la migration

### Q: Le script s'arrête - qu'est-ce que c'est?
**R:** Le script demande confirmation:
```
Continuer? (oui/non):
```
Taper: `oui` et appuyer sur `Enter`.

---

### Q: Puis-je arrêter le script avec Ctrl+C?
**R:** **Déconseill��.** Les fichiers peuvent rester en état intermédiaire.

Si vous devez l'arrêter, restaurer avec `MIGRATION_ROLLBACK.sh`.

---

### Q: Le script prend trop longtemps?
**R:** Normal. 8000 fichiers à traiter = 3-5 minutes.

Patience! C'est mieux que rapide et cassé.

---

### Q: Le script affiche des erreurs?
**R:** Vérifier:
1. Êtes-vous dans le bon répertoire?
   ```bash
   pwd
   # Doit afficher le chemin du projet
   ```

2. Le dossier source existe?
   ```bash
   ls pharmaciecourcelles-demours-paris.mesoigner.fr/
   ```

3. Vous avez les permissions?
   ```bash
   test -w . && echo "OK" || echo "Permission denied"
   ```

---

## ✅ Après la migration

### Q: Comment vérifier que ça a marché?
**R:** Exécuter:
```bash
./MIGRATION_VERIFY.sh
```

Ou manuellement:
```bash
# Nouveau domaine: doit retourner 1000+
grep -r 'data-theme="messoins"' pharmacie-campguezo-cotonou.messoins.bj/ | wc -l

# Ancien domaine: doit retourner 0
grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ | wc -l
```

---

### Q: Les fichiers CSS ne chargent pas
**R:** Vérifier:
```bash
# Les fichiers CSS existent?
ls -la public/assets/css/

# Elles contiennent du contenu?
wc -l public/assets/css/*.css

# Si vides, c'est OK pour maintenant (elles peuvent être créées après)
```

---

### Q: Le logo n'affiche pas
**R:** Vérifier:
```bash
# Le logo est référencé correctement?
grep -r "logo-messoins" pharmacie-campguezo-cotonou.messoins.bj/index.html

# Il doit être dans /assets/uploads/ ou sur le CDN
```

Si manquant, créer un placeholder:
```bash
echo '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="blue" width="100" height="100"/></svg>' > public/assets/uploads/logo-messoins.svg
```

---

### Q: Il y a encore des anciennes URL?
**R:** Vérifier lesquelles:
```bash
grep -r "pharmaciecourcelles-demours-paris" pharmacie-campguezo-cotonou.messoins.bj/ | head -5
```

Remplacer manuellement:
```bash
sed -i 's/pharmaciecourcelles-demours-paris\.mesoigner\.fr/pharmacie-campguezo-cotonou.messoins.bj/g' \
  pharmacie-campguezo-cotonou.messoins.bj/problematic_file.html
```

---

### Q: Les erreurs en console (F12) - est-ce grave?
**R:** Ça dépend:
- **Erreurs rouges (404)**: À corriger
- **Warnings jaunes**: Généralement OK
- **Messages gris**: Ignorables

Chercher les 404 sur les assets (CSS, JS, images).

---

### Q: Le site ne s'affiche pas correctement
**R:** Vérifier dans cet ordre:
1. Ouvrir F12 → Console → chercher erreurs rouges
2. Ouvrir F12 → Network → chercher 404
3. Vérifier que CSS charge
4. Vérifier que logo charge
5. Consulter `MIGRATION_POST_EXECUTION.md`

---

## 🔧 Dépannage

### Q: "command not found: python3"
**R:** Python 3 n'est pas installé.
```bash
# Vérifier
python3 --version

# Installer:
# - Mac: brew install python3
# - Linux: apt install python3
# - Windows: https://www.python.org/downloads/

# Puis réessayer
```

Ou utiliser le script Bash à la place:
```bash
chmod +x migrate-cdn-complete.sh
./migrate-cdn-complete.sh
```

---

### Q: "Permission denied" sur le script
**R:** Rendre exécutable:
```bash
chmod +x scripts/migrate_complete.py
chmod +x migrate-cdn-complete.sh
chmod +x MIGRATION_VERIFY.sh
chmod +x MIGRATION_ROLLBACK.sh
```

---

### Q: Le dossier ne se renomme pas
**R:** Vérifier les permissions:
```bash
chmod -R 755 pharmaciecourcelles-demours-paris.mesoigner.fr
```

Puis réessayer:
```bash
mv pharmaciecourcelles-demours-paris.mesoigner.fr \
   pharmacie-campguezo-cotonou.messoins.bj
```

Si ça ne marche toujours pas:
```bash
sudo mv pharmaciecourcelles-demours-paris.mesoigner.fr \
        pharmacie-campguezo-cotonou.messoins.bj
```

---

### Q: "No space left on device"
**R:** Plus d'espace disque libre.
```bash
# Vérifier
df -h .

# Libérer de l'espace ou utiliser un autre disque
```

---

### Q: Erreur: "sed: can't read"
**R:** Fichier verrouillé ou permission refusée.
```bash
# Vérifier permissions
ls -la pharmaciecourcelles-demours-paris.mesoigner.fr/index.html

# Corriger si nécessaire
chmod 644 pharmaciecourcelles-demours-paris.mesoigner.fr/*.html
```

---

## 🆘 Récupération

### Q: Quelque chose s'est cassé - comment restaurer?
**R:** Utiliser le script rollback:
```bash
chmod +x MIGRATION_ROLLBACK.sh
./MIGRATION_ROLLBACK.sh
```

Répondre `oui` à la confirmation.

---

### Q: La sauvegarde n'existe pas!
**R:** Malheureusement, on ne peut pas restaurer alors.

Deux options:
1. Si vous avez un backup Git: `git checkout HEAD pharmaciecourcelles-demours-paris.mesoigner.fr/`
2. Si vous avez un backup système: restaurer depuis backup

---

### Q: Je veux refaire la migration différemment
**R:** 
1. Restaurer l'original
2. Recommencer

Restaurer avec:
```bash
./MIGRATION_ROLLBACK.sh
```

---

## 🚀 Production

### Q: Puis-je mettre en prod tout de suite?
**R:** Non. Checklist avant prod:
- [ ] Testé localement
- [ ] Vérifications réussies
- [ ] Console navigateur: 0 erreurs
- [ ] Config Laravel mise à jour
- [ ] Cache vidé: `php artisan config:cache`
- [ ] Tests sur staging réussis

---

### Q: Dois-je mettre à jour le DNS?
**R:** **Oui**, mais c'est une autre étape:
1. Migration du code (fait)
2. Mettre à jour le DNS
3. Attendre propagation (jusqu'à 24h)
4. Vérifier: `nslookup pharmacie-campguezo-cotonou.messoins.bj`

---

### Q: Faut-il renouveler le certificat SSL?
**R:** **Oui**. Créer un nouveau certificat pour le nouveau domaine.
```bash
# Avec Let's Encrypt:
certbot certonly --standalone -d pharmacie-campguezo-cotonou.messoins.bj
```

---

### Q: Faut-il mettre à jour .htaccess?
**R:** Peut-être. Vérifier si vous avez des règles spécifiques au domaine:
```bash
grep "pharmaciecourcelles" .htaccess
```

Si oui, remplacer.

---

## 📚 Documentation

### Q: Où trouver plus d'aide?
**R:** Voir:
- `MIGRATION_COMPLETE_GUIDE.md` - Section "Dépannage"
- `MIGRATION_POST_EXECUTION.md` - Section "Problèmes"
- `README_MIGRATION.md` - Section "Support"

---

### Q: Quel document dois-je lire?
**R:** Ça dépend:
- Je suis pressé → `MIGRATION_EXECUTION_STEPS.md`
- Je veux comprendre → `MIGRATION_COMPLETE_GUIDE.md`
- Je veux juste des commandes → `COMMANDES_SIMPLES.md`
- Aidez-moi à préparer → `MIGRATION_READY_CHECKLIST.md`
- Je dois tester après → `MIGRATION_POST_EXECUTION.md`
- Je ne sais pas où commencer → `START_HERE_MIGRATION.md`

---

## 🎯 Résumé rapide

| Question | Réponse |
|----------|---------|
| Combien de temps? | 5-10 minutes |
| C'est dangereux? | Non si sauvegarde créée |
| Python obligatoire? | Non, 3 options disponibles |
| Je dois arrêter le serveur? | Oui |
| Espace disque? | 500 MB minimum |
| En production? | Non, d'abord local puis staging |
| Comment vérifier? | Exécuter `MIGRATION_VERIFY.sh` |
| Quelque chose se casse? | Exécuter `MIGRATION_ROLLBACK.sh` |
| Où trouver de l'aide? | `MIGRATION_COMPLETE_GUIDE.md` |

---

## 🎉 Vous avez d'autres questions?

Consulter:
1. Le document spécifique à votre situation
2. La section "Dépannage" du guide complet
3. Les scripts de vérification et rollback

**Bonne chance! 🚀**
