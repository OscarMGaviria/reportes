import json

new_data_ebejico = {
    "CONSTRUCCIÓN DE ALCANTARILLAS": {
        "entregable": "153 un",
        "actividades": {
            "2.8": 179.0,
            "2.14.1": 228.0,
            "4.1.8": 5202.0,
            "4.2.2": 1683.0,
            "5.1.7": 612.0,
            "6.2.4": 153.0,
            "6.2.24": 1348.0,
            "8.1": 828.0,
            "8.27": 918.0,
            "10.1": 74052.0,
            "13.1": 39780.0
        }
    },
    "CONSTRUCCIÓN DE CUNETA": {
        "entregable": "28,760 m",
        "actividades": {
            "4.1.8": 4999.0,
            "5.1.7": 2301.0,
            "6.2.50": 2876.0,
            "10.1": 80530.0,
            "13.1": 149565.0
        }
    },
    "CONSTRUCCIÓN DE FILTRO PARA CUNETAS": {
        "entregable": "28,760 m",
        "actividades": {
            "8.13.1": 28760.0,
            "13.9": 672984.0
        }
    },
    "CONSTRUCCIÓN DE BORDILLOS": {
        "entregable": "5,752 m",
        "actividades": {
            "4.1.2": 460.0,
            "5.1.7": 115.0,
            "14.3": 5752.0
        }
    },
    "CONSTRUCCIÓN DE DISIPADORES": {
        "entregable": "115 un",
        "actividades": {
            "4.1.9": 604.0,
            "6.1.18.1": 805.0,
            "8.18": 690.0,
            "10.1": 3910.0
        }
    },
    "ESTABILIZACION CON MATERIAL GRANULAR": {
        "entregable": "28.76 Km",
        "actividades": {
            "4.1.1": 3020.0,
            "5.1.2": 3020.0,
            "5.2.16": 40264.0,
            "5.2.13": 7478.0,
            "4.1.96": 5982.0,
            "4.3.8": 5982.0,
            "5.1.15": 18406.0,
            "7.1.1": 143800.0,
            "7.1.12.2": 143800.0,
            "13.1": 1575423.85,
            "13.2": 45300.0
        }
    },
    "SEÑALIZACIÓN VIAL": {
        "entregable": "28.76 Km",
        "actividades": {
            "12.1": 86280.0,
            "12.9": 145.0
        }
    }
}

with open('actividades.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for circuito in data.get('circuitos', []):
    if "EBEJICO" in circuito['nombre'].upper() or "EBÉJICO" in circuito['nombre'].upper():
        for cat in circuito.get('categorias', []):
            cat_name = cat['nombre']
            if cat_name in new_data_ebejico:
                cat['entregable'] = new_data_ebejico[cat_name]['entregable']
                
                # Update actividades
                for act in cat.get('actividades', []):
                    item = act['item']
                    if item in new_data_ebejico[cat_name]['actividades']:
                        act['cantidad_inicial'] = new_data_ebejico[cat_name]['actividades'][item]

with open('actividades.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated EBEJICO - HELICONIA successfully.")
