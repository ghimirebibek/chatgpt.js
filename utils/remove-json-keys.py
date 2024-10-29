'''
Script:       remove-json-keys.py
Version:      2023.9.21
Description:  Remove key/value pairs from json_folder/**.json
Author:       Adam Lui
URL:          https://github.com/adamlui/python-utils
'''

import os
import json

json_folder = '_locales'

# Prompt user for keys to remove
keys_to_remove = []
while True:
    key = input("Enter key to remove (or ENTER if done): ")
    if not key:
        break
    keys_to_remove.append(key)

# Locate JSON directory
script_dir = os.path.abspath(os.path.dirname(__file__))
json_dir = None
for root, dirs, _ in os.walk(script_dir):
    if json_folder in dirs:
        json_dir = os.path.join(root, json_folder)
        break
else:
    print(f"Unable to locate a {json_folder} directory.")
    exit()

# Process JSON files and remove specified keys
processed_count = 0
keys_removed_count, keys_skipped_count = 0, 0

for root, _, files in os.walk(json_dir):
    for filename in files:
        if filename.endswith('.json'):
            file_path = os.path.join(root, filename)
            
            # Load JSON data
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_path}")
                    continue
            
            # Track whether any keys are removed
            modified = False
            for key in keys_to_remove:
                if key in data:
                    del data[key]
                    keys_removed_count += 1
                    modified = True
                else:
                    keys_skipped_count += 1
            
            # Write back if modified
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                processed_count += 1

# Final summary
print(f'\nProcessed JSON Files: {processed_count}')
print(f'Keys Removed: {keys_removed_count}')
print(f'Keys Skipped (not found): {keys_skipped_count}')
