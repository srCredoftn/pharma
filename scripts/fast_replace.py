#!/usr/bin/env python3
"""
Script rapide de remplacement en masse avec gestion parallèle
Remplace domaine, logo et thème à travers le projet
"""

import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Configuration
REPLACEMENTS = [
    ("pharmaciecourcelles-demours-paris.mesoigner.fr", "pharmacie-campguezo-cotonou.messoins.bj"),
    ("logo-mesoigner", "logo-messoins"),
    ('data-theme="mesoigner"', 'data-theme="messoins"'),
    ("data-theme='mesoigner'", "data-theme='messoins'"),
]

INCLUDE_EXTENSIONS = {
    ".php", ".html", ".htm", ".js", ".ts", ".jsx", ".tsx",
    ".css", ".scss", ".sass", ".json", ".md", ".yml", ".yaml",
    ".xml", ".ini", ".env", ".conf",
}

EXCLUDE_DIRS = {".git", "node_modules", "vendor", "storage", ".idea", ".vscode", ".backups"}

# Thread-safe counter
lock = threading.Lock()
stats = {"files_processed": 0, "files_modified": 0, "errors": 0}


def should_process(path: Path) -> bool:
    """Vérifier si le fichier doit être traité"""
    # Vérifier extensions
    if path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True
    
    # Fichiers sans extension (tenter si pas binaire)
    if path.suffix == "":
        try:
            with path.open("rb") as f:
                chunk = f.read(512)
            return b"\x00" not in chunk
        except:
            return False
    
    return False


def process_file(filepath: Path) -> tuple:
    """Traiter un fichier et retourner les stats"""
    try:
        # Lire le fichier
        try:
            content = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                content = filepath.read_text(encoding="latin-1")
            except:
                return filepath, False, 0

        original_content = content

        # Appliquer les remplacements
        changes = 0
        for old, new in REPLACEMENTS:
            count = content.count(old)
            if count > 0:
                content = content.replace(old, new)
                changes += count

        # Écrire si modifié
        if content != original_content:
            filepath.write_text(content, encoding="utf-8")
            return filepath, True, changes

        return filepath, False, 0

    except Exception as e:
        return filepath, False, 0


def rename_items(root: Path):
    """Renommer les dossiers et fichiers"""
    renamed = []
    
    # Dossiers d'abord (de plus profond à moins profond)
    all_dirs = sorted([d for d in root.rglob("*") if d.is_dir()], 
                      key=lambda x: -len(x.parts))
    
    for dir_path in all_dirs:
        new_name = dir_path.name
        for old, new in REPLACEMENTS:
            if old in new_name:
                new_name = new_name.replace(old, new)
        
        if new_name != dir_path.name:
            try:
                new_path = dir_path.parent / new_name
                dir_path.rename(new_path)
                renamed.append(("dir", dir_path.name, new_name))
            except Exception as e:
                pass
    
    # Fichiers
    all_files = [f for f in root.rglob("*") if f.is_file()]
    for file_path in all_files:
        new_name = file_path.name
        for old, new in REPLACEMENTS:
            if old in new_name:
                new_name = new_name.replace(old, new)
        
        if new_name != file_path.name:
            try:
                new_path = file_path.parent / new_name
                file_path.rename(new_path)
                renamed.append(("file", file_path.name, new_name))
            except Exception as e:
                pass
    
    return renamed


def main():
    root = Path(".")
    
    print("🚀 REMPLACEMENT RAPIDE EN MASSE")
    print("=" * 60)
    print()
    
    # Collecter tous les fichiers à traiter
    print("🔍 Recherche des fichiers...")
    files_to_process = []
    for path in root.rglob("*"):
        if path.is_file() and should_process(path):
            # Vérifier si dans un dossier exclu
            if not any(excluded in path.parts for excluded in EXCLUDE_DIRS):
                files_to_process.append(path)
    
    total_files = len(files_to_process)
    print(f"   Trouvé: {total_files} fichiers")
    print()
    
    # Traiter les fichiers en parallèle
    print("⏳ Traitement en cours...")
    modified = 0
    total_changes = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_file, f): f for f in files_to_process}
        
        for idx, future in enumerate(as_completed(futures), 1):
            try:
                filepath, was_modified, changes = future.result()
                if was_modified:
                    modified += 1
                    total_changes += changes
                
                if idx % 500 == 0:
                    print(f"   ✓ {idx}/{total_files} fichiers traités...")
            except Exception as e:
                pass
    
    print(f"   ✓ {total_files}/{total_files} fichiers traités")
    print()
    
    # Renommer
    print("📝 Renommage des dossiers et fichiers...")
    renamed = rename_items(root)
    print(f"   ✓ {len(renamed)} éléments renommés")
    print()
    
    # Résumé
    print("=" * 60)
    print("✅ REMPLACEMENT TERMINÉ!")
    print("=" * 60)
    print()
    print(f"📊 Résumé:")
    print(f"   Fichiers modifiés: {modified}")
    print(f"   Total remplacements: {total_changes}")
    print()
    
    # Vérification
    print("🔍 Vérification:")
    print()
    
    remaining_domain = os.popen(
        'grep -RIn "pharmaciecourcelles-demours-paris.mesoigner.fr" . 2>/dev/null | wc -l'
    ).read().strip()
    print(f"   Domaine restant: {remaining_domain}")
    
    remaining_logo = os.popen(
        'grep -RIn "logo-mesoigner" . 2>/dev/null | wc -l'
    ).read().strip()
    print(f"   Logo restant: {remaining_logo}")
    
    remaining_theme = os.popen(
        'grep -RIn \'data-theme="mesoigner"\' . 2>/dev/null | wc -l'
    ).read().strip()
    print(f"   Thème restant: {remaining_theme}")
    
    print()
    print("✨ Fait!")


if __name__ == "__main__":
    main()
