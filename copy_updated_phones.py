"""Copy updated chapter files from output_bni_chapterdetails to output_bni"""
import shutil
import os

files = [
    'bni_zenith.json',
    'bni_brilliance.json',
    'bni_dheeras.json',
    'bni_diamonds.json',
    'bni_enthiras.json',
    'bni_eternals.json',
    'bni_furious.json',
    'bni_jaaguar.json',
    'bni_jewels.json',
    'bni_joy.json',
    'bni_jubilant.json',
    'bni_marvels.json',
    'bni_maximus.json',
    'bni_nakshatras.json',
    'bni_queens.json',
    'bni_synergy.json',
    'bni_titans.json',
]

copied = 0
for f in files:
    src = f'output_bni_chapterdetails/{f}'
    dst = f'output_bni/{f}'
    if os.path.exists(src):
        shutil.copy(src, dst)
        copied += 1
        print(f'Copied {f}')

print(f'\nCopied {copied} files to output_bni')

