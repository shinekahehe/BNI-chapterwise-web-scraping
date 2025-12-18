"""Regenerate bni_chapters.py with only chapters that have existing JSONs in output_bni"""
import os
import re
from urllib.parse import urldefrag

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "chapter"

# Get existing JSON files in output_bni
output_bni_dir = "output_bni"
existing_slugs = set()
if os.path.exists(output_bni_dir):
    for f in os.listdir(output_bni_dir):
        if f.endswith(".json"):
            existing_slugs.add(f[:-5])  # Remove .json

print(f"Found {len(existing_slugs)} existing JSON files in output_bni")

# Read chapters_raw.txt
chapters = []
with open("chapters_raw.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

current_chapter = None
for line in lines:
    line = line.strip()
    if not line or line.startswith("PASTE") or line == "Link" or "Chapter Members" in line or "Home |" in line:
        continue
    
    # Check if it's a chapter name (tab-separated or just text)
    parts = line.split("\t")
    if len(parts) >= 2:
        name = parts[0].strip()
        url = parts[1].strip()
    else:
        # Try to detect if it's a URL
        if line.startswith("http"):
            if current_chapter:
                url = line
                chapters.append({"chapter": current_chapter, "url": url})
                current_chapter = None
            continue
        else:
            # Might be a chapter name
            current_chapter = line
            continue
    
    if not url or not url.startswith("http"):
        continue
    
    # Clean URL
    url = urldefrag(url)[0]
    
    # Skip unsupported links
    if any(x in url for x in ["share.google", "scribd", "drive.google"]):
        continue
    
    # Only include if:
    # 1. Not a chapterdetail/coregroupdetail URL (those go to output_bni_chapterdetails)
    # 2. Has a corresponding JSON file in output_bni
    if "chapterdetail" in url or "coregroupdetail" in url:
        continue
    
    slug = slugify(name)
    if slug in existing_slugs:
        chapters.append({"chapter": name, "url": url})

# Deduplicate by URL
seen_urls = set()
deduped = []
for c in chapters:
    if c["url"] not in seen_urls:
        seen_urls.add(c["url"])
        deduped.append(c)

print(f"Found {len(deduped)} matching chapters to re-scrape")

# Write to bni_chapters.py
with open("bni_chapters.py", "w", encoding="utf-8") as f:
    f.write("CHAPTERS = [\n")
    for c in deduped:
        f.write(f'    {{"chapter": "{c["chapter"]}", "url": "{c["url"]}"}},\n')
    f.write("]\n")

print(f"Written {len(deduped)} chapters to bni_chapters.py")

