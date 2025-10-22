#!/usr/bin/env python3
"""
Script de diagnostic pour comprendre pourquoi les remplacements ne marche pas
"""

import os
import sys
from pathlib import Path

# Chercher un fichier contenant une des chaînes
test_strings = [
    "pharmaciecourcelles-demours-paris.mesoigner.fr",
    "logo-mesoigner",
    'data-theme="mesoigner"',
]

print("🔍 Diagnostic: Recherche de fichiers contenant les chaînes...")
print()

# Utiliser grep pour trouver des fichiers
for test_str in test_strings:
    print(f"Cherchant: {test_str}")
    result = os.popen(f'grep -l "{test_str}" $(find . -type f -name "*.html" | head -10) 2>/dev/null | head -1').read().strip()
    
    if result:
        print(f"  ✓ Trouvé dans: {result}")
        
        # Essayer de lire ce fichier
        filepath = Path(result)
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Chercher la chaîne
                if test_str in content:
                    print(f"    ✓ Chaîne trouvée dans le contenu lu")
                    
                    # Afficher un aperçu
                    idx = content.find(test_str)
                    preview = content[max(0, idx-50):min(len(content), idx+100)]
                    print(f"    Aperçu: ...{preview}...")
                else:
                    print(f"    ✗ Chaîne NON trouvée dans le contenu (problème d'encodage?)")
            except UnicodeDecodeError:
                print(f"    �� Erreur d'encodage UTF-8, essai latin-1...")
                try:
                    with open(filepath, 'r', encoding='latin-1') as f:
                        content = f.read()
                    if test_str in content:
                        print(f"    ✓ Trouvé avec latin-1!")
                    else:
                        print(f"    ✗ Pas trouvé même avec latin-1")
                except Exception as e:
                    print(f"    ✗ Erreur: {e}")
            except Exception as e:
                print(f"    ✗ Erreur lecture: {e}")
    else:
        print(f"  ✗ Aucun fichier trouvé")
    
    print()

print()
print("💡 Diagnostic: Vérifier les fichiers HTML bruts")
print()

# Chercher directement des fichiers HTML
html_files = list(Path(".").glob("pharmaciecourcelles-demours-paris.mesoigner.fr/*.html"))[:3]
print(f"Fichiers HTML trouvés: {len(html_files)}")

for html_file in html_files:
    print(f"\nFichier: {html_file}")
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher la chaîne
        search_str = "pharmaciecourcelles-demours-paris.mesoigner.fr"
        count = content.count(search_str)
        print(f"  Occurrences de '{search_str}': {count}")
        
        if count > 0:
            idx = content.find(search_str)
            preview = content[max(0, idx-50):min(len(content), idx+100)]
            print(f"  Aperçu: ...{preview}...")
    except Exception as e:
        print(f"  Erreur: {e}")
