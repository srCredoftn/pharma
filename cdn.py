import os
import re
from urllib.parse import urlparse

# === Configuration ===
root_dir = "."  # dossier du projet
text_extensions = {".html", ".htm", ".js", ".css"}

# Liste des CDN open-source connus
open_source_cdns = [
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "stackpath.bootstrapcdn.com",
    "code.jquery.com",
    "cdn.jsdelivr.com",
    "cdn.jsdelivr.net"
]

# Stocker les résultats
cdn_results = []

def check_cdn(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    if not domain:
        return None  # pas une URL externe
    if any(known in domain for known in open_source_cdns):
        return "open-source"
    else:
        return "propriétaire"

def scan_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in text_extensions:
        return
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        urls = re.findall(r'(https?://[^\s\'")]+)', content)
        for url in urls:
            status = check_cdn(url)
            if status:
                cdn_results.append((filepath, url, status))
    except Exception as e:
        print(f"⚠️ Erreur fichier : {filepath} ({e})")

def main():
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            scan_file(os.path.join(dirpath, file))

    print("\n=== Résultat CDN ===")
    for filepath, url, status in cdn_results:
        print(f"{status.upper():>12} | {url} | {filepath}")

if __name__ == "__main__":
    main()
