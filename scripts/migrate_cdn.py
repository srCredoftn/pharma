#!/usr/bin/env python3
"""
Migration CDN complète: mesoigner → messoins
Traite tous les fichiers HTML et effectue les remplacements nécessaires
"""

import os
import sys
import re
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError
import json
from datetime import datetime

class CDNMigrator:
    def __init__(self):
        self.base_dir = Path('.')
        self.html_dir = Path('pharmaciecourcelles-demours-paris.mesoigner.fr')
        self.assets_dir = Path('public/assets')
        self.log = []
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'replacements': 0,
            'errors': 0
        }
        
        # Mapping des remplacements
        self.replacements = [
            # CDN CSS/JS
            ('https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css', '/assets/css/scripts.3e902af8.css'),
            ('https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css', '/assets/css/mesoigner.6063c722.css'),
            
            # CDN images/logos
            ('https://cdn.mesoigner.fr/uploads/logos/logo-mesoigner.svg', '/assets/uploads/logo-messoins.svg'),
            ('https://cdn.mesoigner.fr/src/img/layout/header-wrapper.png', '/assets/uploads/header-wrapper.png'),
            ('https://cdn.mesoigner.fr/src/img/widgets/que-prendre/que-prendre.png', '/assets/uploads/que-prendre.png'),
            
            # Branding générique CDN
            ('cdn.mesoigner.fr', 'cdn.messoins.bj'),
            
            # Branding
            ('data-theme="mesoigner"', 'data-theme="messoins"'),
            ('logo-mesoigner', 'logo-messoins'),
            ('mesoigner.svg', 'messoins.svg'),
            
            # Domaines (dans les URLs)
            ('https://pharmaciecourcelles-demours-paris.mesoigner.fr', 'https://pharmacie-campguezo-cotonou.messoins.bj'),
            ('pharmaciecourcelles-demours-paris.mesoigner.fr', 'pharmacie-campguezo-cotonou.messoins.bj'),
        ]
        
        # URLs à télécharger
        self.downloads = [
            ('https://cdn.mesoigner.fr/dist/front_pharmacies/scripts.3e902af8.css', 'public/assets/css/scripts.3e902af8.css'),
            ('https://cdn.mesoigner.fr/dist/front_pharmacies/mesoigner.6063c722.css', 'public/assets/css/mesoigner.6063c722.css'),
            ('https://cdn.mesoigner.fr/uploads/logos/logo-mesoigner.svg', 'public/assets/uploads/logo-messoins.svg'),
            ('https://cdn.mesoigner.fr/src/img/layout/header-wrapper.png', 'public/assets/uploads/header-wrapper.png'),
            ('https://cdn.mesoigner.fr/src/img/widgets/que-prendre/que-prendre.png', 'public/assets/uploads/que-prendre.png'),
        ]
    
    def setup_directories(self):
        """Créer la structure des dossiers"""
        print("📁 Création de la structure des répertoires...")
        (self.assets_dir / 'css').mkdir(parents=True, exist_ok=True)
        (self.assets_dir / 'uploads').mkdir(parents=True, exist_ok=True)
        (self.assets_dir / 'img').mkdir(parents=True, exist_ok=True)
        print("✅ Répertoires créés")
    
    def download_assets(self):
        """Télécharger les assets du CDN"""
        print("\n⬇️  Téléchargement des assets...")
        for url, local_path in self.downloads:
            try:
                local_file = Path(local_path)
                local_file.parent.mkdir(parents=True, exist_ok=True)
                
                if local_file.exists():
                    print(f"  ⏭️  {local_path} existe déjà")
                else:
                    print(f"  📥 Téléchargement: {url}")
                    urlretrieve(url, local_path)
                    print(f"     ✅ Enregistré: {local_path}")
            except URLError as e:
                print(f"  ❌ Erreur: {url} - {e}")
                self.stats['errors'] += 1
            except Exception as e:
                print(f"  ❌ Erreur inattendus: {local_path} - {e}")
                self.stats['errors'] += 1
    
    def process_html_file(self, file_path):
        """Traiter un fichier HTML"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            original_content = content
            
            # Appliquer tous les remplacements
            for old, new in self.replacements:
                count = content.count(old)
                if count > 0:
                    content = content.replace(old, new)
                    self.stats['replacements'] += count
            
            # Écrire seulement si changements
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.stats['files_modified'] += 1
                return True
            return False
        
        except Exception as e:
            print(f"  ❌ Erreur avec {file_path}: {e}")
            self.stats['errors'] += 1
            return False
    
    def migrate_html_files(self):
        """Traiter tous les fichiers HTML"""
        print("\n🔄 Traitement des fichiers HTML...")
        
        if not self.html_dir.exists():
            print(f"❌ Dossier {self.html_dir} non trouvé")
            return False
        
        html_files = list(self.html_dir.rglob('*.html'))
        print(f"   Trouvé: {len(html_files)} fichiers HTML")
        
        for idx, html_file in enumerate(html_files, 1):
            if self.process_html_file(html_file):
                if idx % 100 == 0:
                    print(f"   ✅ {idx} fichiers traités...")
        
        print(f"\n✅ Traitement terminé: {self.stats['files_modified']} fichiers modifiés")
        return True
    
    def verify_replacements(self):
        """Vérifier qu'il n'y a plus de références à l'ancien branding"""
        print("\n🔍 Vérification des restes...")
        patterns = ['mesoigner', 'pharmaciecourcelles-demours-paris']
        
        remaining = {}
        for pattern in patterns:
            count = 0
            for file_path in self.html_dir.rglob('*.html'):
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if pattern in content:
                        count += 1
                except:
                    pass
            if count > 0:
                remaining[pattern] = count
        
        if remaining:
            print(f"⚠️  Restes trouvés:")
            for pattern, count in remaining.items():
                print(f"   - '{pattern}': {count} fichiers")
        else:
            print("✅ Aucun reste trouvé - Migration complète!")
    
    def generate_report(self):
        """Générer un rapport"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'directory_structure': {
                'html_source': str(self.html_dir),
                'assets_target': str(self.assets_dir),
            }
        }
        
        report_path = Path('migration_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_summary(self):
        """Afficher le résumé"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE LA MIGRATION")
        print("="*60)
        print(f"Fichiers traités:       {self.stats['files_processed']}")
        print(f"Fichiers modifiés:      {self.stats['files_modified']}")
        print(f"Remplacements effectués: {self.stats['replacements']}")
        print(f"Erreurs:                {self.stats['errors']}")
        print("="*60)
        print("\n✅ Migration CDN mesoigner → messoins terminée!")
        print("\n📋 Prochaines étapes:")
        print("   1. Vérifier: ls -la public/assets/")
        print("   2. Tester les CSS: curl -I http://localhost/assets/css/scripts.3e902af8.css")
        print("   3. Renommer le dossier (optionnel)")
        print("   4. Commiter les changements")
    
    def run(self):
        """Exécuter la migration complète"""
        print("🚀 MIGRATION CDN: mesoigner → messoins")
        print("="*60)
        
        self.setup_directories()
        self.download_assets()
        self.migrate_html_files()
        self.verify_replacements()
        report = self.generate_report()
        self.print_summary()
        
        print(f"\n📄 Rapport sauvegardé: migration_report.json")
        return True

def main():
    try:
        migrator = CDNMigrator()
        migrator.run()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n⏸️  Migration interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
