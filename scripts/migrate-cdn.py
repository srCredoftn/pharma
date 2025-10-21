#!/usr/bin/env python3
"""
Script de migration CDN: mesoigner → messoins
Remplace tous les liens CDN et renomme les répertoires
"""

import os
import re
from pathlib import Path

# Configuration de migration
MIGRATIONS = [
    # CDN URLs
    ('https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css', '/assets/css/scripts.3e902af8.css'),
    ('https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css', '/assets/css/mesoigner.6063c722.css'),
    ('https://cdn.mesoigner.fr/uploads/logos/logo-mesoigner.svg', '/assets/uploads/logo-messoins.svg'),
    ('https://cdn.mesoigner.fr/src/img/layout/header-wrapper.png', '/assets/uploads/header-wrapper.png'),
    
    # Branding (mesoigner → messoins)
    ('data-theme="mesoigner"', 'data-theme="messoins"'),
    ('logo-mesoigner', 'logo-messoins'),
    ('cdn.mesoigner.fr', 'cdn.messoins.bj'),
    
    # Domaine
    ('pharmaciecourcelles-demours-paris.mesoigner.fr', 'pharmacie-campguezo-cotonou.messoins.bj'),
    ('https://pharmaciecourcelles-demours-paris.mesoigner.fr', 'https://pharmacie-campguezo-cotonou.messoins.bj'),
]

def process_html_files():
    """Traiter tous les fichiers HTML"""
    html_dir = Path('pharmaciecourcelles-demours-paris.mesoigner.fr')
    
    if not html_dir.exists():
        print(f"❌ Dossier {html_dir} non trouvé")
        return False
    
    count = 0
    for html_file in html_dir.rglob('*.html'):
        try:
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content
            
            # Appliquer toutes les migrations
            for old, new in MIGRATIONS:
                content = content.replace(old, new)
            
            # Écrire seulement si changements
            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                count += 1
                if count % 100 == 0:
                    print(f"✅ {count} fichiers traités...")
        
        except Exception as e:
            print(f"⚠️  Erreur avec {html_file}: {e}")
    
    print(f"\n✅ {count} fichiers HTML mises à jour")
    return True

def main():
    print("🔄 Démarrage de la migration CDN...")
    print(f"  mesoigner → messoins")
    print(f"  pharmaciecourcelles-demours-paris.mesoigner.fr → pharmacie-campguezo-cotonou.messoins.bj\n")
    
    if process_html_files():
        print("\n✅ Migration terminée!")
        print("\nProchaines étapes:")
        print("1. Télécharger les CSS et fonts:")
        print("   curl -o public/assets/css/scripts.3e902af8.css https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css")
        print("   curl -o public/assets/css/mesoigner.6063c722.css https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css")
        print("2. Télécharger les assets:")
        print("   curl -o public/assets/uploads/header-wrapper.png https://cdn.mesoigner.fr/src/img/layout/header-wrapper.png")
        print("3. Renommer le dossier principal")
    else:
        print("\n❌ La migration a échoué")

if __name__ == '__main__':
    main()
