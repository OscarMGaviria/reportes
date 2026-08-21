import json
with open('src/data/catalogo_actividades.json', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'CONSTRUCCI.*?N', 'CONSTRUCCIÓN', text)

with open('src/data/catalogo_actividades.json', 'w', encoding='utf-8') as f:
    f.write(text)
