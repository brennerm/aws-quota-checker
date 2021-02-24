import sys

import keepachangelog

CATEGORIES = ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security']

version = sys.argv[1]

changes = keepachangelog.to_dict("CHANGELOG.md")[version]

print('## Changelog')
for category in CATEGORIES:
    entries = changes.get(category, [])

    if entries:
        print(f'### {category.capitalize()}') 

    for entry in entries:
        print(f'- {entry}') 
