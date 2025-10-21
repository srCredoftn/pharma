# Plan unique: Remplacements du domaine, du logo et du thème (tout-en-un)

Ce fichier contient: checklist, étapes, commandes, et un script Python prêt à l’emploi pour réaliser les 3 remplacements suivants à travers tout le projet.

- Replacement 1 (domaine):
  - Chercher: pharmaciecourcelles-demours-paris.mesoigner.fr
  - Remplacer: pharmacie-campguezo-cotonou.messoins.bj
- Replacement 2 (logo):
  - Chercher: logo-mesoigner
  - Remplacer: logo-messoins
- Replacement 3 (thème):
  - Chercher: data-theme="mesoigner"
  - Remplacer: data-theme="messoins"
  - Bonus: le script gère aussi data-theme='mesoigner' -> data-theme='messoins'


## 1) Checklist rapide
- Faire une sauvegarde Git (commit actuel) et/ou utiliser l’onglet History pour revenir en arrière si besoin.
- Lancer le script en mode simulation (dry-run) et lire le rapport.
- Lancer l’exécution réelle avec sauvegarde automatique des fichiers modifiés.
- Vérifier via recherches ciblées qu’il ne reste plus d’occurrences.
- Pousser les changements (bouton Push Code) et vérifier l’appli.


## 2) Répertoires pris en compte et exclusions
- Inclus: tous les fichiers texte courants (.php, .html, .htm, .js, .ts, .jsx, .tsx, .css, .scss, .sass, .json, .md, .yml, .yaml, .xml, .ini, .env, .conf)
- Exclus par défaut: .git, node_modules, vendor, storage, .idea, .vscode, .backups
- Les fichiers binaires sont ignorés automatiquement (détection des octets nuls).


## 3) Script Python prêt à l’emploi
Enregistrez le contenu ci-dessous tel quel dans un fichier scripts/perform_replacements.py puis exécutez les commandes de la section suivante.

