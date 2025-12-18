"""Verify phone numbers in updated files"""
import json
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

print("Phone number verification:\n")
for f in files:
    path = f'output_bni/{f}'
    if os.path.exists(path):
        data = json.load(open(path, encoding='utf-8'))
        total = len(data)
        with_phone = len([m for m in data if m.get('phone')])
        print(f"{f}: {with_phone}/{total} members with phone numbers")
    else:
        print(f"{f}: File not found")

