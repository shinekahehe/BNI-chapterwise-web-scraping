"""Regenerate bni_chapters.py with only chapters that need phone number updates"""
import os
import re
from urllib.parse import urldefrag

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "chapter"

# Chapters that need phone number updates
chapters_to_update = [
    "BNI Zenith",
    "BNI Brilliance", 
    "BNI Dheeras",
    "BNI Diamonds",
    "BNI Enthiras",
    "BNI Eternals",
    "BNI Furious",
    "BNI Jaaguar",
    "BNI Jewels",
    "BNI Joy",
    "BNI Jubilant",
    "BNI Marvels",
    "BNI Maximus",
    "BNI Nakshatras",
    "BNI Queens",
    "BNI Synergy",
    "BNI Titans",
]

# Read chapters_raw.txt
chapters = []
with open("chapters_raw.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

current_chapter = None
for line in lines:
    line = line.strip()
    if not line or line.startswith("PASTE") or line.startswith("#"):
        continue
    
    # Check if line looks like a URL
    if line.startswith("http"):
        url = urldefrag(line.strip())[0]
        if current_chapter:
            # Only include if it's in our update list
            if current_chapter in chapters_to_update:
                chapters.append({"chapter": current_chapter, "url": url})
        current_chapter = None
    else:
        # This might be a chapter name
        current_chapter = line.strip()

# Also check if there are any remaining chapter names
if current_chapter and current_chapter in chapters_to_update:
    # Try to find URL in next lines
    pass

# Generate bni_chapters.py
output = '''"""BNI Chapters - Auto-generated for phone number updates"""

CHAPTERS = [
'''
for ch in chapters:
    chapter_name = ch["chapter"].replace('"', '\\"')
    url = ch["url"].replace('"', '\\"')
    output += f'    {{"chapter": "{chapter_name}", "url": "{url}"}},\n'

output += "]\n"

with open("bni_chapters.py", "w", encoding="utf-8") as f:
    f.write(output)

print(f"✅ Generated bni_chapters.py with {len(chapters)} chapters to update")
print(f"Chapters: {', '.join([c['chapter'] for c in chapters])}")

