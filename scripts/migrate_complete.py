#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 MIGRATION COMPLÈTE - Script Python
Effectue TOUS les find/replace pour passer de mesoigner → messoins
et pharmaciecourcelles-demours-paris.mesoigner.fr → pharmacie-campguezo-cotonou.messoins.bj
"""

import os
import re
import sys
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

# Dictionnaire des remplacements
REPLACEMENTS = [
    # URLs CDN → Chemins locaux
    ('https://cdn\\.mesoigner\\.fr/dist/front_pharmacies/scripts\\.3e902af8\\.css', '/assets/css/scripts.3e902af8.css'),
    ('https://cdn\\.mesoigner\\.fr/dist/front_pharmacies/mesoigner\\.6063c722\\.css', '/assets/css/mesoigner.6063c722.css'),
    ('https://cdn\\.mesoigner\\.fr/uploads/logos/logo-mesoigner\\.svg', '/assets/uploads/logo-messoins.svg'),
    ('https://cdn\\.mesoigner\\.fr/src/img/layout/header-wrapper\\.png', '/assets/uploads/header-wrapper.png'),
    ('https://cdn\\.mesoigner\\.fr/src/img/widgets/que-prendre/que-prendre\\.png', '/assets/uploads/que-prendre.png'),
    
    # Chemins relatifs CDN (pour fichiers dans subdossiers)
    ('\\.\\./cdn\\.mesoigner\\.fr/dist/front_pharmacies/scripts\\.3e902af8\\.css', '/assets/css/scripts.3e902af8.css'),
    ('\\.\\./cdn\\.mesoigner\\.fr/dist/front_pharmacies/mesoigner\\.6063c722\\.css', '/assets/css/mesoigner.6063c722.css'),
    ('\\.\\./cdn\\.mesoigner\\.fr/src/img/layout/header-wrapper\\.png', '/assets/uploads/header-wrapper.png'),
    ('\\.\\./cdn\\.mesoigner\\.fr/uploads/logos/logo-mesoigner\\.svg', '/assets/uploads/logo-messoins.svg'),
    
    # Data-theme
    ('data-theme=["\']mesoigner["\']', 'data-theme="messoins"'),
    
    # Branding
    ('logo-mesoigner', 'logo-messoins'),
    ('mesoigner\\.svg', 'messoins.svg'),
    
    # Domaine principal
    ('pharmaciecourcelles-demours-paris\\.mesoigner\\.fr', 'pharmacie-campguezo-cotonou.messoins.bj'),
    
    # CDN complet
    ('https://cdn\\.mesoigner\\.fr/', 'https://cdn.messoins.bj/'),
]

def migrate_file(filepath):
    """Migrate a single file with all replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for pattern, replacement in REPLACEMENTS:
            content = re.sub(pattern, replacement, content)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    except Exception as e:
        print_warning(f"Erreur lors du traitement de {filepath}: {str(e)}")
        return False

def main():
    print_header("🚀 MIGRATION COMPLÈTE - MESOIGNER → MESSOINS")
    print()
    
    # Vérifier le répertoire
    html_dir = Path("pharmaciecourcelles-demours-paris.mesoigner.fr")
    
    if not html_dir.exists():
        print_error(f"Le répertoire {html_dir} n'existe pas!")
        print_info("Assurez-vous d'être dans le bon répertoire")
        sys.exit(1)
    
    print_info(f"Répertoire trouvé: {html_dir.absolute()}")
    print()
    
    # Compter les fichiers
    html_files = list(html_dir.rglob("*.html"))
    total = len(html_files)
    
    print_info(f"Fichiers HTML trouvés: {total}")
    print()
    
    if total == 0:
        print_warning("Aucun fichier HTML trouvé!")
        sys.exit(1)
    
    # Demander confirmation
    print_warning("Ceci va modifier TOUS les fichiers HTML")
    response = input("Continuer? (oui/non): ").strip().lower()
    
    if response not in ['oui', 'yes', 'o', 'y']:
        print_info("Migration annulée")
        sys.exit(0)
    
    print()
    print_header("TRAITEMENT EN COURS")
    print()
    
    # Traiter les fichiers
    modified = 0
    errors = 0
    
    for i, filepath in enumerate(html_files, 1):
        # Barre de progression
        percent = (i * 100) // total
        bar_length = 40
        filled = (percent * bar_length) // 100
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\r[{bar}] {percent}% ({i}/{total})", end='', flush=True)
        
        if migrate_file(filepath):
            modified += 1
        else:
            errors += 1
    
    print()  # Nouvelle ligne après la barre
    print()
    
    # Résultats
    print_header("RÉSULTATS")
    print()
    
    print_success(f"Fichiers traités: {total}")
    print_success(f"Fichiers modifiés: {modified}")
    
    if errors > 0:
        print_warning(f"Fichiers avec erreurs: {errors}")
    
    print()
    
    # Vérifications
    print_header("VÉRIFICATIONS")
    print()
    
    print_info("Vérification en cours...")
    print()
    
    # Compter les occurrences restantes
    old_domain_count = 0
    old_cdn_count = 0
    messoins_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            old_domain_count += content.count('pharmaciecourcelles-demours-paris')
            old_cdn_count += content.count('https://cdn.mesoigner.fr')
            messoins_count += content.count('messoins')
        except:
            pass
    
    print_success(f"Références au nouveau domaine (messoins): {messoins_count}")
    print_success(f"Anciennes références au domaine: {old_domain_count}")
    print_success(f"Anciennes URL CDN mesoigner: {old_cdn_count}")
    
    print()
    
    if old_domain_count == 0 and old_cdn_count == 0:
        print_success("✨ Migration réussie! Aucune ancienne référence trouvée")
    else:
        print_warning("Certaines anciennes références restent")
        print_info("Cela peut être normal si elles sont dans les commentaires ou données")
    
    print()
    print_header("PROCHAINES ÉTAPES")
    print()
    
    print("1. Renommer le dossier (IMPORTANT):")
    print("   mv pharmaciecourcelles-demours-paris.mesoigner.fr pharmacie-campguezo-cotonou.messoins.bj")
    print()
    
    print("2. Mettre à jour config/app.php (si nécessaire):")
    print("   - Vérifier le domaine de base")
    print("   - Vérifier les URLs de base")
    print()
    
    print("3. Tester localement:")
    print("   php artisan serve")
    print()
    
    print_success("Migration Python terminée! 🎉")
    print()

if __name__ == "__main__":
    main()
