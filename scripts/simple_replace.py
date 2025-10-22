#!/usr/bin/env python3
"""
Script de remplacement simple et fiable
"""

import os
import sys
from pathlib import Path

# Remplacements
REPLACEMENTS = [
    ("pharmaciecourcelles-demours-paris.mesoigner.fr", "pharmacie-campguezo-cotonou.messoins.bj"),
    ("logo-mesoigner", "logo-messoins"),
    ('data-theme="mesoigner"', 'data-theme="messoins"'),
    ("data-theme='mesoigner'", "data-theme='messoins'"),
]

def is_text_file(filepath):
    """Vérifier si c'est un fichier texte"""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(512)
        return b'\x00' not in chunk
    except:
        return False

def process_file(filepath):
    """Traiter un fichier"""
    if not is_text_file(filepath):
        return False, 0
    
    try:
        # Essayer UTF-8 d'abord
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Essayer latin-1
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            return False, 0
    
    original = content
    changes = 0
    
    # Appliquer les remplacements
    for old, new in REPLACEMENTS:
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            changes += count
    
    # Écrire si modifié
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        except Exception as e:
            print(f"Erreur écriture {filepath}: {e}", file=sys.stderr)
            return False, 0
    
    return False, 0

def main():
    print("🚀 REMPLACEMENT SIMPLE")
    print("=" * 60)
    print()
    
    root = Path(".")
    modified = 0
    total_changes = 0
    errors = 0
    count = 0
    
    # Extensions valides
    valid_ext = {'.php', '.html', '.htm', '.js', '.ts', '.jsx', '.tsx', '.css', '.json', '.md', '.yml', '.yaml', '.xml', '.ini', '.env', '.conf', '.scss', '.sass'}
    
    # Parcourir tous les fichiers
    for filepath in root.rglob('*'):
        if not filepath.is_file():
            continue
        
        # Ignorer certains dossiers
        if any(x in filepath.parts for x in ['.git', 'node_modules', 'vendor', '.idea']):
            continue
        
        # Vérifier l'extension
        if filepath.suffix.lower() not in valid_ext and filepath.suffix != '':
            continue
        
        count += 1
        
        was_modified, changes = process_file(filepath)
        if was_modified:
            modified += 1
            total_changes += changes
            print(f"✓ {filepath} ({changes} remplacements)")
        
        if count % 1000 == 0:
            print(f"  [{count} fichiers traités...]")
    
    print()
    print("=" * 60)
    print(f"✅ TERMINÉ!")
    print("=" * 60)
    print()
    print(f"Fichiers traités: {count}")
    print(f"Fichiers modifiés: {modified}")
    print(f"Total remplacements: {total_changes}")
    print()

if __name__ == "__main__":
    main()