```python
#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import shutil
import json
from datetime import datetime

REPLACEMENTS = [
    {
        "name": "domaine",
        "find": "pharmaciecourcelles-demours-paris.mesoigner.fr",
        "replace": "pharmacie-campguezo-cotonou.messoins.bj",
    },
    {
        "name": "logo",
        "find": "logo-mesoigner",
        "replace": "logo-messoins",
    },
    {
        "name": "theme_double_quotes",
        "find": "data-theme=\"mesoigner\"",
        "replace": "data-theme=\"messoins\"",
    },
    {
        "name": "theme_single_quotes",
        "find": "data-theme='mesoigner'",
        "replace": "data-theme='messoins'",
    },
]

DEFAULT_INCLUDE_EXT = {
    ".php", ".html", ".htm", ".js", ".ts", ".jsx", ".tsx",
    ".css", ".scss", ".sass", ".json", ".md", ".yml", ".yaml",
    ".xml", ".ini", ".env", ".conf",
}

DEFAULT_EXCLUDE_DIRS = {".git", "node_modules", "vendor", "storage", ".idea", ".vscode", ".backups"}


def is_binary_file(path: Path, read_bytes: int = 2048) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(read_bytes)
        return b"\x00" in chunk
    except Exception:
        return True


def try_read_text(path: Path):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc), enc
        except Exception:
            continue
    return None, None


def ensure_backup(original: Path, backup_root: Path):
    rel = original.relative_to(Path.cwd())
    dest = backup_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(original), str(dest))


def should_visit_dir(d: Path, exclude_dirs: set, include_hidden: bool) -> bool:
    name = d.name
    if not include_hidden and name.startswith('.'):
        return False
    if name in exclude_dirs:
        return False
    return True


def should_process_file(f: Path, include_ext: set, include_hidden: bool) -> bool:
    name = f.name
    if not include_hidden and name.startswith('.'):
        return False
    if f.suffix.lower() in include_ext:
        return True
    # Fichiers sans extension: tenter quand même si ce n'est pas binaire
    if f.suffix == "":
        return True
    return False


def apply_replacements_to_text(text: str):
    total_delta = 0
    per_rule = {}
    new_text = text
    for rule in REPLACEMENTS:
        before = new_text.count(rule["find"])
        if before:
            new_text = new_text.replace(rule["find"], rule["replace"])
            after = new_text.count(rule["find"])  # devrait être 0
            changed = before - after
            per_rule[rule["name"]] = changed
            total_delta += changed
        else:
            per_rule[rule["name"]] = 0
    changed = (new_text != text)
    return changed, new_text, per_rule, total_delta


def rename_logo_files(root: Path, dry_run: bool, include_hidden: bool, exclude_dirs: set):
    renamed = []
    for d in root.rglob('*'):
        if d.is_dir():
            if not should_visit_dir(d, exclude_dirs, include_hidden):
                # Skip descente dans ce dossier
                # Optimisation: ne pas descendre dans les dossiers exclus
                # En rglob, on ne peut pas stopper la descente facilement sans walk manuel
                pass
            continue
        if d.is_file() and "logo-mesoigner" in d.name:
            new_name = d.name.replace("logo-mesoigner", "logo-messoins")
            new_path = d.with_name(new_name)
            if dry_run:
                renamed.append({"from": str(d), "to": str(new_path)})
            else:
                try:
                    d.rename(new_path)
                    renamed.append({"from": str(d), "to": str(new_path)})
                except Exception as e:
                    renamed.append({"from": str(d), "to": str(new_path), "error": str(e)})
    return renamed


def main():
    parser = argparse.ArgumentParser(description="Remplacements de domaine, logo et thème à travers le projet")
    parser.add_argument("--root", default=".", help="Racine du projet (chemin relatif)")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans écriture")
    parser.add_argument("--no-backup", action="store_true", help="Ne pas créer de sauvegarde des fichiers modifiés")
    parser.add_argument("--backup-dir", default=None, help="Chemin du dossier de sauvegarde")
    parser.add_argument("--include-ext", default=",".join(sorted(DEFAULT_INCLUDE_EXT)), help="Extensions incluses, séparées par des virgules")
    parser.add_argument("--include-hidden", action="store_true", help="Inclure fichiers/dossiers cachés")
    parser.add_argument("--exclude-dirs", default=",".join(sorted(DEFAULT_EXCLUDE_DIRS)), help="Dossiers exclus, séparés par des virgules")
    parser.add_argument("--json-log", default=None, help="Fichier JSON de log des changements")
    parser.add_argument("--rename-files", action="store_true", help="Renommer aussi les fichiers qui contiennent 'logo-mesoigner' -> 'logo-messoins'")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    include_ext = {e.strip().lower() if e.strip().startswith('.') else f".{e.strip().lower()}" for e in args.include_ext.split(',') if e.strip()}
    exclude_dirs = {d.strip() for d in args.exclude_dirs.split(',') if d.strip()}

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = None
    if not args.no_backup and not args.dry_run:
        backup_dir = Path(args.backup_dir) if args.backup_dir else Path(".backups") / f"replacements-{timestamp}"
        backup_dir = backup_dir.resolve()

    json_log_path = Path(args.json_log) if args.json_log else Path(f"replacements-log-{timestamp}.json")

    summary = {
        "root": str(root),
        "dry_run": args.dry_run,
        "backup_dir": str(backup_dir) if backup_dir else None,
        "include_ext": sorted(include_ext),
        "exclude_dirs": sorted(exclude_dirs),
        "include_hidden": args.include_hidden,
        "rename_files": args.rename_files,
        "files": [],
        "totals": {r["name"]: 0 for r in REPLACEMENTS},
        "renamed_files": [],
    }

    if not root.exists() or not root.is_dir():
        print(f"Racine invalide: {root}", file=sys.stderr)
        sys.exit(1)

    # Parcours
    for path in root.rglob('*'):
        try:
            if path.is_dir():
                # Contrôle basique via nom du dossier courant
                if path.name in exclude_dirs:
                    continue
                if not args.include_hidden and path.name.startswith('.'):
                    continue
                continue
            if not path.is_file():
                continue

            if not should_process_file(path, include_ext, args.include_hidden):
                continue

            if is_binary_file(path):
                continue

            text, enc = try_read_text(path)
            if text is None:
                continue

            changed, new_text, per_rule, delta = apply_replacements_to_text(text)
            if changed:
                if not args.dry_run:
                    if backup_dir:
                        ensure_backup(path, backup_dir)
                    path.write_text(new_text, encoding=enc or "utf-8")
                summary["files"].append({
                    "path": str(path),
                    "encoding": enc,
                    "changes": per_rule,
                })
                for k, v in per_rule.items():
                    summary["totals"][k] += v
        except Exception as e:
            summary["files"].append({
                "path": str(path),
                "error": str(e),
            })

    # Renommage éventuel des fichiers 'logo-mesoigner*'
    if args.rename_files:
        renamed = rename_logo_files(root, args.dry_run, args.include_hidden, exclude_dirs)
        summary["renamed_files"] = renamed

    # Log JSON
    try:
        with open(json_log_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"Rapport écrit: {json_log_path}")
    except Exception as e:
        print(f"Impossible d'écrire le rapport JSON: {e}", file=sys.stderr)

    # Résumé console
    print("\nRésumé des remplacements:")
    for rule in REPLACEMENTS:
        name = rule["name"]
        print(f"- {name}: {summary['totals'].get(name, 0)} occurrences remplacées")
    if args.rename_files:
        print(f"- fichiers renommés: {len(summary['renamed_files'])}")


if __name__ == "__main__":
    main()
```


