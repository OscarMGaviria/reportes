import json
with open('src/data/Circuitos.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

for feature in data['features']:
    props = feature['properties']
    name = str(props.get('NOMBRE_VIA', '')) + ' - ' + str(props.get('CIRCUITO', '')) + ' - ' + str(props.get('MPIO_NOMBR', ''))
    if 'SOPETRAN' in name.upper() or 'BELMIRA' in name.upper() or 'HORIZONTES' in name.upper():
        print(f"{name} - FECHA_INI: {props.get('FECHA_INI')} - PLAZO_MESE: {props.get('PLAZO_MESE')}")
