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


def rename_directories_and_files(root: Path, dry_run: bool):
    renamed = []
    domain_mapping = [
        ("pharmaciecourcelles-demours-paris.mesoigner.fr", "pharmacie-campguezo-cotonou.messoins.bj"),
    ]
    file_mapping = [
        ("logo-mesoigner", "logo-messoins"),
    ]

    # Renommer les dossiers d'abord (de manière récursive)
    items_to_rename = []
    for path in root.rglob('*'):
        if path.is_dir():
            new_name = path.name
            for old, new in domain_mapping + file_mapping:
                if old in new_name:
                    new_name = new_name.replace(old, new)

            if new_name != path.name:
                items_to_rename.append((path, new_name, "directory"))
        elif path.is_file():
            new_name = path.name
            for old, new in file_mapping:
                if old in new_name:
                    new_name = new_name.replace(old, new)

            if new_name != path.name:
                items_to_rename.append((path, new_name, "file"))

    # Trier par profondeur (plus profond d'abord pour les dossiers)
    items_to_rename.sort(key=lambda x: (x[2] != "directory", -len(x[0].parts)))

    # Appliquer les renommages
    for path, new_name, item_type in items_to_rename:
        new_path = path.with_name(new_name)
        if dry_run:
            renamed.append({"from": str(path), "to": str(new_path), "type": item_type})
        else:
            try:
                path.rename(new_path)
                renamed.append({"from": str(path), "to": str(new_path), "type": item_type})
                print(f"  ✓ Renommé {item_type}: {path.name} → {new_name}")
            except Exception as e:
                renamed.append({
                    "from": str(path),
                    "to": str(new_path),
                    "type": item_type,
                    "error": str(e)
                })
                print(f"  ✗ Erreur renommage {item_type} {path.name}: {e}")

    return renamed


def process_all_files(root, args, backup_dir, include_ext, exclude_dirs):
    """Traiter tous les fichiers et retourner le résumé"""
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

    file_count = 0
    modified_count = 0

    # Parcours avec gestion robuste des erreurs
    for path in root.rglob('*'):
        try:
            if path.is_dir():
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

            file_count += 1
            text, enc = try_read_text(path)
            if text is None:
                continue

            changed, new_text, per_rule, delta = apply_replacements_to_text(text)
            if changed:
                if not args.dry_run:
                    try:
                        if backup_dir:
                            ensure_backup(path, backup_dir)
                        path.write_text(new_text, encoding=enc or "utf-8")
                        modified_count += 1
                    except IOError as io_err:
                        # Log l'erreur mais continue
                        summary["files"].append({
                            "path": str(path),
                            "encoding": enc,
                            "error": f"IOError lors de l'écriture: {str(io_err)}",
                        })
                        continue

                summary["files"].append({
                    "path": str(path),
                    "encoding": enc,
                    "changes": per_rule,
                })
                for k, v in per_rule.items():
                    summary["totals"][k] += v

                if modified_count % 100 == 0 and modified_count > 0:
                    print(f"  ✓ {modified_count} fichiers modifiés...")

        except Exception as e:
            # Ignorer les erreurs et continuer
            pass

    return summary, file_count, modified_count


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

    if not root.exists() or not root.is_dir():
        print(f"Racine invalide: {root}", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = None
    if not args.no_backup and not args.dry_run:
        backup_dir = Path(args.backup_dir) if args.backup_dir else Path(".backups") / f"replacements-{timestamp}"
        backup_dir = backup_dir.resolve()

    json_log_path = Path(args.json_log) if args.json_log else Path(f"replacements-log-{timestamp}.json")

    print("🔄 Traitement des fichiers...")
    summary, file_count, modified_count = process_all_files(root, args, backup_dir, include_ext, exclude_dirs)

    # Renommage éventuel des fichiers 'logo-mesoigner*'
    if args.rename_files:
        print("📝 Renommage des fichiers contenant 'logo-mesoigner'...")
        renamed = rename_logo_files(root, args.dry_run, args.include_hidden, exclude_dirs)
        summary["renamed_files"] = renamed

    # Log JSON
    try:
        with open(json_log_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"✓ Rapport écrit: {json_log_path}")
    except Exception as e:
        print(f"⚠ Impossible d'écrire le rapport JSON: {e}", file=sys.stderr)

    # Résumé console
    print(f"\n📊 Résumé ({file_count} fichiers traités, {modified_count} modifiés):")
    for rule in REPLACEMENTS:
        name = rule["name"]
        count = summary["totals"].get(name, 0)
        print(f"  ✓ {name}: {count} occurrences remplacées")
    if args.rename_files:
        print(f"  ✓ fichiers renommés: {len(summary['renamed_files'])}")

    if not args.dry_run:
        print("\n✅ Remplacements appliqués avec succès!")


if __name__ == "__main__":
    main()
