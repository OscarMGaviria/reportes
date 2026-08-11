import json

new_data_sopetran = {
    "CONSTRUCCIÓN DE ALCANTARILLAS": {
        "entregable": "141 un",
        "actividades": {
            "2.8": 34.0,
            "2.14.1": 210.0,
            "4.1.8": 4794.0,
            "4.2.2": 1551.0,
            "5.1.7": 564.0,
            "6.2.4": 141.0,
            "6.2.24": 1242.0,
            "8.1": 1056.0,
            "8.27": 846.0,
            "10.1": 68244.0,
            "13.1": 24139.0
        }
    },
    "CONSTRUCCIÓN DE CUNETA": {
        "entregable": "35,190 m",
        "actividades": {
            "4.1.8": 6116.0,
            "5.1.7": 2815.0,
            "6.2.50": 3519.0,
            "10.1": 98534.0,
            "13.1": 120482.0
        }
    },
    "CONSTRUCCIÓN DE FILTRO PARA CUNETAS": {
        "entregable": "35,190 m",
        "actividades": {
            "8.13.1": 35190.0,
            "13.9": 542207.52
        }
    },
    "CONSTRUCCIÓN DE BORDILLOS": {
        "entregable": "7,038 m",
        "actividades": {
            "4.1.2": 563.0,
            "5.1.7": 141.0,
            "14.3": 7038.0
        }
    },
    "CONSTRUCCIÓN DE DISIPADORES": {
        "entregable": "106 un",
        "actividades": {
            "4.1.9": 2226.0,
            "6.1.18.1": 742.0,
            "8.18": 636.0,
            "10.1": 3602.0
        }
    },
    "ESTABILIZACION CON MATERIAL GRANULAR": {
        "entregable": "35.19 Km",
        "actividades": {
            "4.1.1": 3695.0,
            "5.1.2": 3695.0,
            "5.2.16": 49266.0,
            "5.2.13": 9149.0,
            "4.1.96": 7320.0,
            "4.3.8": 7320.0,
            "5.1.15": 22521.0,
            "7.1.1": 175950.0,
            "7.1.12.2": 175950.0,
            "13.1": 1269269.20,
            "13.2": 55425.0
        }
    },
    "SEÑALIZACIÓN VIAL": {
        "entregable": "35.19 Km",
        "actividades": {
            "12.1": 105570.0,
            "12.9": 175.0
        }
    }
}

with open('actividades.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for circuito in data.get('circuitos', []):
    if "SOPETRAN" in circuito['nombre'].upper() or "SOPETRÁN" in circuito['nombre'].upper():
        for cat in circuito.get('categorias', []):
            cat_name = cat['nombre']
            if cat_name in new_data_sopetran:
                cat['entregable'] = new_data_sopetran[cat_name]['entregable']
                
                # Update actividades
                for act in cat.get('actividades', []):
                    item = act['item']
                    if item in new_data_sopetran[cat_name]['actividades']:
                        act['cantidad_inicial'] = new_data_sopetran[cat_name]['actividades'][item]

with open('actividades.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated SOPETRAN successfully.")
