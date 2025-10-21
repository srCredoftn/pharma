# 🎯 COMMANDES SIMPLES - À EXÉCUTER DANS L'ORDRE

**Ouvre le terminal et copie/colle chaque commande une à une**

---

## AVANT DE COMMENCER
Va dans ton dossier projet d'abord:
```
cd chemin/vers/ton/projet
```

---

## ✅ COMMANDE 1
**Créer le dossier CSS**
```bash
mkdir -p public/assets/css
```
⏱️ Durée: 1 seconde

---

## ✅ COMMANDE 2
**Télécharger le 1er CSS (22KB)**
```bash
curl -o public/assets/css/scripts.3e902af8.css "https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css"
```
⏱️ Durée: 5 secondes
📥 Attendez la barre de progression

---

## ✅ COMMANDE 3
**Télécharger le 2e CSS (271KB)**
```bash
curl -o public/assets/css/mesoigner.6063c722.css "https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css"
```
⏱️ Durée: 5-10 secondes
📥 Attendez la barre de progression

---

## ✅ COMMANDE 4
**Vérifier que les fichiers sont téléchargés**
```bash
ls -lh public/assets/css/
```
✔️ Vous devez voir 2 fichiers

---

## ✅ COMMANDE 5
**Rendre le script exécutable**
```bash
chmod +x quick-migrate.sh
```
⏱️ Durée: 1 seconde

---

## ✅ COMMANDE 6
**LANCER LA MIGRATION (LA PLUS IMPORTANTE!)**
```bash
./quick-migrate.sh
```
⏱️ Durée: 30-60 secondes
🔄 Vous verrez du texte qui défile
✔️ Attendez le message "Migration terminée!"

---

## ✅ COMMANDE 7
**Vérifier que la migration a marché**
```bash
grep -r 'data-theme="messoins"' pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l
```
✔️ Vous devez voir: 1000+

---

## ✅ COMMANDE 8
**Vérifier qu'il n'y a plus d'anciennes URLs**
```bash
grep -r "https://cdn.mesoigner.fr" pharmaciecourcelles-demours-paris.mesoigner.fr/ | wc -l
```
✔️ Vous devez voir: 0

---

## ✅ COMMANDE 9
**Lancer le serveur pour tester**
```bash
php artisan serve
```
⏱️ Durée: 2-3 secondes
🌐 Ouvrez: http://localhost:8000
✔️ Vérifiez que le site s'affiche correctement

---

## ✅ COMMANDE 10
**Arrêter le serveur**
```
Ctrl + C
```
(Appuyez sur Ctrl et C en même temps)

---

# 🎉 C'EST FINI!

Vous avez terminé la migration! 🚀

---

# 🔗 FICHIERS IMPORTANTS

- `GUIDE_LOCAL_COMPLET.md` - Guide complet avec explications
- `GUIDE_VISUEL_ETAPE_PAR_ETAPE.md` - Guide avec détails visuels
- `COMMANDES_A_EXECUTER.txt` - Liste des commandes à copier
- `COMMANDES_SIMPLES.md` - Ce fichier (version simple)
- `quick-migrate.sh` - Script de migration
- `scripts/migrate_cdn.py` - Alternative Python

---

# 🆘 PROBLÈMES?

**"command not found"**
→ Installer le logiciel manquant

**"Permission denied"**
→ Exécuter: `chmod +x quick-migrate.sh`

**Autres problèmes**
→ Consulter `GUIDE_LOCAL_COMPLET.md` ou `GUIDE_VISUEL_ETAPE_PAR_ETAPE.md`

---

**Bonne migration! 💪**