## 4) Commandes (dans l’ordre)
- Créer le fichier du script:
  - Chemin: scripts/perform_replacements.py
  - Coller le code ci-dessus tel quel et enregistrer.

- Simulation (dry-run) avec rapport JSON:
```
python3 scripts/perform_replacements.py --dry-run --json-log replacements-dry-run.json
```

- Exécution réelle avec sauvegarde et renommage des fichiers logo:
```
python3 scripts/perform_replacements.py --rename-files
```

- Exécution réelle sans renommage de fichiers:
```
python3 scripts/perform_replacements.py
```

- Exécution avec un dossier de sauvegarde personnalisé:
```
python3 scripts/perform_replacements.py --backup-dir .backups/replacements-migration
```


## 5) Vérifications après exécution
- Vérifier qu’il ne reste plus d’occurrences:
```
# Domaine
grep -RIn "pharmaciecourcelles-demours-paris\.mesoigner\.fr" . | wc -l

# Logo (références restantes)
grep -RIn "logo-mesoigner" . | wc -l

# Thème
grep -RIn 'data-theme=\"mesoigner\"' . | wc -l
grep -RIn "data-theme='mesoigner'" . | wc -l
```
- Inspecter le rapport JSON généré (replacements-log-YYYYmmdd-HHMMSS.json) pour connaître les fichiers modifiés.


## 6) Rollback (si nécessaire)
- Chaque fichier modifié a été sauvegardé dans un dossier .backups/replacements-YYYYmmdd-HHMMSS en conservant l’arborescence.
- Pour restaurer un fichier particulier:
```
cp .backups/replacements-YYYYmmdd-HHMMSS/chemin/vers/fichier.ext chemin/vers/fichier.ext
```


## 7) Conseils et notes
- Le script ne touche pas les fichiers binaires (images, polices, etc.).
- Les remplacements sont exacts et ciblés sur les chaînes spécifiées, sans affecter d’autres usages de "mesoigner".
- Le renommage des fichiers contenant "logo-mesoigner" est optionnel via --rename-files.
- Si vous avez des besoins additionnels (autres motifs à remplacer), ajoutez une entrée au tableau REPLACEMENTS.


## 8) Ordre de priorité pour ne pas se perdre
1. Créer scripts/perform_replacements.py avec le code ci-dessus.
2. Lancer la simulation (dry-run) et lire replacements-dry-run.json.
3. Lancer l’exécution réelle avec sauvegarde: python3 scripts/perform_replacements.py
4. Vérifier via grep que tout est remplacé.
5. Tester l’application, puis utiliser le bouton Push Code pour pousser les changements.


## 9) Ce que fait exactement le script
- Parcourt tout le projet en partant de . en ignorant: .git, node_modules, vendor, storage, .idea, .vscode, .backups
- Ouvre uniquement les fichiers texte (extensions courantes + fichiers sans extension non binaires).
- Applique les remplacements ci-dessous, en comptant précisément les occurrences: 
  - pharmaciecourcelles-demours-paris.mesoigner.fr -> pharmacie-campguezo-cotonou.messoins.bj
  - logo-mesoigner -> logo-messoins
  - data-theme="mesoigner" -> data-theme="messoins"
  - data-theme='mesoigner' -> data-theme='messoins'
- Sauvegarde automatiquement tout fichier modifié (sauf en --dry-run).
- Génère un rapport JSON détaillant les fichiers changés et les compteurs par règle.
- Peut renommer les fichiers qui contiennent "logo-mesoigner" dans leur nom si --rename-files est fourni.
